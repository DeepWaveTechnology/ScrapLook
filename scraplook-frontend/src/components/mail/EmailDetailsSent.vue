<template>
  <div>
    <h2 class="text-3xl font-bold text-purple-800 mb-6 mt-8 flex items-center gap-2">
      <i class="pi pi-send text-xl" /> Messages envoyés
    </h2>

    <Message v-if="messages.length === 0" severity="info" class="mb-4">
      Aucun message envoyé depuis cette adresse.
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
            <Tag value="Envoyé" severity="success" />
          </div>
        </template>

        <template #content>
          <p class="text-sm text-gray-600 mb-2">
            <i class="pi pi-calendar mr-2" />
            <strong>Envoyé le :</strong> {{ formatDate(message.sentAt) }}
          </p>

          <Divider class="my-2" />

          <div class="text-gray-800 whitespace-pre-line mb-4">
            {{ message.body }}
          </div>

          <p class="text-sm text-gray-700 font-semibold mb-1">
            <i class="pi pi-users mr-2" /> Destinataires :
          </p>
          <ul class="list-disc list-inside text-sm text-gray-700 ml-4">
            <li
              v-for="recipient in message.recipients || []"
              :key="recipient.id"
            >
              {{ recipient.email?.address || "Adresse inconnue" }}
              <span class="text-gray-500">({{ recipient.type || "?" }})</span>
            </li>
          </ul>
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
