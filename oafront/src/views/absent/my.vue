<script setup name="myabsent">
import OAPageHeader from "@/components/OAPageHeader.vue";
import { ref, reactive, onMounted, computed, watch } from "vue"
import absentHttp from "@/api/absentHttp";
import { ElMessage } from "element-plus";
import timeFormatter from "@/utils/timeFormatter";
import OAMain from "@/components/OAMain.vue";
import OAPagination from "@/components/OAPagination.vue";
import OADialog from "@/components/OADialog.vue";


let formLabelWidth = '140px'
let dialogFormVisible = ref(false)
let absentForm = reactive({
  title: '',
  absent_type_id: null,
  date_range: [],
  request_content: ''
})
let absentFormRef = ref()
let rules = reactive({
  title: [
    { required: true, message: 'Please enter the title.', trigger: 'blur' },
  ],
  absent_type_id: [
    { required: true, message: 'Please select the leave type.', trigger: 'change' },
  ],
  date_range: [
    { required: true, message: 'Please select the leave period.', trigger: 'change' },
  ],
  request_content: [
    { required: true, message: 'Please enter the leave reason.', trigger: 'blur' },
  ],
})
// My Attendance
let absents = ref([])
let absent_types = ref([])
let responder = reactive({
  email: '',
  realname: ''
})

let pagination = reactive({
  total: 0,
  page: 1
})
let responder_str = computed(() => {
  if (responder.email) {
    return '[' + responder.email + ']' + responder.realname
  } else {
    return "None"
  }
})

watch(() => pagination.page, (value) => {
  requestAbsents(value);
})

const requestAbsents = async (page) => {
  try {
    let absents_data = await absentHttp.getMyAbsents(page)
    let total = absents_data.count;
    pagination.total = total;
    let results = absents_data.results;
    absents.value = results
  } catch (detail) {
    ElMessage.error(detail)
  }
}

const onShowDialog = () => {
  absentForm.title = '',
    absentForm.absent_type_id = null,
    absentForm.date_range = [],
    absentForm.request_content = ''
  dialogFormVisible.value = true;
}

const onSubmitAbsent = () => {
  absentFormRef.value.validate(async (valid, fields) => {
    if (valid) {
      let data = {
        title: absentForm.title,
        absent_type_id: absentForm.absent_type_id,
        start_date: absentForm.date_range[0],
        end_date: absentForm.date_range[1],
        request_content: absentForm.request_content
      }
      try {
        let absent = await absentHttp.applyAbsent(data)
        dialogFormVisible.value = false;
        absents.value.unshift(absent)
        ElMessage.success('Leave request submitted successfully.');
      } catch (detail) {
        ElMessage.error(detail)
      }
    }
  })
}

onMounted(async () => {
  try {
    // Get Leave Types
    let absent_types_data = await absentHttp.getAbsentTypes()
    absent_types.value = absent_types_data

    // Get Approvers
    let responder_data = await absentHttp.getResponder()
    Object.assign(responder, responder_data)

    // Get My Attendance
    requestAbsents(1)
  } catch (detail) {
    ElMessage.error(detail)
  }
})
</script>

<template>
  <OAMain title="My Attendance">
       <el-card style="text-align: right">
      <el-button type="primary" @click="onShowDialog"><el-icon>
          <Plus />
        </el-icon>Request Leave</el-button>
    </el-card>
    <el-card>
      <el-table :data="absents" style="width: 100%">
        <el-table-column prop="title" label="Title" />
        <el-table-column prop="absent_type.name" label="Leave Type" />
        <el-table-column prop="request_content" label="Leave Reason" />
        <el-table-column prop="create_time" label="Create Time" width="200">
          <template #default="scope">
            {{ timeFormatter.stringFromDateTime(scope.row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="start_date" label="Start Date" />
        <el-table-column prop="end_date" label="End Date" />
        <el-table-column label="Approver">
          <template #default="scope">
            <!-- {{ scope.row.responder_str }} -->
            {{ responder_str }}
          </template>
        </el-table-column>

        <el-table-column prop="response_content" label="Feedback" />
        <el-table-column label="Status">
          <template #default="scope">
            <el-tag type="info" v-if="scope.row.status == 1">Pending</el-tag>
            <el-tag type="success" v-else-if="scope.row.status == 2">Approved</el-tag>
            <el-tag type="danger" v-else>Rejected</el-tag>
          </template>
        </el-table-column>
      </el-table>
      <template #footer>
        <OAPagination v-model:page="pagination.page" :total="pagination.total"></OAPagination>
      </template>
    </el-card>

  </OAMain>

  <OADialog title="Apply for Leave" v-model="dialogFormVisible" @submit="onSubmitAbsent" >
    <el-form :model="absentForm" label-width="120px" label-position="right" :rules="rules" ref="absentFormRef">
      <el-form-item label="Title" :label-width="formLabelWidth" prop="title">
        <el-input v-model="absentForm.title" placeholder="Enter leave title" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Leave Type" :label-width="formLabelWidth" prop="absent_type_id">
        <el-select v-model="absentForm.absent_type_id" placeholder="Select Leave Type">
          <el-option v-for="item in absent_types" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="Leave Period" :label-width="formLabelWidth" prop="date_range">
        <el-date-picker v-model="absentForm.date_range" type="daterange" start-placeholder="Start date"
          end-placeholder="End date" format="YYYY-MM-DD" value-format="YYYY-MM-DD" />
      </el-form-item>
      <el-form-item label="Approver" :label-width="formLabelWidth">
        <el-input :value="responder_str" readonly disabled autocomplete="off" />
      </el-form-item>
      <el-form-item label="Leave Reason" :label-width="formLabelWidth">
        <el-input type="textarea" v-model="absentForm.request_content" placeholder="Enter leave reason"
          autocomplete="off" />
      </el-form-item>
    </el-form>
  </OADialog>
</template>
<style scoped>
</style>