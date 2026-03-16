<script setup name="staffadd">
import { ref, reactive } from 'vue';
import staffHttp from '@/api/staffHttp';
import { useRouter } from 'vue-router';
import OAMain from "@/components/OAMain.vue"
import {useAuthStore} from "@/stores/auth"
import { ElMessage } from 'element-plus';


const router = useRouter();
const authStore = useAuthStore()

// Only the department leader can add new employees to the department.
let staffForm = reactive({
    email: "",
    password: "",
    realname: "",
});
const formRef = ref()
let rules = reactive({
    email: [{required: true, message: "Please enter the email address.", trigger: 'blur'}],
    password: [{required: true, message: "Please enter the password.", trigger: 'blur'}],
    realname: [{required: true, message: "Please enter the real name.", trigger: 'blur'}],
})

const onSubmit = () => {
    formRef.value.validate(async (valid, fields) => {
        if(valid){
            try{
                await staffHttp.addStaff(staffForm.realname, staffForm.email, staffForm.password)
                ElMessage.success('Employee added successfully.')
                router.push({name: 'staff_list'})
            }catch(detail){
                ElMessage.error(detail)
            }
        }
    })
}

</script>

<template>
    <OAMain title="Add Employee">
        <el-card shadow="always">
            <el-form :rules="rules" :model="staffForm" ref="formRef" label-width="120px">
                <el-form-item label="Name" prop="realname">
                    <el-input v-model="staffForm.realname" placeholder="Please enter the name">
                    </el-input>
                </el-form-item>

                <el-form-item label="Email" prop="email">
                    <el-input v-model="staffForm.email" placeholder="Please enter the email"> </el-input>
                </el-form-item>

                <el-form-item label="Password" prop="password">
                    <el-input v-model="staffForm.password" placeholder="Please enter the password" type="password">
                    </el-input>
                </el-form-item>

                <el-form-item label="Department">
                    <el-input readonly disabled placeholder="Department" :value="authStore.user.department.name">
                    </el-input>
                </el-form-item>

                <el-form-item label="Leader">
                    <el-input readonly disabled :placeholder="'[' + authStore.user.email + ']' + authStore.user.realname">
                    </el-input>
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" @click="onSubmit"> Submit </el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </OAMain>
</template>

<style scoped></style>