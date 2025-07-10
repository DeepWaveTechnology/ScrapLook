import axios from "axios";
import {useAuth} from "@/composables/useAuth";
import { BACKEND_URL } from '@/config'

const api = axios.create({
  baseURL: BACKEND_URL,
})

api.interceptors.request.use(
  (config) => {
      const { isLoggedIn, token } = useAuth();

    console.log(isLoggedIn.value)
    if (isLoggedIn.value) {
      config.headers.Authorization = `Bearer ${token.value}`
        console.log('Token set in request header:', token.value)
        console.log(isLoggedIn.value)
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default api