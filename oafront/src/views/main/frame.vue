<script setup name="frame">
import { ref, computed, reactive, onMounted } from "vue"
import {
    Expand,
    Fold
} from '@element-plus/icons-vue'
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import authHttp from "@/api/authHttp";
import { ElMessage } from "element-plus";
import routes from "@/router/frame"

const authStore = useAuthStore()
const router = useRouter()



let displayUser = reactive({
    department: {},
    realname: ""
})
let defaultActive = ref("home")
let isCollapse = ref(false);
let dialogVisible = ref(false)
let formLabelWidth = "100px"
let resetPwdForm = reactive({
    oldpwd: '',
    pwd1: '',
    pwd2: ''
})
let formTag = ref()
let rules = reactive({
    oldpwd: [
        { required: true, message: 'Please enter the old password.', trigger: 'blur' },
        { min: 6, max: 20, message: 'Password length must be between 6 and 20 characters.！', trigger: 'blur' },
    ],
    pwd1: [
        { required: true, message: 'Please enter the new password.', trigger: 'blur' },
        { min: 6, max: 20, message: 'Password length must be between 6 and 20 characters.', trigger: 'blur' },
    ],
    pwd2: [
        { required: true, message: 'Please confirm the password.', trigger: 'blur' },
        { min: 6, max: 20, message: 'Password length must be between 6 and 20 characters.', trigger: 'blur' },
    ]
})
let asideWidth = computed(() => {
    if (isCollapse.value) {
        return "64px"
    } else {
        return "250px"
    }
})

onMounted(() => {
    defaultActive.value = router.currentRoute.value.name
    displayUser.department = authStore.user.department
    displayUser.realname = authStore.user.realname
})

const onCollapseAside = () => {
    isCollapse.value = !isCollapse.value
}

const onExit = () => {
    authStore.clearUserToken();
    router.push({ name: 'login' })
}

const onControlResetPwdDialog = () => {
    resetPwdForm.oldpwd = ""
    resetPwdForm.pwd1 = ""
    resetPwdForm.pwd2 = ""
    dialogVisible.value = true;
}

const onSubmit = () => {
    formTag.value.validate(async (valid, fields) => {
        if (valid) {
            try {
                await authHttp.resetPwd(resetPwdForm.oldpwd, resetPwdForm.pwd1, resetPwdForm.pwd2)
                ElMessage.success("Password updated successfully.")
                dialogVisible.value = false;
            } catch (detail) {
                ElMessage.error(detail)
            }
        } else {
            ElMessage.info('Please fill in the required fields.')
        }
    })
}

</script>

<template>
    <el-container class="container">
        <el-aside class="aside" :width="asideWidth">
            <router-link to="/" class="brand"><strong>OA</strong><span v-show="!isCollapse">SYSTEM</span></router-link>
            <el-menu :router="true" active-text-color="#ffd04b" background-color="#343a40" class="el-menu-vertical-demo"
                :default-active="defaultActive" text-color="#fff" :collapse="isCollapse" :collapse-transition="false">
                <template v-for="route in routes[0].children">
                    <template v-if="authStore.has_permission(route.meta.permissions, route.meta.opt)">
                        <el-menu-item v-if="!route.children" :index="route.name" :route="{ name: route.name }">
                            <el-icon>
                                <component :is="route.meta.icon"></component>
                            </el-icon>
                            <span>{{ route.meta.text }}</span>
                        </el-menu-item>

                        <el-sub-menu v-else :index="route.name">
                            <template #title>
                                <el-icon>
                                    <component :is="route.meta.icon"></component>
                                </el-icon>
                                <span>{{ route.meta.text }}</span>
                            </template>
                            <template v-for="child in route.children">
                                <template v-if="authStore.has_permission(child.meta.permissions, child.meta.opt)">
                                    <el-menu-item v-if="!child.meta.hidden" :index="child.name"
                                        :route="{ name: child.name }">
                                        <el-icon>
                                            <component :is="child.meta.icon"></component>
                                        </el-icon>
                                        <span>{{ child.meta.text }}</span>
                                    </el-menu-item>
                                </template>
                            </template>
                        </el-sub-menu>
                    </template>
                </template>
            </el-menu>
        </el-aside>
        <el-container>
            <el-header class="header">
                <div class="left-header">
                    <el-button v-show="isCollapse" :icon="Expand" @click="onCollapseAside" />
                    <el-button v-show="!isCollapse" :icon="Fold" @click="onCollapseAside" />
                </div>
                <el-dropdown>
                    <span class="el-dropdown-link">
                        <el-avatar :size="30" icon="UserFilled" />
                        <span style="margin-left: 10px;">[{{ displayUser.department.name }}]{{
                            displayUser.realname
                            }}</span>
                        <el-icon class="el-icon--right">
                            <arrow-down />
                        </el-icon>
                    </span>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item @click="onControlResetPwdDialog">Change Password</el-dropdown-item>
                            <el-dropdown-item divided @click="onExit">Log Out</el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </el-header>
            <el-main class="main">
                <RouterView></RouterView>
            </el-main>
        </el-container>
    </el-container>
    <el-dialog v-model="dialogVisible" title="Change Password" width="500">
        <el-form :model="resetPwdForm" :rules="rules" ref="formTag">
            <el-form-item label="Old Password" :label-width="formLabelWidth" prop="oldpwd">
                <el-input v-model="resetPwdForm.oldpwd" autocomplete="off" type="password" />
            </el-form-item>

            <el-form-item label="New Password" :label-width="formLabelWidth" prop="pwd1">
                <el-input v-model="resetPwdForm.pwd1" autocomplete="off" type="password" />
            </el-form-item>

            <el-form-item label="Confirm Password" :label-width="formLabelWidth" prop="pwd2">
                <el-input v-model="resetPwdForm.pwd2" autocomplete="off" type="password" />
            </el-form-item>

        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="dialogVisible = false">Cancel</el-button>
                <el-button type="primary" @click="onSubmit">
                    Confirm
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>


