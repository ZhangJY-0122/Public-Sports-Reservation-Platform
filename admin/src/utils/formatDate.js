/**
 * 日期格式化工具
 */

/**
 * 格式化日期为 YYYY-MM-DD HH:mm:ss 格式
 * @param {Date|string} date - 日期对象或日期字符串
 * @returns {string} 格式化后的日期字符串
 */
export const formatDate = (date) => {
  if (!date) return ''
  
  let d = date
  if (typeof date === 'string') {
    // 处理ISO 8601格式的日期字符串
    d = new Date(date.replace('T', ' ').replace(/\.\d+Z?$/, ''))
  }
  
  if (isNaN(d.getTime())) {
    return ''
  }
  
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  const seconds = String(d.getSeconds()).padStart(2, '0')
  
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

/**
 * 格式化日期为 YYYY-MM-DD 格式
 * @param {Date|string} date - 日期对象或日期字符串
 * @returns {string} 格式化后的日期字符串
 */
export const formatDateShort = (date) => {
  if (!date) return ''
  
  let d = date
  if (typeof date === 'string') {
    d = new Date(date.replace('T', ' ').replace(/\.\d+Z?$/, ''))
  }
  
  if (isNaN(d.getTime())) {
    return ''
  }
  
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  
  return `${year}-${month}-${day}`
}

/**
 * 格式化时间为 HH:mm:ss 格式
 * @param {Date|string} date - 日期对象或日期字符串
 * @returns {string} 格式化后的时间字符串
 */
export const formatTime = (date) => {
  if (!date) return ''
  
  let d = date
  if (typeof date === 'string') {
    d = new Date(date.replace('T', ' ').replace(/\.\d+Z?$/, ''))
  }
  
  if (isNaN(d.getTime())) {
    return ''
  }
  
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  const seconds = String(d.getSeconds()).padStart(2, '0')
  
  return `${hours}:${minutes}:${seconds}`
}

/**
 * 格式化时间为 HH:mm 格式（不显示秒）
 * @param {Date|string} date - 日期对象或日期字符串
 * @returns {string} 格式化后的时间字符串
 */
export const formatTimeShort = (date) => {
  if (!date) return ''
  
  let d = date
  if (typeof date === 'string') {
    d = new Date(date.replace('T', ' ').replace(/\.\d+Z?$/, ''))
  }
  
  if (isNaN(d.getTime())) {
    return ''
  }
  
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  
  return `${hours}:${minutes}`
}

/**
 * 获取相对时间描述（如：2小时前、3天前等）
 * @param {Date|string} date - 日期对象或日期字符串
 * @returns {string} 相对时间描述
 */
export const getRelativeTime = (date) => {
  if (!date) return ''
  
  let d = date
  if (typeof date === 'string') {
    d = new Date(date.replace('T', ' ').replace(/\.\d+Z?$/, ''))
  }
  
  if (isNaN(d.getTime())) {
    return ''
  }
  
  const now = new Date()
  const diff = now.getTime() - d.getTime()
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  const months = Math.floor(days / 30)
  const years = Math.floor(days / 365)
  
  if (years > 0) {
    return `${years}年前`
  } else if (months > 0) {
    return `${months}个月前`
  } else if (days > 0) {
    return `${days}天前`
  } else if (hours > 0) {
    return `${hours}小时前`
  } else if (minutes > 0) {
    return `${minutes}分钟前`
  } else {
    return '刚刚'
  }
}