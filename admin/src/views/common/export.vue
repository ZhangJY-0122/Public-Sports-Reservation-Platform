<template>
    <div>
      <el-button @click="exportToExcel">导出 Excel</el-button>
      <el-table :data="items" ref="tableRef">
        <el-table-column prop="name" label="姓名"></el-table-column>
        <el-table-column prop="age" label="年龄"></el-table-column>
        <el-table-column prop="address" label="地址"></el-table-column>
      </el-table>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import * as XLSX from 'xlsx';
  import { saveAs } from 'file-saver';
  
  export default {
    setup() {
      const tableRef = ref(null);
      const items = ref([
        { name: '张三', age: 30, address: '北京市' },
        { name: '李四', age: 25, address: '上海市' },
        { name: '王五', age: 28, address: '广州市' },
      ]);
  
      const exportToExcel = () => {
        // 获取表格数据
        const tableData = items.value;
  
        // 创建列名映射
        const columnMap = {
          name: '姓名',
          age: '年龄',
          address: '地址',
        };
  
        // 转换数据，使列名与数据字段名对应
        const formattedData = tableData.map(item => {
          const formattedItem = {};
          for (const key in item) {
            if (columnMap[key]) {
              formattedItem[columnMap[key]] = item[key];
            }
          }
          return formattedItem;
        });
  
        // 将转换后的数据转换为工作表
        const worksheet = XLSX.utils.json_to_sheet(formattedData);
  
        // 创建一个新的工作簿
        const workbook = XLSX.utils.book_new();
  
        // 将工作表添加到工作簿中
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');
  
        // 生成 Excel 文件的二进制数据
        const excelBuffer = XLSX.write(workbook, {
          bookType: 'xlsx',
          type: 'array',
        });
  
        // 创建 Blob 对象并保存文件
        const data = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        saveAs(data, 'table.xlsx');
      };
  
      return {
        tableRef,
        items,
        exportToExcel,
      };
    },
  };
  </script>