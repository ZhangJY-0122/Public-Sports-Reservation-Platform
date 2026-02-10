  export function changeDate(val){
    var date = new Date(val);
    var timestamp = date.getTime();
    //转化为字符串

    var date = new Date(timestamp);
    var year = date.getFullYear();
    var month = ("0" + (date.getMonth() + 1)).slice(-2);
    var day = ("0" + date.getDate()).slice(-2);
    var formattedDate = year + "-" + month + "-" + day;
    console.log(formattedDate);
    return formattedDate

}

/**
 * 将数字转换为中文货币格式
 * @param {number} num - 需要转换的数字
 * @returns {string} - 转换后的中文货币字符串
 */
export function convertToChineseCurrency(num) {
  const chineseNum = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖'];
  const units = ['', '拾', '佰', '仟'];
  const bigUnits = ['', '万', '亿', '万亿'];
  let integerPart = Math.floor(num);
  let fractionPart = Math.round((num - integerPart) * 100);
  let integerChinese = '';
  let fractionChinese = '';
  // 处理整数部分
  if (integerPart === 0) {
      integerChinese = '零';
  } else {
      let groupIndex = 0;
      let group = '';
      while (integerPart > 0) {
          let temp = '';
          for (let i = 0; i < 4 && integerPart > 0; i++) {
              let digit = integerPart % 10;
              integerPart = Math.floor(integerPart / 10);
              if (digit === 0) {
                  if (temp.length > 0 && temp[temp.length - 1]!== chineseNum[0]) {
                      temp = chineseNum[0]+temp;
                  }
              } else {
                  temp = chineseNum[digit]+units[i]+temp;
              }
          }
          if (temp.length > 0) {
              group = temp + bigUnits[groupIndex]+group;
          }
          groupIndex++;
      }
      integerChinese = group;
  }
  // 处理小数部分
  if (fractionPart === 0) {
      fractionChinese = '整';
  } else {
      fractionChinese = chineseNum[Math.floor(fractionPart / 10)] + '角';
      if (fractionPart % 10!== 0) {
          fractionChinese += chineseNum[fractionPart % 10] + '分';
      }
  }
  if (fractionChinese === '整') {
      return integerChinese + '元整';
  } else {
      return integerChinese + '元' + fractionChinese;
  }
}



export function getYearStartAndEnd() {
    let year=new Date().getFullYear()
    const start = new Date(year, 0, 1); // 当年的第一天
    const end = new Date(year, 11, 31); // 当年的最后一天
    return { start, end };
  }
  
  // 获取当月的第一天和最后一天
 export function getMonthStartAndEnd() {
    const year=new Date().getFullYear()
    const month=new Date().getMonth()

    const start = new Date(year, month, 1); // 当月的第一天
    const end = new Date(year, month + 1, 0); // 下月的前一天，即当月的最后一天
    return { start, end };
  }


//  获取本周的第一天和最后一天
 export function getWeekStartAndEnd() {
    const today = new Date();
    const dayOfWeek = today.getDay(); // 0 表示周日，1 表示周一，以此类推
    const startOfWeek = new Date(today);
    startOfWeek.setDate(today.getDate() - dayOfWeek + 1); // 本周第一天
    const endOfWeek = new Date(today);
    endOfWeek.setDate(today.getDate() + (6 - dayOfWeek)); // 本周最后一天
    return { startOfWeek, endOfWeek };
  }


