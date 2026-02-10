import { defineStore } from 'pinia'
import { ref } from 'vue';
export const useUserStore = defineStore('user',
    () => {
        const token = ref('')
        const userInfo = ref({})
        const checkdata= ref({})
        const setToken = (newtoken) => {
            // localStorage.setItem('token', token)
            token.value=newtoken

             
            // token.value = token

        }

    
        const removeToken = () => {
            // localStorage.removeItem('token')
            token.value = ''
        }

        const setUserInfo = (newUserInfo) => {
            userInfo.value = newUserInfo
        }
        const removeUserInfo = () => {
            userInfo.value = {}
        }

        const setCheckData = (newCheckData) => {
            checkdata.value = newCheckData
        }
        const removeCheckData = () => {
            checkdata.value = {}
        }

        return {
            token,
            setToken,
            removeToken,
            userInfo,
            setUserInfo,
            removeUserInfo,
            checkdata,
            setCheckData,
            removeCheckData
        }
    },
    
        {
            persist: true
        }

)