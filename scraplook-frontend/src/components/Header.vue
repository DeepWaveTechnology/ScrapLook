<template>
  <Menubar
    :model="items"
    class="bg-white shadow-md px-10"
    style="height: 80px; font-size: 1.25rem; font-weight: 600;"
  />
</template>

<script setup>
import { ref } from 'vue'
import Menubar from 'primevue/menubar'
import { useRouter } from 'vue-router'
const router = useRouter()

const items = ref([
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
])
</script>

<style scoped>
</style>
