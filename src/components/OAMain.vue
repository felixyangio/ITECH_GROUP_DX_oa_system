<script setup name="myabsent"> 
import OAPageHeader from "./OAPageHeader.vue";
import {defineProps} from "vue" 

let props = defineProps({
  title: ""
})

</script>

<template>
  <el-space direction="vertical" fill :size="30" style="width: 100%;">
    <OAPageHeader :content="props.title"></OAPageHeader>
    <slot></slot >
  </el-space>
</template>
<style scoped>
.el-space :deep(.el-space__item) {
  width: 100%;
}


</style>