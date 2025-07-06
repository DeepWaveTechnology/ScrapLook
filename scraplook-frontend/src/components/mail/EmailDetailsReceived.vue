<template>
  <div>
    <h2 class="text-3xl font-bold text-purple-800 mb-6 mt-8 flex items-center gap-2">
      <i class="pi pi-inbox text-xl" /> Messages reçus
    </h2>

    <Message v-if="messages.length === 0" severity="info" class="mb-4">
      Aucun message reçu pour cette adresse.
    </Message>

    <div v-else class="space-y-6">
      <Card
        v-for="message in messages"
        :key="message.id"
        class="shadow-md border border-gray-200"
      >
        <template #title>
          <div class="flex items-center justify-between">
            <span class="text-xl font-semibold text-gray-800">{{ message.subject }}</span>
            <Tag value="Reçu" severity="info" />
          </div>
        </template>

        <template #content>
          <p class="text-sm text-gray-600 mb-2">
            <i class="pi pi-calendar mr-2" />
            <strong>Reçu le :</strong> {{ formatDate(message.sentAt) }}
          </p>

          <Divider class="my-2" />

          <div class="text-gray-800 whitespace-pre-line mb-4">
            {{ message.body }}
          </div>

          <p class="text-sm text-gray-700">
            <i class="pi pi-user mr-2" />
            <strong>Expéditeur :</strong>
            {{ message.fromEmail?.address || "Adresse inconnue" }}
          </p>
        </template>
      </Card>
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
