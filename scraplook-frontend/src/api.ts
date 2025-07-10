import axios from "axios";
import {useAuth} from "@/composables/useAuth";
import { BACKEND_URL } from '@/config'

const api = axios.create({
  baseURL: BACKEND_URL,
})

api.interceptors.request.use(
  (config) => {
      const { isLoggedIn, token } = useAuth();

    if (isLoggedIn.value) {
      config.headers.Authorization = `Bearer ${token.value}`
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default api