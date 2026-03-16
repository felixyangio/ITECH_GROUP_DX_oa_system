# OA System — 项目启动文档

## 项目概览

本项目为前后端分离的企业 OA 办公系统：

| 层级 | 技术栈 | 目录 |
|------|--------|------|
| 前端 | Vue 3 + Vite + Element Plus + Pinia | `src/` |
| 后端 | Django 6 + Django REST Framework + JWT | `oaback/` |
| 数据库 | SQLite3（开发环境） | `oaback/db.sqlite3` |

---

## 环境要求

| 工具 | 推荐版本 |
|------|---------|
| Python | 3.10+ |
| Node.js | 18+ |
| npm | 9+ |

---

## 一、后端启动

### 1. 创建并激活虚拟环境

```bash
# 在项目根目录下
python -m venv venv

# Windows 激活
venv\Scripts\activate
```

### 2. 安装依赖

```bash
pip install -r oaback/requirements.txt
```

主要依赖：

```
Django==6.0.3
djangorestframework==3.16.1
djangorestframework_simplejwt==5.5.1
django-cors-headers==4.9.0
pillow==12.1.1
```

### 3. 数据库迁移

```bash
cd oaback
python manage.py migrate
```

### 4. 创建超级管理员（首次部署）

```bash
python manage.py createsuperuser
```

### 5. 启动后端开发服务

```bash
python manage.py runserver
```

后端默认运行于：`http://127.0.0.1:8000`

管理后台地址：`http://127.0.0.1:8000/admin`

---

## 二、前端启动

### 1. 安装依赖

```bash
# 在项目根目录下（src/ 所在目录）
npm install
```

### 2. 环境变量配置

开发环境配置文件：`.env.development`

```env
VITE_BASE_URL=http://127.0.0.1:8000
VITE_APP_TITLE="OA System"
```

> 若后端端口有变动，修改 `VITE_BASE_URL` 即可。

### 3. 启动前端开发服务

```bash
npm run dev
```

前端默认运行于：`http://localhost:5173`

---

## 三、初始数据配置（首次使用）

进入 Django 管理后台 `http://127.0.0.1:8000/admin`，按以下顺序操作：

1. **新建部门**：STAFF → Department → Add
   - 示例：`Tech`、`Marketing`

2. **注册员工**：在前端 Employee List 页面点击 Add，或通过管理后台 STAFF → Staff 手动创建

3. **为员工绑定部门**：STAFF → Staff → 编辑对应员工，设置所属部门

---

## 四、API 路由一览

| 模块 | 前缀 | 说明 |
|------|------|------|
| 认证 | `/auth/` | 登录、修改密码 |
| 员工 | `/staff/` | 部门管理、员工 CRUD |
| 公告 | `/inform/` | 发布、列表、详情、阅读记录 |
| 请假 | `/absent/` | 请假申请与审批 |
| 首页 | `/home/` | 数据统计 |

---

## 五、员工状态说明

| 值 | 含义 | 前端显示 |
|----|------|---------|
| `1` | Active（正常） | 绿色 |
| `0` | Inactive（停用） | 黄色 |
| `3` | Locked（锁定） | 红色 |

---

## 六、JWT 认证说明

- 请求头格式：`Authorization: JWT <token>`
- Access Token 有效期：**1 天**
- Refresh Token 有效期：**7 天**
- Token 存储于浏览器 `localStorage`

---

## 七、常见问题

**Q：前端请求报 CORS 错误？**
确认后端已运行在 `http://127.0.0.1:8000`，且 `.env.development` 中 `VITE_BASE_URL` 与之一致。

**Q：登录后页面空白 / 员工列表无数据？**
检查该登录用户是否已在 Django Admin 中关联了 Staff 记录，并设置了所属部门。

**Q：发布公告后列表无数据？**
确认已执行所有数据库迁移（`python manage.py migrate`），`inform_inform_departments` 关联表需存在。

**Q：部门下拉框为空？**
确认已在 Django Admin 的 STAFF → Department 中至少添加一个部门。
