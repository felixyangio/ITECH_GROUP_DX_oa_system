<script setup name="stafflist">
import OAMain from '@/components/OAMain.vue';
import { ref, reactive, onMounted, watch } from "vue";
import timeFormatter from '@/utils/timeFormatter';
import staffHttp from '@/api/staffHttp';
import { ElMessage } from 'element-plus';
import OADialog from '@/components/OADialog.vue';
import { useAuthStore } from '@/stores/auth';


const authStore = useAuthStore()

let staffs = ref([])
let pagination = reactive({
    page: 1,
    total: 0
})
let page_size = ref(10)
let dialogVisible = ref(false)
let staffForm = reactive({
    status: 1
})
let handleIndex = 0
let departments = ref([])
let filterForm = reactive({
    department_id: null,
    realname: "",
    date_joined: []
})
let tableRef = ref()
const BASE_URL = import.meta.env.VITE_BASE_URL


async function fetchStaffList(page, page_size) {
    try {
        // Get employee list
        let data = await staffHttp.getStaffList(page, page_size, filterForm)
        pagination.total = data.count
        pagination.page = page
        staffs.value = data.results
    } catch (detail) {
        ElMessage.error(detail)
    }
}

onMounted(async () => {
    fetchStaffList(1, page_size.value)

    try {
        let data = await staffHttp.getAllDepartment()
        departments.value = data.results;
    } catch (detail) {
        ElMessage.error(detail)
    }
})

watch(() => pagination.page, async function (value) {
    fetchStaffList(value, page_size.value)
})

watch(page_size, function (value) {
    if (pagination.page == 1) {
        fetchStaffList(1, value)
    } else {
        pagination.page = 1
    }
})

const onEditStaff = (index) => {
    handleIndex = index
    dialogVisible.value = true;
    let staff = staffs.value[index]
    staffForm.status = staff.status
}

const onSubmitEditStaff = async () => {
    let staff = staffs.value[handleIndex]
    try {
        let newstaff = await staffHttp.updateStaffStatus(staff.uid, staffForm.status)
        ElMessage.success("Employee status updated successfully.")
        dialogVisible.value = false;
        staffs.value.splice(handleIndex, 1, newstaff)
    } catch (detail) {
        ElMessage.error(detail)
    }
}

const onSearch = () => {
    fetchStaffList(1, page_size.value)
}

const onDownload = async () => {
    let rows = tableRef.value.getSelectionRows()
    if(!rows || rows.length==0){
        ElMessage.info('Employee status updated successfully!')
        return;
    }
    try{
        let response = await staffHttp.downloadStaffs(rows.map(row => row.uid))
        // Create a URL object from the returned binary data.
        let href = URL.createObjectURL(response.data)
        const a = document.createElement("a")
        a.href = href
        a.setAttribute('download', 'Employee Information.xlsx')
       
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        // Revoke the URL object
        URL.revokeObjectURL(href)
    }catch(detail){
        ElMessage.error(detail)
    }
}

const onUploadSuccess = () => {
    ElMessage.success("Employees uploaded successfully.")
    // Refetch the employee data for the first page.
    fetchStaffList(1, page_size.value)
}

const onUploadFail = (error) => {
    const detail = JSON.parse(error.message).detail
    ElMessage.error(detail)
}

</script>

<template>
    <OADialog title="Update Employee Status" v-model="dialogVisible" @submit="onSubmitEditStaff">
        <el-form :model="staffForm" label-width="100px">
            <el-form-item label="Status">
                <el-radio-group v-model="staffForm.status" class="ml-4">
                    <el-radio :value="1">Active</el-radio>
                    <el-radio :value="3">Locked</el-radio>
                </el-radio-group>
            </el-form-item>
        </el-form>
    </OADialog>
    <OAMain title="Employee List">
        <el-card>
            <el-form :inline="true" class="my-form-inline">
                <el-form-item label="Department">
                    <el-select v-model="filterForm.department_id">
                        <el-option v-for="department in departments" :label="department.name" :value="department.id"
                            :key="department.name" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Name">
                    <el-input v-model="filterForm.realname" />
                </el-form-item>
                <el-form-item label="Join Date">
                    <el-date-picker v-model="filterForm.date_joined" type="daterange" range-separator="to"
                        start-placeholder="Start Date" end-placeholder="End Date" format="YYYY-MM-DD" value-format="YYYY-MM-DD" />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" icon="Search" @click="onSearch"></el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="danger" icon="Download" @click="onDownload">Download</el-button>
                </el-form-item>

                <el-form-item>
                    <el-upload
                        :action="BASE_URL+'/staff/upload'"
                        :headers="{Authorization: 'JWT '+authStore.token}"
                        :on-success="onUploadSuccess"
                        :on-error="onUploadFail"
                        :show-file-list="false"
                        :auto-upload="true"
                        accept=".xlsx, .xls">
                        <el-button type="danger" icon="Upload">Upload</el-button>
                    </el-upload>
                </el-form-item>
            </el-form>
        </el-card>
        <el-card>
            <el-table :data="staffs" ref="tableRef">
                <el-table-column type="selection" width="55"></el-table-column>
                <el-table-column label="No." width="60">
                    <template #default="scope">{{ scope.$index + 1 }}</template>
                </el-table-column>
                <el-table-column prop="realname" label="Name"></el-table-column>
                <el-table-column prop="email" label="Email"></el-table-column>
                <el-table-column label="Join Date">
                    <template #default="scope">
                        {{ timeFormatter.stringFromDate(scope.row.date_joined) }}
                    </template>
                </el-table-column>
                <el-table-column prop="department.name" label="Department"></el-table-column>
                <el-table-column label="Status">
                    <template #default="scope">
                        <el-tag v-if="scope.row.status == 1" type="success">Active</el-tag>
                        <el-tag v-else-if="scope.row.status == 2" type="warning">Inactive</el-tag>
                        <el-tag v-else type="danger">Locked</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="Actions">
                    <template #default="scope">
                        <el-button type="primary" icon="Edit" circle @click="onEditStaff(scope.$index)"></el-button>
                    </template>
                </el-table-column>
            </el-table>

            <template #footer>
                <div style="display: flex; justify-content: space-between;">
                    <el-form-item label="Items per page:">
                        <el-select v-model="page_size" size="small" style="width: 100px;">
                            <el-option select label="10 items/page" :value="10" />
                            <el-option label="20 items/page" :value="20" />
                        </el-select>
                    </el-form-item>
                    <el-pagination background layout="prev, pager, next" :total="pagination.total"
                        v-model:currentPage="pagination.page" :page-size="page_size" />
                </div>
            </template>
        </el-card>
    </OAMain>
</template>

<style scoped>
.my-form-inline .el-input {
    --el-input-width: 140px;
}

.my-form-inline .el-select {
    --el-select-width: 140px;
}

.el-form--inline .el-form-item {
    margin-right: 20px;
}
</style>