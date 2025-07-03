<template>
  <div class="p-4">
    <h2 class="text-2xl font-bold mb-4">Liste des utilisateurs</h2>

    <div v-if="loading" class="text-gray-500">Chargement...</div>
    <div v-else-if="error" class="text-red-500">Erreur : {{ error }}</div>
    <ul v-else class="space-y-4">
      <li
        v-for="user in users"
        :key="user.id"
        class="p-4 border rounded shadow hover:bg-gray-50 transition"
      >
        <p class="text-lg font-semibold">{{ user.name }}</p>
        <ul class="pl-4 text-sm text-gray-700">
          <li v-for="email in user.emails" :key="email.id">
            📧 {{ email.address }}
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const users = ref([]);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    const res = await fetch("http://127.0.0.1:8000/user/all");
    if (!res.ok) throw new Error(`Erreur ${res.status}`);
    users.value = await res.json();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
/* Ajoute des styles supplémentaires si besoin */
</style>
