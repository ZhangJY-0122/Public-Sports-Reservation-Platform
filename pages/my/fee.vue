<template>
    <view class="expenses-container">
        <!-- 顶部导航栏 -->
        <view class="header">
            <view class="back-btn" @click="goBack">←</view>
            <text class="header-title">我的费用</text>
            <view class="export-btn" @click="exportData">📊</view>
        </view>

        <!-- 总统计卡片 -->
        <view class="total-stats-section">
            <view class="total-card">
                <view class="total-header">
                    <text class="total-icon">💰</text>
                    <text class="total-title">总支出</text>
                </view>
                <text class="total-amount">¥{{ totalExpenses.toFixed(2) }}</text>
                <text class="total-period">本月</text>
            </view>
        </view>

        <!-- 费用类型标签页 -->
        <view class="expense-tabs">
            <view class="expense-tab" 
                  :class="{ active: selectedExpenseType === 'all' }" 
                  @click="setExpenseType('all')">
                全部费用
            </view>
            <view class="expense-tab" 
                  :class="{ active: selectedExpenseType === 'activity' }" 
                  @click="setExpenseType('activity')">
                活动费用
            </view>
            <view class="expense-tab" 
                  :class="{ active: selectedExpenseType === 'coaching' }" 
                  @click="setExpenseType('coaching')">
                教练费用
            </view>
            <view class="expense-tab" 
                  :class="{ active: selectedExpenseType === 'sharing' }" 
                  @click="setExpenseType('sharing')">
                平摊费用
            </view>
        </view>

        <!-- 月份筛选 -->
        <view class="month-filter">
            <view class="month-selector" @click="showMonthPicker">
                <text class="month-label">📅 {{ currentMonth }}</text>
                <text class="month-dropdown">▼</text>
            </view>
        </view>

        <!-- 费用统计图 -->
        <view class="chart-section" v-if="filteredExpenses.length > 0">
            <text class="chart-title">费用分布</text>
            <view class="chart-container">
                <view class="chart-bar" v-for="category in expenseChart" :key="category.name" @click="viewCategoryDetails(category)">
                    <view class="chart-bar-container">
                        <view class="chart-bar-fill" :style="{ width: category.percentage + '%', backgroundColor: category.color }"></view>
                    </view>
                    <text class="chart-label">{{ category.name }}</text>
                    <text class="chart-value">¥{{ category.amount.toFixed(2) }}</text>
                </view>
            </view>
        </view>

        <!-- 费用列表 -->
        <scroll-view class="expenses-list" scroll-y="true">
            <view class="expense-item" v-for="expense in filteredExpenses" :key="expense.id">
                <view class="expense-header">
                    <view class="expense-icon">
                        <text class="icon-emoji">{{ expense.icon }}</text>
                    </view>
                    <view class="expense-info">
                        <text class="expense-title">{{ expense.title }}</text>
                        <text class="expense-type">{{ expense.category }}</text>
                        <text class="expense-date">{{ expense.date }}</text>
                    </view>
                    <view class="expense-amount">
                        <text class="amount-value" :class="expense.type">{{ expense.type === 'payment' ? '-' : '+' }}¥{{ expense.amount.toFixed(2) }}</text>
                        <text class="payment-method">{{ expense.paymentMethod }}</text>
                    </view>
                </view>

                <view class="expense-details" v-if="expense.description">
                    <text class="detail-label">📝 详情</text>
                    <text class="detail-value">{{ expense.description }}</text>
                </view>

                <view class="expense-actions">
                    <view class="action-btn" @click="viewReceipt(expense)">
                        查看票据
                    </view>
                    <view class="action-btn" @click="shareExpense(expense)">
                        分享费用
                    </view>
                    <view class="action-btn refund" v-if="expense.canRefund" @click="requestRefund(expense)">
                        申请退款
                    </view>
                </view>
            </view>

            <!-- 空状态 -->
            <view class="empty-state" v-if="filteredExpenses.length === 0">
                <text class="empty-icon">💰</text>
                <text class="empty-text">暂无{{ getCurrentTypeText() }}记录</text>
                <text class="empty-subtext">快去参加活动，创造美好回忆！</text>
            </view>
        </scroll-view>

        <!-- 快捷操作浮动按钮 -->
        <view class="floating-btn" @click="showQuickActions">
            <text class="btn-text">💳</text>
        </view>

        <!-- 月份选择器 -->
        <view class="modal-overlay" v-if="showMonthModal" @click="hideMonthPicker">
            <view class="modal-content" @click.stop>
                <view class="modal-header">
                    <text class="modal-title">选择月份</text>
                    <view class="close-btn" @click="hideMonthPicker">×</view>
                </view>
                <scroll-view class="month-list" scroll-y="true">
                    <view class="month-item" 
                          v-for="month in availableMonths" 
                          :key="month.value" 
                          :class="{ selected: month.value === currentMonthValue }"
                          @click="selectMonth(month.value)">
                        <text class="month-name">{{ month.label }}</text>
                        <text class="month-amount">¥{{ month.amount.toFixed(2) }}</text>
                    </view>
                </scroll-view>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    name: 'MyExpensesPage',
    data() {
        return {
            selectedExpenseType: 'all',
            currentMonth: '2024年1月',
            currentMonthValue: '2024-01',
            showMonthModal: false,
            
            expensesList: [
                // 活动费用
                {
                    id: 1,
                    title: '篮球训练营',
                    category: '活动费用',
                    icon: '🏀',
                    amount: 280.00,
                    type: 'payment',
                    date: '2024-01-20',
                    time: '14:30',
                    paymentMethod: '微信支付',
                    description: '包含场地费、器材费、教练指导费',
                    canRefund: true,
                    receipt: '篮球训练营_20240120_280.pdf'
                },
                {
                    id: 2,
                    title: '游泳会员卡',
                    category: '活动费用',
                    icon: '🏊‍♂️',
                    amount: 1200.00,
                    type: 'payment',
                    date: '2024-01-15',
                    time: '10:20',
                    paymentMethod: '支付宝',
                    description: '月度游泳会员卡，包含所有泳池使用',
                    canRefund: false,
                    receipt: '游泳会员卡_20240115_1200.pdf'
                },
                {
                    id: 3,
                    title: '羽毛球场地费',
                    category: '活动费用',
                    icon: '🏸',
                    amount: 45.00,
                    type: 'payment',
                    date: '2024-01-18',
                    time: '16:45',
                    paymentMethod: '现金',
                    description: '2小时场地费用',
                    canRefund: true,
                    receipt: '羽毛球场地费_20240118_45.pdf'
                },
                
                // 教练费用
                {
                    id: 4,
                    title: '私人教练课程',
                    category: '教练费用',
                    icon: '👨‍🏫',
                    amount: 300.00,
                    type: 'payment',
                    date: '2024-01-19',
                    time: '09:00',
                    paymentMethod: '银行卡',
                    description: '1小时一对一私人教练指导',
                    canRefund: true,
                    receipt: '私人教练课程_20240119_300.pdf'
                },
                {
                    id: 5,
                    title: '瑜伽课程',
                    category: '教练费用',
                    icon: '🧘‍♀️',
                    amount: 80.00,
                    type: 'payment',
                    date: '2024-01-21',
                    time: '19:30',
                    paymentMethod: '微信支付',
                    description: '团体瑜伽课程',
                    canRefund: false,
                    receipt: '瑜伽课程_20240121_80.pdf'
                },
                
                // 平摊费用
                {
                    id: 6,
                    title: '篮球赛平摊费用',
                    category: '平摊费用',
                    icon: '🤝',
                    amount: 25.00,
                    type: 'payment',
                    date: '2024-01-17',
                    time: '18:20',
                    paymentMethod: '微信群转账',
                    description: '篮球友谊赛场地和器材费用',
                    canRefund: false,
                    receipt: '篮球赛平摊费用_20240117_25.pdf'
                },
                {
                    id: 7,
                    title: '聚餐AA费用',
                    category: '平摊费用',
                    icon: '🍽️',
                    amount: 68.50,
                    type: 'payment',
                    date: '2024-01-16',
                    time: '20:15',
                    paymentMethod: '支付宝',
                    description: '运动后聚餐，6人平摊',
                    canRefund: false,
                    receipt: '聚餐AA费用_20240116_68.5.pdf'
                },
                {
                    id: 8,
                    title: '交通费用返还',
                    category: '平摊费用',
                    icon: '🚗',
                    amount: 15.00,
                    type: 'refund',
                    date: '2024-01-14',
                    time: '13:30',
                    paymentMethod: '微信转账',
                    description: '去程交通费用返还',
                    canRefund: false,
                    receipt: ''
                },
                
                // 其他月份的费用
                {
                    id: 9,
                    title: '健身房年卡',
                    category: '活动费用',
                    icon: '🏋️‍♂️',
                    amount: 2880.00,
                    type: 'payment',
                    date: '2023-12-15',
                    time: '14:20',
                    paymentMethod: '银行卡',
                    description: '年度健身卡，包含所有器械和课程',
                    canRefund: false,
                    receipt: '健身房年卡_20231215_2880.pdf'
                }
            ],
            
            availableMonths: [
                { label: '2024年1月', value: '2024-01', amount: 1593.50 },
                { label: '2023年12月', value: '2023-12', amount: 3168.50 },
                { label: '2023年11月', value: '2023-11', amount: 1245.80 },
                { label: '2023年10月', value: '2023-10', amount: 2156.30 },
                { label: '2023年9月', value: '2023-09', amount: 987.60 }
            ]
        }
    },
    computed: {
        totalExpenses() {
            const currentYearMonth = this.currentMonthValue
            return this.expensesList
                .filter(expense => expense.date.startsWith(currentYearMonth))
                .reduce((total, expense) => {
                    return total + (expense.type === 'payment' ? expense.amount : -expense.amount)
                }, 0)
        },
        
        filteredExpenses() {
            let filtered = this.expensesList.filter(expense => 
                expense.date.startsWith(this.currentMonthValue)
            )
            
            if (this.selectedExpenseType !== 'all') {
                const typeMap = {
                    'activity': '活动费用',
                    'coaching': '教练费用',
                    'sharing': '平摊费用'
                }
                
                filtered = filtered.filter(expense => expense.category === typeMap[this.selectedExpenseType])
            }
            
            return filtered.sort((a, b) => new Date(b.date + ' ' + b.time) - new Date(a.date + ' ' + a.time))
        },
        
        expenseChart() {
            const currentYearMonth = this.currentMonthValue
            let filtered = this.expensesList.filter(expense => 
                expense.date.startsWith(currentYearMonth) && expense.type === 'payment'
            )
            
            if (this.selectedExpenseType !== 'all') {
                const typeMap = {
                    'activity': '活动费用',
                    'coaching': '教练费用',
                    'sharing': '平摊费用'
                }
                
                filtered = filtered.filter(expense => expense.category === typeMap[this.selectedExpenseType])
            }
            
            const categories = {}
            filtered.forEach(expense => {
                if (!categories[expense.category]) {
                    categories[expense.category] = 0
                }
                categories[expense.category] += expense.amount
            })
            
            const total = Object.values(categories).reduce((sum, amount) => sum + amount, 0)
            const colors = {
                '活动费用': '#ff6b35',
                '教练费用': '#4a90e2', 
                '平摊费用': '#28a745'
            }
            
            return Object.keys(categories).map(category => ({
                name: category,
                amount: categories[category],
                percentage: total > 0 ? (categories[category] / total * 100).toFixed(1) : 0,
                color: colors[category] || '#999'
            }))
        }
    },
    methods: {
        goBack() {
            uni.navigateBack()
        },
        
        setExpenseType(type) {
            this.selectedExpenseType = type
        },
        
        getCurrentTypeText() {
            switch (this.selectedExpenseType) {
                case 'activity': return '活动费用'
                case 'coaching': return '教练费用'
                case 'sharing': return '平摊费用'
                default: return '费用'
            }
        },
        
        showMonthPicker() {
            this.showMonthModal = true
        },
        
        hideMonthPicker() {
            this.showMonthModal = false
        },
        
        selectMonth(monthValue) {
            this.currentMonthValue = monthValue
            
            const monthObj = this.availableMonths.find(m => m.value === monthValue)
            if (monthObj) {
                this.currentMonth = monthObj.label
            }
            
            this.hideMonthPicker()
        },
        
        viewReceipt(expense) {
            if (expense.receipt) {
                uni.showModal({
                    title: '查看票据',
                    content: `票据文件：${expense.receipt}\n\n是否要下载查看？`,
                    success: (res) => {
                        if (res.confirm) {
                            uni.showToast({
                                title: '票据下载中...',
                                icon: 'loading'
                            })
                            
                            setTimeout(() => {
                                uni.showToast({
                                    title: '票据已保存到相册',
                                    icon: 'success'
                                })
                            }, 1500)
                        }
                    }
                })
            } else {
                uni.showModal({
                    title: '提示',
                    content: '该费用暂无票据信息',
                    showCancel: false
                })
            }
        },
        
        shareExpense(expense) {
            const shareText = `💰 费用分享\n\n项目：${expense.title}\n类别：${expense.category}\n金额：¥${expense.amount.toFixed(2)}\n日期：${expense.date}\n\n#运动消费记录`
            
            uni.showModal({
                title: '分享费用',
                content: shareText,
                confirmText: '复制文本',
                success: (res) => {
                    if (res.confirm) {
                        // 复制到剪贴板
                        uni.setClipboardData({
                            data: shareText,
                            success: () => {
                                uni.showToast({
                                    title: '已复制到剪贴板',
                                    icon: 'success'
                                })
                            }
                        })
                    }
                }
            })
        },
        
        requestRefund(expense) {
            uni.showModal({
                title: '申请退款',
                content: `确定要为"${expense.title}"申请退款吗？\n退款金额：¥${expense.amount.toFixed(2)}`,
                success: (res) => {
                    if (res.confirm) {
                        uni.showToast({
                            title: '退款申请已提交',
                            icon: 'success'
                        })
                        
                        // 模拟添加退款记录
                        const refundExpense = {
                            ...expense,
                            id: expense.id + 1000,
                            type: 'refund',
                            title: `${expense.title}-退款`,
                            canRefund: false
                        }
                        
                        this.expensesList.unshift(refundExpense)
                    }
                }
            })
        },
        
        viewCategoryDetails(category) {
            const categoryExpenses = this.filteredExpenses.filter(expense => 
                expense.category === category.name && expense.type === 'payment'
            )
            
            const detailText = `📊 ${category.name}详情\n\n总额：¥${category.amount.toFixed(2)}\n笔数：${categoryExpenses.length}笔\n占比：${category.percentage}%\n\n最近消费：${categoryExpenses[categoryExpenses.length - 1]?.title || '无'}`
            
            uni.showModal({
                title: category.name,
                content: detailText,
                showCancel: false
            })
        },
        
        exportData() {
            const exportData = {
                month: this.currentMonth,
                totalExpenses: this.totalExpenses,
                categories: this.expenseChart,
                details: this.filteredExpenses.map(expense => ({
                    title: expense.title,
                    amount: expense.amount,
                    category: expense.category,
                    date: expense.date,
                    paymentMethod: expense.paymentMethod
                }))
            }
            
            uni.showModal({
                title: '导出数据',
                content: `确定要导出${this.currentMonth}的费用数据吗？\n包含${this.filteredExpenses.length}条记录`,
                success: (res) => {
                    if (res.confirm) {
                        uni.showToast({
                            title: '数据导出中...',
                            icon: 'loading'
                        })
                        
                        setTimeout(() => {
                            uni.showToast({
                                title: '数据已导出',
                                icon: 'success'
                            })
                        }, 2000)
                    }
                }
            })
        },
        
        showQuickActions() {
            uni.showActionSheet({
                itemList: ['查看优惠券', '添加费用', '联系客服', '设置提醒'],
                success: (res) => {
                    const actions = ['查看优惠券', '添加费用', '联系客服', '设置提醒']
                    uni.showToast({
                        title: actions[res.tapIndex],
                        icon: 'none'
                    })
                }
            })
        }
    }
}
</script>

