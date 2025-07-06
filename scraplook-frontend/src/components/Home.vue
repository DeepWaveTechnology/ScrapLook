<template>
  <div class="flex items-center justify-center h-screen bg-gray-50">
    <Card class="shadow-xl border border-gray-200 w-full max-w-xl text-center">
      <template #title>
        <div class="text-3xl font-bold text-purple-700">
          Bienvenue sur ce gestionnaire de messagerie
        </div>
      </template>
      <template #content>
        <p class="text-gray-600 mt-4 text-lg">
          Utilisez le menu pour créer, envoyer ou consulter vos messages.
        </p>
        <i class="pi pi-envelope mt-6 text-purple-500 text-4xl animate-bounce" />
      </template>
    </Card>
  </div>
</template>

<script setup>
// Rien de spécial ici pour l’instant
</script>