<!-- <style scoped>
.container {
  height: 100vh;
  background-color: #f4f6f9;
}

.aside {
  background-color: #343a40;
  box-shadow: 0 14px 28px rgba(0, 0, 0, .25), 0 10px 10px rgba(0, 0, 0, .22) !important;
}

.aside .brand {
  color: #fff;
  text-decoration: none;
  border-bottom: 1px solid #434a50;
  background-color: #232631;
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
}

.header {
  height: 60px;
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.el-dropdown-link {
  display: flex;
  align-items: center;
}

.el-menu {
  border-right: none;
}
</style> -->
<style scoped>
/* ===============================
Container
=============================== */

.container {
  height: 100vh;
  position: relative;
  overflow: hidden;

  background:
    radial-gradient(circle at 15% 20%, rgba(120,150,255,.18), transparent 40%),
    radial-gradient(circle at 85% 70%, rgba(180,200,255,.22), transparent 45%),
    linear-gradient(180deg,#f8fafc,#eef2f7);
}


/* ===============================
Sidebar
=============================== */

.aside {

  background: linear-gradient(
    180deg,
    #ffffff,
    #f1f5f9
  );

  border-right: 1px solid rgba(0,0,0,.06);

  box-shadow: 6px 0 20px rgba(0,0,0,.06);

}


/* ===============================
Brand
=============================== */

.aside .brand {

  height: 64px;

  display: flex;

  align-items: center;

  justify-content: center;

  font-size: 20px;

  font-weight: 600;

  letter-spacing: 1px;

  color: #111827;

  border-bottom: 1px solid rgba(0,0,0,.05);

  background: linear-gradient(
    135deg,
    #ffffff,
    #f1f5f9
  );

}

.brand-sub {
  margin-left: 6px;
  color: #6b7280;
}


/* ===============================
Menu
=============================== */

:deep(.el-menu) {
  background: transparent !important;
  border-right: none;
}


/* menu item */

:deep(.el-menu-item) {

  height: 52px;

  font-size: 14px;

  font-weight: 500;

  color: #374151 !important;

  border-radius: 10px;

  margin: 4px 10px;

  transition: all .25s;

}


/* hover */

:deep(.el-menu-item:hover) {

  background: #f5f8ff !important;

  transform: translateX(3px);

  color: #111827 !important;

}


/* active indicator */

:deep(.el-menu-item.is-active) {

  background: #eef3ff !important;

  color: #2563eb !important;

  font-weight: 600;

  border-left: 4px solid #2563eb;

  padding-left: 16px;

  box-shadow: 0 0 6px rgba(37,99,235,.25);

}


/* submenu */

:deep(.el-sub-menu__title) {

  color: #374151 !important;

  font-weight: 500;

  border-radius: 10px;

  margin: 4px 10px;

  transition: .2s;

}


:deep(.el-sub-menu__title:hover) {

  background: #f5f8ff !important;

}


/* submenu items */

:deep(.el-sub-menu .el-menu-item) {

  color: #4b5563 !important;

}


/* ===============================
Header (Glass Effect)
=============================== */

.header {

  height: 64px;

  background: rgba(255,255,255,.75);

  backdrop-filter: blur(18px);

  border-bottom: 1px solid rgba(0,0,0,.05);

  display: flex;

  align-items: center;

  justify-content: space-between;

  padding: 0 24px;

  box-shadow: 0 4px 16px rgba(0,0,0,.04);

}


.left-header {

  display: flex;

  align-items: center;

}


/* ===============================
Search
=============================== */

.global-search {

  margin-left: 20px;

  width: 260px;

}

.global-search :deep(.el-input__wrapper) {

  border-radius: 10px;

  background: #f8fafc;

  border: 1px solid rgba(0,0,0,.05);

}


/* ===============================
Breadcrumb
=============================== */

.breadcrumb {

  margin-bottom: 20px;

  font-size: 14px;

  color: #6b7280;

}


/* ===============================
Main Content
=============================== */

.main {

  padding: 28px;

  overflow: auto;

}


/* card */

.main :deep(.el-card),
.main :deep(.el-table) {

  background: white;

  border-radius: 14px;

  border: 1px solid rgba(0,0,0,.05);

  box-shadow: 0 12px 30px rgba(0,0,0,.08);

}


/* ===============================
Table
=============================== */

:deep(.el-table th) {

  color: #111827;

  font-weight: 600;

  background: #f8fafc;

}

:deep(.el-table td) {

  color: #374151;

}


/* row hover */

:deep(.el-table__row:hover) {

  background: #f1f5ff !important;

}


/* ===============================
Buttons
=============================== */

:deep(.el-button--primary) {

  background: linear-gradient(
    135deg,
    #3b82f6,
    #2563eb
  );

  border: none;

  box-shadow: 0 6px 16px rgba(37,99,235,.3);

  transition: .2s;

}


:deep(.el-button--primary:hover) {

  transform: translateY(-2px);

  box-shadow: 0 10px 22px rgba(37,99,235,.35);

}


/* ===============================
Welcome Card
=============================== */

.welcome-card {

  margin-bottom: 20px;

  border-radius: 16px;

  background: linear-gradient(
    135deg,
    #ffffff,
    #f5f8ff
  );

  border: 1px solid rgba(0,0,0,.05);

  box-shadow: 0 10px 28px rgba(0,0,0,.08);

}


.welcome-card h2 {

  font-size: 20px;

  color: #111827;

  margin-bottom: 6px;

}

.welcome-card p {

  color: #6b7280;

  font-size: 14px;

}
</style>