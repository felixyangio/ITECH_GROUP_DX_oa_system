<script setup name="publishinform">
import OAMain from '@/components/OAMain.vue';
import { ref, reactive, onBeforeUnmount, shallowRef, onMounted } from "vue"
import '@wangeditor/editor/dist/css/style.css' 
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import staffHttp from '@/api/staffHttp';
import { ElMessage } from "element-plus"
import { useAuthStore } from '@/stores/auth';
import informHttp from '@/api/informHttp';
import { i18nChangeLanguage } from '@wangeditor/editor'

i18nChangeLanguage('en')

const authStore = useAuthStore()

let informForm = reactive({
  title: '',
  content: '',
  department_ids: []
})
const rules = reactive({
  title: [{ required: true, message: "Please enter the title.", trigger: 'blur' }],
  content: [{ required: true, message: "Please enter the content.", trigger: 'blur' }],
  department_ids: [{ required: true, message: "Please select a department.", trigger: 'change' }]
})
let formRef = ref()
let formLabelWidth = "200px"
let departments = ref([])

////////////// wangEditor //////////////
const editorRef = shallowRef()

console.log(import.meta.env)

const toolbarConfig = {}
const editorConfig = {
  placeholder: "Please enter content...",

  MENU_CONF: {
    uploadImage: {
      server: `${import.meta.env.VITE_BASE_URL}/image/upload`,
      // 'http://127.0.0.1:8000/image/upload',
      fieldName: 'image',
      maxFileSize: 0.5 * 1024 * 1024,
      maxNumberOfFiles: 10,
      allowedFileTypes: ['image/*'],
      headers: {
        Authorization: "JWT " + authStore.token
      },
      timeout: 6 * 1000, // 6 s,

      customInsert(res, insertFn) {
        if (res.errno == 0) {
          // let data = res.data;
          const data = res.data[0]
          let url = import.meta.env.VITE_BASE_URL + data.url
          let href = import.meta.env.VITE_BASE_URL + data.href
          let alt = data.alt;
          // Get url, alt, and href from response and insert the image
          insertFn(url, alt, href)
        } else {
          ElMessage.error(res.message)
        }
      },
      // Triggered when a single file upload fails
      onFailed(file, res) {
        console.log(`${file.name} upload failed`, res)
      },
      // Triggered when upload error occurs or timeout happens
      onError(file, err, res) {
        if (file.size > 0.5 * 1024 * 1024) {
          ElMessage.error('Image size cannot exceed 0.5MB.')
        } else {
          ElMessage.error('Invalid image format.')
        }
      },
    }
  }
}
// editorConfig.MENU_CONF['uploadImage']
let mode = "default"


onBeforeUnmount(() => {
  const editor = editorRef.value
  if (editor == null) return
  editor.destroy()
})

const handleCreated = (editor) => {
  editorRef.value = editor // Store the editor instance
}
////////////// wangEditor //////////////

onMounted(async () => {
  try {
    let data = await staffHttp.getAllDepartment()
    departments.value = data.results
  } catch (detail) {
    ElMessage.error(detail)
  }
})

const onSubmit = () => {
  formRef.value.validate(async (valid, fields) => {
    if (valid) {
      console.log(informForm);
      try {
        let data = await informHttp.publishInform(informForm)
        console.log(data);
      } catch (detail) {
        ElMessage.error(detail)
      }
    }
  })
}

</script>

<template>
  <OAMain title="Publish Notification">
    <el-card>
      <el-form :model="informForm" :rules="rules" ref="formRef">
        <el-form-item label="Title" :label-width="formLabelWidth" prop="title">
          <el-input v-model="informForm.title" autocomplete="off" />
        </el-form-item>
        <el-form-item label="Visible Departments" :label-width="formLabelWidth" prop="department_ids">
          <el-select multiple v-model="informForm.department_ids">
            <el-option :value="0" label="All Departments"></el-option>
            <el-option v-for="department in departments" :label="department.name" :value="department.id"
              :key="department.name" />
          </el-select>
        </el-form-item>
        <el-form-item label="Content" :label-width="formLabelWidth" prop="content">
          <div style="border: 1px solid #ccc; width: 100%;">
            <Toolbar style="border-bottom: 1px solid #ccc" :editor="editorRef" :defaultConfig="toolbarConfig"
              :mode="mode" />
            <Editor style="height: 500px; overflow-y: hidden;" v-model="informForm.content"
              :defaultConfig="editorConfig" :mode="mode" @onCreated="handleCreated" />
          </div>
        </el-form-item>
        <el-form-item>
          <div style="text-align: right; flex: 1;">
            <el-button type="primary" @click="onSubmit">Publish</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </OAMain>
</template>

<style scoped></style>