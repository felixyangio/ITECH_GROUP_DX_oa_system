<script setup name="subabsent">
import OAPageHeader from "@/components/OAPageHeader.vue";
import { ref, reactive, onMounted } from "vue"
import absentHttp from "@/api/absentHttp";
import { ElMessage } from "element-plus";
import timeFormatter from "@/utils/timeFormatter";
import OAMain from "@/components/OAMain.vue";
import OAPagination from "@/components/OAPagination.vue";
import OADialog from "@/components/OADialog.vue";


let absents = ref([]);
let pagination = reactive({
  total: 0,
  page: 1
})
let absentForm = reactive({
  status: 2,
  response_content: ""
})
let rules = reactive({
  status: [{ required: true, message: 'Please select a decision.', trigger: 'change' }],
  response_content: { required: true, messgae: 'Please provide a reason.', trigger: 'blur' }
})
let dialogVisible = ref(false)
let absentFormRef = ref()
let handleIndex = null

onMounted(async () => {
  try {
    let data = await absentHttp.getSubAbsents()
    pagination.total = data.total
    absents.value = data.results
  } catch (detail) {
    ElMessage.error(detail)
  }
})

const onShowDialog = (index) => {
  absentForm.status = 2;
  absentForm.response_content = ""
  dialogVisible.value = true;
  handleIndex = index
}

const onSubmitAbsent = async() => {
  absentFormRef.value.validate(async (valid, fields) => {
    if (valid) {
      try {
        dialogVisible.value = false;
        const absent = absents.value[handleIndex]
        const data = await absentHttp.handleSubAbsent(absent.id, absentForm.status, absentForm.response_content)
        absents.value.splice(handleIndex, 1, data)
        ElMessage.success('Team attendance processed successfully.');

      } catch (detail) {
        ElMessage.error(detail)
      }
    }
  })
}

const onCancelProcess = () => {
  dialogVisible.value = false
}
</script>

<template>
  <OADialog title="Process Attendance" v-model="dialogVisible" @submit="onSubmitAbsent" @cancel="onCancelProcess">
    <el-form :model="absentForm" label-width="120px" label-position="right" :rules="rules" ref="absentFormRef">
      <el-form-item label="Result" prop="status">
        <el-radio-group v-model="absentForm.status">
          <el-radio :value="2">Approve</el-radio>
          <el-radio :value="3">Reject</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="Reason" prop="response_content">
        <el-input type="textarea" v-model="absentForm.response_content" placeholder="Enter reject reason" />
      </el-form-item>
    </el-form>
  </OADialog>
  <OAMain title="Team Attendance">
    <el-card>
      <el-table :data="absents" style="width: 100%">
        <el-table-column prop="title" label="Title" />
        <el-table-column label="Applicant">
          <template #default="{ row }">
            {{ '[' + row.requester.department.name + ']' + row.requester.realname }}
          </template>
        </el-table-column>
        <el-table-column prop="absent_type.name" label="Leave Type" />
        <el-table-column prop="request_content" label="Leave Reason" />
        <el-table-column prop="create_time" label="Create Time" width="200">
          <template #default="scope">
            {{ timeFormatter.stringFromDateTime(scope.row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="start_date" label="Start Date" />
        <el-table-column prop="end_date" label="End Date" />
        <el-table-column prop="responder.realname" label="Approver" />
        <el-table-column prop="response_content" label="Feedback" />
        <el-table-column label="Status">
          <template #default="scope">
            <el-tag type="info" v-if="scope.row.status == 1">Pending</el-tag>
            <el-tag type="success" v-else-if="scope.row.status == 2">Approved</el-tag>
            <el-tag type="danger" v-else>Rejected</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Process">
          <template #default="scope">
            <el-button v-if="scope.row.status == 1" @click="onShowDialog(scope.$index)" type="primary" icon="EditPen" />
            <el-button v-else disabled type="default">Processed</el-button>
          </template>
        </el-table-column>
      </el-table>
      <template #footer>
        <OAPagination v-model:page="pagination.page" :total="pagination.total"></OAPagination>
      </template>
    </el-card>
  </OAMain>
</template>
<style scoped></style>