import { createPinia } from 'pinia'
//
// 引入pinia-plugin-persistedstate插件
import persist from 'pinia-plugin-persistedstate'

const pinia=createPinia()
pinia.use(persist)
export default pinia


export * from './modules/user'
export * from './modules/nav'

