<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">
      Messages envoyés depuis cette adresse
    </h1>

    <div v-if="loading" class="flex justify-center mt-12">
      <ProgressSpinner style="width: 60px; height: 60px" />
    </div>

    <Message v-else-if="error" severity="error" class="p-4 mb-4">
      {{ error }}
    </Message>

    <div v-else-if="emailData">
      <p class="text-lg text-purple-700 mb-4">
        Adresse email : <strong>{{ emailData.address }}</strong>
      </p>

      <div v-if="emailData.sentMessages.length === 0" class="text-gray-500">
        Aucun message envoyé.
      </div>

      <div v-else class="space-y-6">
        <div
          v-for="message in emailData.sentMessages"
          :key="message.id"
          class="p-4 border border-gray-300 rounded-md bg-white shadow-sm"
        >
          <h2 class="text-xl font-semibold mb-2">{{ message.subject }}</h2>
          <p class="mb-1 text-sm text-gray-600">
            <strong>Envoyé le :</strong> {{ formatDate(message.sentAt) }}
          </p>
          <div class="whitespace-pre-line mb-2">{{ message.body }}</div>

          <h3 class="font-semibold text-sm">Destinataires :</h3>
          <ul class="list-disc list-inside text-sm text-gray-700">
            <li v-for="recipient in message.recipients" :key="recipient.id">
              {{ recipient.email }} ({{ recipient.type }})
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import ProgressSpinner from "primevue/progressspinner";
import Message from "primevue/message";

const route = useRoute();
const emailId = route.params.emailId;
console.log("Email ID from route:", emailId);
const emailData = ref(null);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    const res = await fetch(
      `http://127.0.0.1:8000/messages/sent_messages?id_email_address=${emailId}`
    );
    console.log("response:", res);  
    if (!res.ok) throw new Error(`Erreur ${res.status}`);
    const data = await res.json();
    console.log("data:", data);
    emailData.value =
      Array.isArray(data) && data.length > 0
        ? data[0]
        : { address: "", sentMessages: [] };
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});

function formatDate(dateString) {
  const d = new Date(dateString);
  return d.toLocaleString();
}
</script>
