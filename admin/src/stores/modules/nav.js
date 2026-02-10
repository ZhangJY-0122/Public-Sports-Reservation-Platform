import { defineStore } from 'pinia'
import { ref } from 'vue';
export const useNavStore = defineStore('nav',
    //返回的 对象中的属性和方法都会暴露给组件
    () => {
        const nav = ref('')

        const setNav = (v) => {
            // localStorage.setItem('nav', nav)
            nav.value=v


        }

    
        const removeNav = () => {
            // localStorage.removeItem('token')
            nav.value = ''
        }

  

        return {
            nav,
            setNav,
            removeNav,
           
        }
    },
    
        {
            persist: true
        }

)