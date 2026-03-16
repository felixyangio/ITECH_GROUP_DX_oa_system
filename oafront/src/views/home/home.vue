<script setup name="home">
import { ref, reactive, onMounted } from "vue"
import { ElMessage } from "element-plus"
import timeFormatter from "@/utils/timeFormatter";
import OAMain from "@/components/OAMain.vue"
import homeHttp from "@/api/homeHttp";
import * as echarts from 'echarts';

let informs = ref([])
let absents = ref([])

onMounted(async () => {
    try {
        informs.value = await homeHttp.getLatestInforms()
        absents.value = await homeHttp.getLatestAbsents()

        let rows = await homeHttp.getDepartmentStaffCount()
        console.log(rows);
        let xdatas = []
        let ydatas = []
        for (let row of rows) {
            xdatas.push(row.name)
            ydatas.push(row.staff_count)
        }

        var myChart = echarts.init(document.getElementById('department-staff-count'));

        myChart.setOption({
            tooltip: {},
            xAxis: {
                data: xdatas
            },
            yAxis: {},
            series: [
                {
                    name: 'Department Staff Count',
                    type: 'bar',
                    data: ydatas
                }
            ]
        });
    } catch (detail) {
        ElMessage.error(detail)
    }


})

</script>

<template>
    <OAMain title="Home">
        <el-card>
            <template #header>
                <h2>Department Staff Count</h2>
            </template>
            <div id="department-staff-count" style="width: 100%;height:300px;"></div>
        </el-card>

        <el-row :gutter="20">
            <el-col :span="12">
                <el-card>
                    <template #header>
                        <h2>Latest Notifications</h2>
                    </template>
                    <el-table :data="informs">
                        <el-table-column label="Title">
                            <template #default="scope">
                                <router-link :to="{ name: 'inform_detail', params: { pk: scope.row.id } }">{{ scope.row.title
                                    }}</router-link>
                            </template>
                        </el-table-column>
                        <el-table-column label="Auther" prop="author.realname"></el-table-column>
                        <el-table-column label="Published Time">
                            <template #default="scope">
                                {{ timeFormatter.stringFromDate(scope.row.create_time) }}
                            </template>
                        </el-table-column>
                        <el-table-column label="Read Status">
                            <template #default="scope">
                                <el-tag v-if="scope.row.reads.length > 0">Read</el-tag>
                                <el-tag v-else type="danger">Unread</el-tag>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-card>
            </el-col>
            <el-col :span="12">
                <el-card>
                    <template #header>
                        <h2>Latest Leave Requests</h2>
                    </template>
                    <el-table :data="absents">
                        <el-table-column label="Department" prop="requester.department.name"></el-table-column>
                        <el-table-column label="Requester" prop="requester.realname"></el-table-column>
                        <el-table-column label="Start Date" prop="start_date"></el-table-column>
                        <el-table-column label="End Date" prop="end_date"></el-table-column>
                        <el-table-column label="Request Time">
                            <template #default="scope">
                                {{ timeFormatter.stringFromDateTime(scope.row.create_time) }}
                            </template>
                        </el-table-column>
                    </el-table>
                </el-card>
            </el-col>
        </el-row>
    </OAMain>
</template>

<style scoped></style>