<style scoped>
.expenses-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* 顶部导航栏 */
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20rpx 30rpx;
    background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
    color: #fff;
}

.back-btn,
.export-btn {
    width: 80rpx;
    height: 80rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    font-size: 36rpx;
}

.header-title {
    font-size: 36rpx;
    font-weight: bold;
}

/* 总统计卡片 */
.total-stats-section {
    padding: 30rpx;
}

.total-card {
    background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
    border-radius: 20rpx;
    padding: 40rpx 30rpx;
    color: #fff;
    text-align: center;
    box-shadow: 0 8rpx 25rpx rgba(40, 167, 69, 0.3);
}

.total-header {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20rpx;
}

.total-icon {
    font-size: 48rpx;
    margin-right: 15rpx;
}

.total-title {
    font-size: 32rpx;
    font-weight: bold;
}

.total-amount {
    font-size: 72rpx;
    font-weight: bold;
    display: block;
    margin-bottom: 10rpx;
}

.total-period {
    font-size: 26rpx;
    opacity: 0.9;
}

/* 费用类型标签页 */
.expense-tabs {
    display: flex;
    background: #fff;
    padding: 20rpx 30rpx;
    border-bottom: 1px solid #e1e8ed;
}

.expense-tab {
    flex: 1;
    text-align: center;
    padding: 15rpx 0;
    background: #f8f9fa;
    color: #666;
    border-radius: 25rpx;
    font-size: 26rpx;
    margin: 0 3rpx;
    border: 2rpx solid transparent;
}

