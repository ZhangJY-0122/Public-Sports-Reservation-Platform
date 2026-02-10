<template>
  <div class="business-analysis-container">
    <div class="page-header">
      <h2>场馆营业分析</h2>
      <div class="header-actions">
        <el-button type="primary" @click="refreshData">
          <el-icon><Refresh /></el-icon> 刷新数据
        </el-button>
      </div>
    </div>

    <!-- 统计卡片区域 -->
    <div class="stats-cards">
      <el-card shadow="hover" class="stat-card">
        <div class="stat-icon income-icon">
          <el-icon><Wallet /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-title">总收入</div>
          <div class="stat-value">¥{{ totalIncome.toFixed(2) }}</div>
        </div>
      </el-card>
      <el-card shadow="hover" class="stat-card">
        <div class="stat-icon booking-icon">
          <el-icon><Ticket /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-title">总预约数</div>
          <div class="stat-value">{{ totalBookings }}</div>
        </div>
      </el-card>
      <el-card shadow="hover" class="stat-card">
        <div class="stat-icon average-icon">
          <el-icon><TrendCharts /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-title">平均预约金额</div>
          <div class="stat-value">¥{{ averageAmount.toFixed(2) }}</div>
        </div>
      </el-card>
    </div>

    <!-- 图表区域 -->
    <div class="charts-container">
      <!-- 月度收入趋势图 -->
      <el-card shadow="hover" class="chart-card">
        <template #header>
          <div class="card-header">
            <span>月度收入趋势</span>
          </div>
        </template>
        <div class="chart-content">
          <div ref="monthlyIncomeChart" class="chart"></div>
        </div>
      </el-card>

      <!-- 场馆收入排名图 -->
      <el-card shadow="hover" class="chart-card">
        <template #header>
          <div class="card-header">
            <span>场馆收入排名</span>
          </div>
        </template>
        <div class="chart-content">
          <div ref="venueRankChart" class="chart"></div>
        </div>
      </el-card>

      <!-- 收入来源分布图 -->
      <el-card shadow="hover" class="chart-card pie-chart-card">
        <template #header>
          <div class="card-header">
            <span>收入来源分布</span>
          </div>
        </template>
        <div class="chart-content">
          <div ref="incomeSourceChart" class="chart"></div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import { Refresh, Wallet, Ticket, TrendCharts } from '@element-plus/icons-vue'
import bookingApi from '../../api/booking'

// 响应式数据
const monthlyIncomeChart = ref(null)
const venueRankChart = ref(null)
const incomeSourceChart = ref(null)
const loading = ref(false)

// 统计数据
const totalIncome = ref(0)
const totalBookings = ref(0)
const averageAmount = ref(0)

// 图表实例
let monthlyChart = null
let venueChart = null
let sourceChart = null

// 初始化月度收入趋势图
const initMonthlyIncomeChart = () => {
  if (monthlyIncomeChart.value) {
    monthlyChart = echarts.init(monthlyIncomeChart.value)
    const option = {
      tooltip: {
        trigger: 'axis',
        formatter: '{b}<br/>收入: ¥{c}'
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: [],
        axisLabel: {
          interval: 0,
          rotate: 30
        }
      },
      yAxis: {
        type: 'value',
        name: '收入 (元)',
        axisLabel: {
          formatter: '¥{value}'
        }
      },
      series: [
        {
          data: [],
          type: 'line',
          smooth: true,
          lineStyle: {
            width: 3,
            color: '#1677ff'
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {
                offset: 0,
                color: 'rgba(22, 119, 255, 0.3)'
              },
              {
                offset: 1,
                color: 'rgba(22, 119, 255, 0.05)'
              }
            ])
          },
          itemStyle: {
            color: '#1677ff'
          }
        }
      ]
    }
    monthlyChart.setOption(option)
  }
}

// 初始化场馆收入排名图
const initVenueRankChart = () => {
  if (venueRankChart.value) {
    venueChart = echarts.init(venueRankChart.value)
    const option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        formatter: '{b}<br/>收入: ¥{c}'
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'value',
        name: '收入 (元)',
        axisLabel: {
          formatter: '¥{value}'
        }
      },
      yAxis: {
        type: 'category',
        data: [],
        axisLabel: {
          interval: 0,
          rotate: 0
        }
      },
      series: [
        {
          data: [],
          type: 'bar',
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              {
                offset: 0,
                color: '#4096ff'
              },
              {
                offset: 1,
                color: '#1677ff'
              }
            ])
          }
        }
      ]
    }
    venueChart.setOption(option)
  }
}

