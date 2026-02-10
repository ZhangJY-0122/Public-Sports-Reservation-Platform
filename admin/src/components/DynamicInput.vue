<template>
    <div class="dynamic-input-container">
        <div v-for="(inputItem, index) in inputList" :key="index" class="input-item">
            <el-input v-model="inputItem.value" :placeholder="placeholder" :style="{ width: inputWidth }" clearable
                @input="handleInputChange(index)" />
            <button @click="removeInput(index)" class="remove-button">
               <el-icon><CloseBold /></el-icon>
            </button>
        </div>
        <button @click="addInput" class="add-button">
            <el-icon style="vertical-align: middle">
                <Plus />
            </el-icon>
            <span style="vertical-align: middle"> 添加 </span>
        </button>
    </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted, getCurrentInstance } from 'vue';
import { ElInput, ElButton, ElMessage } from 'element-plus';

// 接收外部传入的属性
const props = defineProps({
    // 输入框的占位符文本
    placeholder: {
        type: String,
        default: '请输入内容'
    },
    // 输入框的宽度，可自定义，如 '200px'
    inputWidth: {
        type: String,
        default: '150px'
    },
    // 双向绑定的存储输入值的数组
    modelValue: {
        type: Array,
        default: () => []
    }
});

// 定义内部响应式数据
const inputList = ref([]);
const emit = defineEmits(['update:modelValue']);

// 组件挂载时，根据传入的modelValue初始化inputList
onMounted(() => {
    const initValues = props.modelValue.map(value => ({ value: value }));
    inputList.value = initValues.length > 0 ? initValues : [{ value: '' }];
    console.log('inputList 初始化后的值：', inputList.value);
});

// 监听传入的modelValue变化，更新inputList
watch(() => props.modelValue, (newValues) => {
    const initValues = newValues.map(value => ({ value: value }));
    inputList.value = initValues.length > 0 ? initValues : [{ value: '' }];
    console.log('inputList 根据 modelValue 变化更新后的值：', inputList.value);
});

// 添加输入框的函数
const addInput = () => {
    inputList.value.push({ value: '' });
    updateModelValue();
};

// 删除输入框的函数
const removeInput = (index) => {
    if (inputList.value.length > 1) {
        inputList.value.splice(index, 1);
        updateModelValue();
    } else {
        ElMessage({
            message: '至少保留一个输入框',
            type: 'warning',
            showClose: true
        });
    }
};

// 处理输入框内容改变的函数
const handleInputChange = (index) => {
    console.log('输入框内容改变，当前索引为：', index);
    updateModelValue();
};

// 更新modelValue的函数，将inputList中的输入值同步到modelValue
const updateModelValue = () => {
    const inputValues = inputList.value.map(item => item.value);
    emit('update:modelValue', inputValues);
};

// 将内部使用的Element-Plus组件暴露出去，方便外部使用组件时能正确识别
defineExpose({
    ElInput,
    ElButton
});
</script>

<style scoped>
.dynamic-input-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
}

.input-item {
    display: flex;
    align-items: center;
    position: relative;
}

.el-input {
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