.expense-tab.active {
    background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
    color: #fff;
}

/* 月份筛选 */
.month-filter {
    background: #fff;
    padding: 20rpx 30rpx;
    border-bottom: 1px solid #e1e8ed;
}

.month-selector {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 15rpx 20rpx;
    background: #f8f9fa;
    border-radius: 25rpx;
    border: 2rpx solid #e1e8ed;
}

.month-label {
    font-size: 28rpx;
    color: #333;
    font-weight: bold;
    margin-right: 10rpx;
}

.month-dropdown {
    font-size: 20rpx;
    color: #666;
}

/* 费用统计图 */
.chart-section {
    background: #fff;
    margin: 20rpx 30rpx;
    padding: 30rpx;
    border-radius: 20rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
}

.chart-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 30rpx;
}

.chart-container {
    display: flex;
    flex-direction: column;
    gap: 20rpx;
}

.chart-bar {
    display: flex;
    align-items: center;
    gap: 20rpx;
}

.chart-bar-container {
    flex: 1;
    height: 30rpx;
    background: #f1f3f4;
    border-radius: 15rpx;
    overflow: hidden;
}

.chart-bar-fill {
    height: 100%;
    border-radius: 15rpx;
    transition: width 0.3s ease;
}

.chart-label {
    width: 150rpx;
    font-size: 28rpx;
    color: #333;
    font-weight: 500;
}

