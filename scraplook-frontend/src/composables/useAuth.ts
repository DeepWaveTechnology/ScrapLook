import { ref, computed } from 'vue';

const token = ref(localStorage.getItem('access_token') || null);
const refreshToken = ref(localStorage.getItem('refresh_token') || null);
const userName = ref(localStorage.getItem('user_name') || '');

export function useAuth() {
  const isLoggedIn = computed(() => !!token.value);

  function login(userAccessToken: string, userRefreshToken: string, name: string) {
    token.value = userAccessToken;
    refreshToken.value = userRefreshToken;
    userName.value = name;
    localStorage.setItem('access_token', userAccessToken);
    localStorage.setItem('refresh_token', userRefreshToken);
    localStorage.setItem('user_name', name);
  }

  function logout() {
    token.value = null;
    userName.value = '';
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_name');
  }

  function saveAccessToken(newAccessToken: string): void {
    localStorage.removeItem('access_token');
    token.value = newAccessToken;
    localStorage.setItem('access_token', newAccessToken);
  }

  return {
    token,
    refreshToken,
    userName,
    isLoggedIn,
    login,
    logout,
    saveAccessToken
  }
}
