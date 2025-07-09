<template>
  <Menubar :model="menuItems" class="bg-white shadow-md px-10" style="height: 80px; font-size: 1.25rem; font-weight: 600;">
    <template #end>
      <div class="flex items-center gap-4">
        <div v-if="isLoggedIn" class="text-gray-700">
          Connecté en tant que <strong>{{ userName }}</strong>
        </div>
        <button
          v-if="isLoggedIn"
          @click="handleLogout"
          class="p-button p-component p-button-text"
          type="button"
        >
          <span class="p-button-icon pi pi-sign-out"></span>
          <span class="p-button-label">Déconnexion</span>
        </button>
        <button
          v-else
          @click="goLogin"
          class="p-button p-component p-button-text"
          type="button"
        >
          <span class="p-button-icon pi pi-sign-in"></span>
          <span class="p-button-label">Connexion</span>
        </button>
      </div>
    </template>
  </Menubar>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import Menubar from 'primevue/menubar'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const { token, userName, isLoggedIn, logout } = useAuth()

const menuItems = [
  {
    label: 'MonApp',
    icon: 'pi pi-home',
    command: () => router.push('/'),
    class: 'text-blue-600 text-3xl font-bold'
  },
  {
    label: 'Utilisateurs',
    icon: 'pi pi-users',
    command: () => router.push('/users'),
    class: 'text-lg'
  },
]

function goLogin() {
  router.push('/login')
}

function handleLogout() {
  logout()
  router.push('/')
}
</script>

<style scoped>
.p-button-text {
  color: #5a5a5a;
  border: none;
  background: none;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.p-button-text:hover {
  color: #3f51b5;
}
</style>
