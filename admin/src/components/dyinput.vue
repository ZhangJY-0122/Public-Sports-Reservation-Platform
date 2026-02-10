<template>
    <div>
      <el-button type="primary" @click="addInput">添加 Input</el-button>
      <div v-for="(input, index) in inputs" :key="index" class="input-container">
        <el-input
          v-model="input.value"
          :placeholder="placeholder"
          :style="{ width: inputWidth }"
          @input="updateValues"
        ></el-input>
        <el-button type="danger" @click="removeInput(index)">删除</el-button>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, watch } from 'vue';
  
  export default {
    props: {
      placeholder: {
        type: String,
        default: '请输入内容'
      },
      inputWidth: {
        type: String,
        default: '200px'
      },
      modelValue: {
        type: Array,
        default: () => []
      }
    },
    setup(props, { emit }) {
      const inputs = ref([{ value: '' }]);
  
      // 初始化 inputs 数组
      watch(
        () => props.modelValue,
        (newVal) => {
          inputs.value = newVal.map(value => ({ value }));
        },
        { immediate: true }
      );
  
      const addInput = () => {
        inputs.value.push({ value: '' });
      };
  
      const removeInput = (index) => {
        inputs.value.splice(index, 1);
      };
  
      const updateValues = () => {
        emit('update:modelValue', inputs.value.map(input => input.value));
      };
  
      return {
        inputs,
        addInput,
        removeInput,
        updateValues
      };
    }
  };
  </script>
  
  <style scoped>
  .input-container {
    margin: 10px 0;
    display: flex;
    align-items: center;
  }
  </style>
  
