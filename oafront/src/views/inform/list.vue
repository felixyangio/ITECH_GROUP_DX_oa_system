<script setup name="informlist">
import { ref, reactive, onMounted } from "vue"
import OAMain from "@/components/OAMain.vue";
import OADialog from "@/components/OADialog.vue";
import OAPagination from "@/components/OAPagination.vue";
import timeFormatter from "@/utils/timeFormatter"
import { useAuthStore } from "@/stores/auth";
import informHttp from "@/api/informHttp";
import { ElMessage } from "element-plus";

const authStore = useAuthStore()

let informs = ref([])
let pagination = reactive({
    page: 1,
    total: 0
})
let dialogVisible = ref(false)
let handleIndex = 0

onMounted(async () => {
    try {
        let data = await informHttp.getInformList(1)
        // data = {count: 10, next: , previous: , results: []}
        pagination.total = data.count
        informs.value = data.results
        console.log(data.results);
    } catch (detail) {
        ElMessage.error(detail)
    }
})


const onShowDialog = (index) => {
    handleIndex = index
    dialogVisible.value = true;
}

const onDeleteInform = async () => {
    try {
        let inform = informs.value[handleIndex]
        await informHttp.deleteInform(inform.id)
        informs.value.splice(handleIndex, 1)
        dialogVisible.value = false;
        ElMessage.success("Notification deleted successfully.")
    } catch (detail) {
        ElMessage.error(detail)
    }
}

</script>

<template>
    <OADialog v-model="dialogVisible" title="Prompt" @submit="onDeleteInform">
        <span>Are you sure you want to delete this notification?</span>
    </OADialog>
    <OAMain title="Notification List">
        <el-card>
            <el-table :data="informs">
                <el-table-column label="Title">
                    <template #default="scope">
                        <el-badge v-if="scope.row.reads.length==0" is-dot class="item">
                            <RouterLink :to="{ name: 'inform_detail', params: { pk: scope.row.id } }">{{ scope.row.title }}</RouterLink>
                        </el-badge>
                        <RouterLink v-else :to="{ name: 'inform_detail', params: { pk: scope.row.id } }">{{ scope.row.title }}</RouterLink>
                    </template>
                </el-table-column>
                <el-table-column label="Publisher">
                    <template #default="scope">
                        {{ '[' + scope.row.author.department.name + ']' + scope.row.author.realname }}
                    </template>
                </el-table-column>
                <el-table-column label="Publish Time">
                    <template #default="scope">
                        {{ timeFormatter.stringFromDateTime(scope.row.create_time) }}
                    </template>
                </el-table-column>
                <el-table-column label="Visible Departments">
                    <template #default="scope">
                        <el-tag v-if="scope.row.public" type="success"> Public</el-tag>
                        <el-tag v-else v-for="department in scope.row.departments" :key="department.name" type="info">{{
                            department.name }}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="Action">
                    <template #default="scope">
                        <el-button v-if="scope.row.author.uid == authStore.user.uid" @click="onShowDialog(scope.$index)"
                            type="danger" icon="Delete" />
                        <el-button v-else disabled type="default">None</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <template #footer>
                <OAPagination v-model="pagination.page" :total="pagination.total"></OAPagination>
            </template>
        </el-card>
    </OAMain>
</template>

<style scoped>
.el-badge{
    margin-right: 4px;
    margin-top: 4px;
}
.el-tag{
  margin-right: 4px;
}
</style>