.chart-value {
    width: 150rpx;
    text-align: right;
    font-size: 28rpx;
    color: #333;
    font-weight: bold;
}

/* 费用列表 */
.expenses-list {
    flex: 1;
    padding: 20rpx 30rpx;
    height: calc(100vh - 500rpx);
}

.expense-item {
    background: #fff;
    border-radius: 20rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
}

.expense-header {
    display: flex;
    align-items: flex-start;
    margin-bottom: 20rpx;
}

.expense-icon {
    margin-right: 20rpx;
}

.icon-emoji {
    font-size: 50rpx;
    display: block;
}

.expense-info {
    flex: 1;
}

.expense-title {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 8rpx;
}

.expense-type {
    font-size: 24rpx;
    color: #28a745;
    display: block;
    margin-bottom: 8rpx;
}

.expense-date {
    font-size: 22rpx;
    color: #999;
    display: block;
}

.expense-amount {
    text-align: right;
}

.amount-value {
    font-size: 32rpx;
    font-weight: bold;
    display: block;
    margin-bottom: 8rpx;
}

.amount-value.payment {
    color: #dc3545;
}

.amount-value.refund {
    color: #28a745;
}

.payment-method {
    font-size: 22rpx;
    color: #666;
    display: block;
}

.expense-details {
    margin-bottom: 20rpx;
    padding: 20rpx;
    background: #f8f9fa;
    border-radius: 15rpx;
}

