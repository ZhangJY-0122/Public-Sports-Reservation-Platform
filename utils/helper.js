// utils/activityMapper.js
export const transformActivity = item => ({
  title             : item.title,
  description       : item.description,
  activity_type     : item.sportType,
  start_date        : item.startTime,
  end_date          : item.endTime,
  start_time        : (item.startTime || '').split(' ')[1] ?? '14:00',
  end_time          : (item.endTime   || '').split(' ')[1] ?? '16:00',
  location          : item.location,
  max_participants  : Number(item.maxParticipants),
  registration_fee : Number(item.totalFee),
});

// 批量转换
export const mapActivityList = list => list.map(transformActivity);

/*
import { transformActivity, mapActivityList } from '@/utils/activityMapper.js';

// 单条
const one = transformActivity(raw);

// 批量
const newList = mapActivityList(response.list);




*/