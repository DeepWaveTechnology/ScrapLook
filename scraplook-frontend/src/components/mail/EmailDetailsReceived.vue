<template>
  <div>
    <h2 class="text-2xl font-semibold mb-4 mt-8">Messages reçus</h2>
    <div v-if="messages.length === 0" class="text-gray-500">
      Aucun message reçu.
    </div>

    <div v-else class="space-y-6">
      <div
        v-for="message in messages"
        :key="message.id"
        class="p-4 border border-gray-300 rounded-md bg-white shadow-sm"
      >
        <h3 class="text-xl font-semibold mb-2">{{ message.subject }}</h3>
        <p class="mb-1 text-sm text-gray-600">
          <strong>Reçu le :</strong> {{ formatDate(message.sentAt) }}
        </p>
        <div class="whitespace-pre-line mb-2">{{ message.body }}</div>

        <h4 class="font-semibold text-sm">Expéditeur :</h4>
        <p class="text-sm text-gray-700">
          {{ message.fromEmail?.address || "Adresse inconnue" }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  messages: {
    type: Array,
    required: true,
  },
});

function formatDate(dateString) {
  const d = new Date(dateString);
  return isNaN(d.getTime()) ? "Date invalide" : d.toLocaleString();
}
</script>