// 初始化收入来源分布图
const initIncomeSourceChart = () => {
  if (incomeSourceChart.value) {
    sourceChart = echarts.init(incomeSourceChart.value)
    const option = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: ¥{c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 'left',
        top: 'center'
      },
      series: [
        {
          name: '收入来源',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: true,
            formatter: '{b}\n{d}%'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: '16',
              fontWeight: 'bold'
            }
          },
          data: []
        }
      ]
    }
    sourceChart.setOption(option)
  }
}

// 更新图表数据
const updateCharts = (data) => {
  // 更新月度收入趋势图
  if (monthlyChart) {
    const months = data.monthly_income.map(item => item.month)
    const incomeData = data.monthly_income.map(item => item.income)
    
    monthlyChart.setOption({
      xAxis: {
        data: months
      },
      series: [
        {
          data: incomeData
        }
      ]
    })
  }
  
  // 更新场馆收入排名图
  if (venueChart) {
    const venues = data.venue_income_rank.map(item => item.venue_name).reverse()
    const venueIncomes = data.venue_income_rank.map(item => item.total_income).reverse()
    
    venueChart.setOption({
      yAxis: {
        data: venues
      },
      series: [
        {
          data: venueIncomes
        }
      ]
    })
  }
  
  // 更新收入来源分布图
  if (sourceChart) {
    const sourceData = data.income_source_distribution.map(item => ({
      name: item.source,
      value: item.amount
    }))
    
    sourceChart.setOption({
      series: [
        {
          data: sourceData
        }
      ]
    })
  }
  
  // 更新统计数据
  totalIncome.value = data.total_statistics.total_income
  totalBookings.value = data.total_statistics.total_bookings
  averageAmount.value = data.total_statistics.average_booking_amount
}

// 获取营业分析数据
const fetchBusinessAnalysis = async () => {
  loading.value = true
  try {
    const response = await bookingApi.getBusinessAnalysis()
    if (response.code === 0 && response.data) {
      updateCharts(response.data)
    }
  } catch (error) {
    console.error('获取营业分析数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 刷新数据
const refreshData = () => {
  fetchBusinessAnalysis()
}

// 响应式调整图表大小
const handleResize = () => {
  monthlyChart?.resize()
  venueChart?.resize()
  sourceChart?.resize()
}

// 生命周期钩子
onMounted(() => {
  initMonthlyIncomeChart()
  initVenueRankChart()
  initIncomeSourceChart()
  fetchBusinessAnalysis()
  window.addEventListener('resize', handleResize)
})

// 组件卸载时清理
onMounted(() => {
  return () => {
    window.removeEventListener('resize', handleResize)
    monthlyChart?.dispose()
    venueChart?.dispose()
    sourceChart?.dispose()
  }
})
</script>

<style scoped lang="scss">
.business-analysis-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  
  h2 {
    margin: 0;
    font-size: 20px;
    font-weight: 600;
  }
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  transition: all 0.3s ease;
  cursor: pointer;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12) !important;
  }
  
  .stat-icon {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 20px;
    font-size: 24px;
    
    &.income-icon {
      background-color: rgba(22, 119, 255, 0.1);
      color: #1677ff;
    }
    
    &.booking-icon {
      background-color: rgba(82, 196, 26, 0.1);
      color: #52c41a;
    }
    
    &.average-icon {
      background-color: rgba(247, 149, 33, 0.1);
      color: #f79521;
    }
  }
  
  .stat-info {
    flex: 1;
  }
  
  .stat-title {
    font-size: 14px;
    color: #606266;
    margin-bottom: 8px;
  }
  
  .stat-value {
    font-size: 24px;
    font-weight: 600;
    color: #303133;
  }
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.chart-card {
  transition: all 0.3s ease;
  
  &:hover {
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12) !important;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 600;
    font-size: 16px;
  }
  
  .chart-content {
    padding: 10px 0;
  }
  
  .chart {
    width: 100%;
    height: 300px;
  }
}

.pie-chart-card {
  grid-column: span 1;
}

@media (max-width: 768px) {
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .charts-container {
    grid-template-columns: 1fr;
  }
  
  .chart {
    height: 250px;
  }
}
</style>