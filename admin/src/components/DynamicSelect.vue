<template>
  <div class="dynamic-select-container">
    <div v-for="(selectItem, index) in selectList" :key="index" class="select-item">
      <el-select
        v-model="selectItem.selectedValue"
        :placeholder="placeholder"
        :style="{ width: selectWidth }"
        @change="handleSelectChange(index)"
      >
        <el-option
          v-for="option in options"
          :key="option.value"
          :label="option.label"
          :value="option.value"
        ></el-option>
      </el-select>
      <button @click="removeSelect(index)" class="remove-button">
     <el-icon><CloseBold /></el-icon>
      </button>
    </div>
    <button @click="addSelect" class="add-button">
      <i class="el-icon-plus"></i> 添加选择框
    </button>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue';
import { ElSelect, ElOption, ElButton, ElMessage } from 'element-plus';

// 接收外部传入的属性
const props = defineProps({
  // 选择框的占位符文本
  placeholder: {
    type: String,
    default: '请选择'
  },
  // 选择框的宽度，可自定义，如 '200px'
  selectWidth: {
    type: String,
    default: '150px'
  },
  // 选择框的数据源，是包含label和value属性的对象数组
  options: {
    type: Array,
    default: () => []
  },
  // 双向绑定的存储选择值的数组
  modelValue: {
    type: Array,
    default: () => []
  }
});

// 定义内部响应式数据
const selectList = ref([]);
const emit = defineEmits(['update:modelValue']);

// 组件挂载时，根据传入的modelValue初始化selectList
onMounted(() => {
  const initValues = props.modelValue.map(value => ({ selectedValue: value }));
    if (initValues.length === 0 && props.options.length > 0) {
        initValues.push({ selectedValue: props.options[0].value });
    }
    selectList.value = initValues.length > 0? initValues : [ { selectedValue: '' } ];
    // 新增逻辑，判断如果有传入的modelValue，设置第一个选择框显示其第一个值
    if (props.modelValue.length > 0) {
        selectList.value[0].selectedValue = props.modelValue[0];
    }
});

// 监听传入的modelValue变化，更新selectList
watch(() => props.modelValue, (newValues) => {
  const initValues = newValues.map(value => ({ selectedValue: value }));
    if (initValues.length === 0 && props.options.length > 0) {
        // 如果外部传入的modelValue为空，但options有数据，取options第一个元素的value作为默认值
        initValues.push({ selectedValue: props.options[0].value });
    }
    selectList.value = initValues.length > 0? initValues : [ { selectedValue: '' } ];
    // 新增逻辑，确保显示第一个选择的值（如果有合适的传入值）
    if (newValues.length > 0) {
        selectList.value[0].selectedValue = newValues[0];
    }
});

// 添加选择框的函数
const addSelect = () => {
  selectList.value.push({ selectedValue: '' });
  updateModelValue();
};

// 删除选择框的函数
const removeSelect = (index) => {
  if (selectList.value.length > 1) {
    selectList.value.splice(index, 1);
    updateModelValue();
  } else {
    ElMessage({
      message: '至少保留一个选择框',
      type: 'warning',
      showClose: true
    });
  }
};

// 处理选择框值改变的函数
const handleSelectChange = (index) => {
  updateModelValue();
};

// 更新modelValue的函数，将selectList中的选择值同步到modelValue
const updateModelValue = () => {
  const selectedValues = selectList.value.map(item => item.selectedValue);
  emit('update:modelValue', selectedValues);
};

// 将内部使用的Element-Plus组件暴露出去，方便外部使用组件时能正确识别
defineExpose({
  ElSelect,
  ElOption,
  ElButton
});
</script>

<style scoped>
.dynamic-select-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.select-item {
  display: flex;
  align-items: center;
  position: relative;
}

.el-select {
  margin-right: 5px;
}

.remove-button {
  position: absolute;
  right: -25px;
  top: 50%;
  transform: translateY(-50%);
  background-color: transparent;
  border: none;
  color: #ccc;
  cursor: pointer;
}

.add-button {
  margin-top: 10px;
  background-color: #409EFF;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  cursor: pointer;
}

.add-button:hover {
  background-color: #66b1ff;
}
</style>