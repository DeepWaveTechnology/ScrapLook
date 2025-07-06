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
        v-for="message in localMessages"
        :key="message.id"
        class="shadow-md border border-gray-200"
      >
        <template #title>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <!-- Bouton delete -->
              <Button
                icon="pi pi-trash"
                class="p-button-text p-button-danger"
                @click="deleteMessage(message.id)"
                :aria-label="'Supprimer le message ' + message.subject"
                :loading="deletingId === message.id"
              />
              <span class="text-xl font-semibold text-gray-800">{{ message.subject }}</span>
            </div>
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
import { ref, watch } from "vue";

const props = defineProps({
  messages: {
    type: Array,
    required: true,
  },
  idEmailAddress: {
    type: String,
    required: true,
  },
});

const localMessages = ref([...props.messages]);
const deletingId = ref(null);

watch(
  () => props.messages,
  (newMessages) => {
    localMessages.value = [...newMessages];
  }
);

async function deleteMessage(messageId) {
  if (!confirm("Voulez-vous vraiment supprimer ce message ?")) return;

  deletingId.value = messageId;

  try {
    const id_email_address = props.idEmailAddress;

    const params = new URLSearchParams({
      id_email_address,
      id_message: messageId,
    });

    const res = await fetch(`http://127.0.0.1:8000/messages/?${params.toString()}`, {
      method: "DELETE",
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail?.[0]?.msg || `Erreur ${res.status}`);
    }

    localMessages.value = localMessages.value.filter((m) => m.id !== messageId);
  } catch (err) {
    alert("Erreur lors de la suppression : " + err.message);
  } finally {
    deletingId.value = null;
  }
}

function formatDate(dateString) {
  const d = new Date(dateString);
  return isNaN(d.getTime()) ? "Date invalide" : d.toLocaleString();
}

</script>