.detail-label {
    font-size: 24rpx;
    color: #999;
    margin-bottom: 10rpx;
    display: block;
}

.detail-value {
    font-size: 26rpx;
    color: #333;
    line-height: 1.5;
}

.expense-actions {
    display: flex;
    gap: 15rpx;
}

.action-btn {
    flex: 1;
    text-align: center;
    padding: 15rpx 0;
    border-radius: 25rpx;
    font-size: 26rpx;
    background: #f8f9fa;
    color: #666;
    border: 2rpx solid #e1e8ed;
}

.action-btn.refund {
    background: #fff3cd;
    color: #856404;
    border-color: #ffeaa7;
}

/* 空状态 */
.empty-state {
    text-align: center;
    padding: 100rpx 30rpx;
}

.empty-icon {
    font-size: 120rpx;
    display: block;
    margin-bottom: 30rpx;
}

.empty-text {
    font-size: 32rpx;
    color: #333;
    display: block;
    margin-bottom: 15rpx;
}

.empty-subtext {
    font-size: 26rpx;
    color: #666;
    display: block;
}

/* 浮动按钮 */
.floating-btn {
    position: fixed;
    bottom: 120rpx;
    right: 40rpx;
    width: 120rpx;
    height: 120rpx;
    background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
    color: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8rpx 25rpx rgba(40, 167, 69, 0.3);
    z-index: 1000;
}

