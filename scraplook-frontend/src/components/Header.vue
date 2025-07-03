<template>
  <header class="bg-white shadow-md p-4 flex items-center justify-between">
    <div class="text-2xl font-bold text-blue-600">
      <router-link to="/">MonApp</router-link>
    </div>
    <nav class="space-x-4">
      <router-link to="/users" class="text-gray-700 hover:text-blue-500">Utilisateurs</router-link>
    </nav>
  </header>
</template>

<script setup>
// Aucun script spécifique nécessaire pour ce header simple
</script>

<style scoped>
/* Tu peux ajouter des styles personnalisés ici si besoin */
</style>
