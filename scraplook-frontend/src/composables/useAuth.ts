import { ref, computed } from 'vue'

const token = ref(localStorage.getItem('access_token') || null)
const userName = ref(localStorage.getItem('user_name') || '')

export function useAuth() {
  const isLoggedIn = computed(() => !!token.value)

  function login(newToken, name) {
    token.value = newToken
    userName.value = name
    localStorage.setItem('access_token', newToken)
    localStorage.setItem('user_name', name)
  }

  function logout() {
    token.value = null
    userName.value = ''
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_name')
  }

  return {
    token,
    userName,
    isLoggedIn,
    login,
    logout,
  }
}