.btn-text {
    font-size: 50rpx;
}

/* 月份选择器模态框 */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 2000;
    display: flex;
    align-items: center;
    justify-content: center;
}

.modal-content {
    background: #fff;
    border-radius: 20rpx;
    margin: 40rpx;
    max-height: 600rpx;
    width: calc(100% - 80rpx);
    box-shadow: 0 8rpx 30rpx rgba(0, 0, 0, 0.3);
}

.modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 30rpx;
    border-bottom: 1px solid #e1e8ed;
}

.modal-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
}

.close-btn {
    width: 60rpx;
    height: 60rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f8f9fa;
    border-radius: 50%;
    font-size: 40rpx;
    color: #666;
}

.month-list {
    max-height: 400rpx;
}

.month-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 25rpx 30rpx;
    border-bottom: 1px solid #f1f3f4;
}

.month-item.selected {
    background: #f0f9ff;
}

.month-name {
    font-size: 28rpx;
    color: #333;
    font-weight: 500;
}

.month-amount {
    font-size: 28rpx;
    color: #28a745;
    font-weight: bold;
}

/* 点击效果 */
.back-btn:active,
.export-btn:active,
.expense-tab:active,
.action-btn:active,
.floating-btn:active,
.month-selector:active,
.close-btn:active,
.month-item:active {
    transform: scale(0.95);
}
</style>