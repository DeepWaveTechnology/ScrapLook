<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">
      Détails de l'adresse email
    </h1>

    <div v-if="loading" class="flex justify-center mt-12">
      <ProgressSpinner style="width: 60px; height: 60px" />
    </div>

    <Message v-else-if="error" severity="error" class="p-4 mb-4">
      {{ error }}
    </Message>

    <div v-else>
      <p class="text-lg text-purple-700 mb-4">
        Adresse email : <strong>{{ address || 'Inconnue' }}</strong>
      </p>

      <EmailDetailsSent :messages="sentMessages" />
      <EmailDetailsReceived :messages="receivedMessages" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import ProgressSpinner from "primevue/progressspinner";
import Message from "primevue/message";
import EmailDetailsSent from "./EmailDetailsSent.vue";
import EmailDetailsReceived from "./EmailDetailsReceived.vue";

const route = useRoute();
const emailId = route.params.emailId;

const address = ref("Adresse inconnue");
const sentMessages = ref([]);
const receivedMessages = ref([]);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    const resSent = await fetch(
      `http://127.0.0.1:8000/messages/sent_messages?id_email_address=${emailId}`
    );
    if (!resSent.ok) throw new Error(`Erreur ${resSent.status}`);
    const dataSent = await resSent.json();
    sentMessages.value = Array.isArray(dataSent) ? dataSent : [];
    address.value = dataSent[0]?.fromEmail?.address || "Adresse inconnue";

    const resReceived = await fetch(
      `http://127.0.0.1:8000/messages/received_messages?id_email_address=${emailId}`
    );
    if (!resReceived.ok) throw new Error(`Erreur ${resReceived.status}`);
    const dataReceived = await resReceived.json();
    receivedMessages.value = Array.isArray(dataReceived) ? dataReceived : [];
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});
</script>
