<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Détails de l'adresse email</h1>

    <div v-if="loading" class="flex justify-center mt-12">
      <ProgressSpinner style="width: 60px; height: 60px" />
    </div>

    <Message v-else-if="error" severity="error" class="p-4 mb-4">
      {{ error }}
    </Message>

    <div v-else>
      <p class="text-lg text-purple-700 mb-4">
        Adresse email actuelle :
        <strong>{{ originalAddress || "Inconnue" }}</strong>
      </p>

      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Modifier l'adresse email :
        </label>
        <InputText v-model="editedAddress" class="w-full max-w-md" />
      </div>

      <Button
        label="Mettre à jour"
        icon="pi pi-save"
        class="bg-purple-600 hover:bg-purple-700 text-white mb-6"
        @click="updateEmail"
        :loading="updating"
      />

      <Button
        label="Envoyer un message"
        icon="pi pi-send"
        class="ml-4 bg-blue-600 hover:bg-blue-700 text-white mb-6"
        @click="goToSendMessage"
      />

      <Message v-if="successMessage" severity="success" class="mb-4">
        {{ successMessage }}
      </Message>

      <Message v-if="updateError" severity="error" class="mb-4">
        {{ updateError }}
      </Message>

      <EmailDetailsSent :messages="sentMessages" :idEmailAddress="emailId" />
      <EmailDetailsReceived :messages="receivedMessages" :idEmailAddress="emailId" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import EmailDetailsSent from "./EmailDetailsSent.vue";
import EmailDetailsReceived from "./EmailDetailsReceived.vue";
import { BACKEND_URL } from "@/config";

const route = useRoute();
const router = useRouter();
const emailId = route.params.emailId;

const originalAddress = ref("Adresse inconnue");
const editedAddress = ref("");
const sentMessages = ref([]);
const receivedMessages = ref([]);
const loading = ref(true);
const updating = ref(false);
const error = ref(null);
const updateError = ref(null);
const successMessage = ref(null);
const userId = ref(null); // pour PATCH

onMounted(async () => {
  try {
    const resSent = await fetch(
      `${BACKEND_URL}/messages/sent_messages?id_email_address=${emailId}`
    );
    if (!resSent.ok) throw new Error(`Erreur ${resSent.status}`);
    const dataSent = await resSent.json();
    sentMessages.value = Array.isArray(dataSent) ? dataSent : [];
    const currentEmail = dataSent[0]?.fromEmail;
    originalAddress.value = currentEmail?.address || "Adresse inconnue";
    editedAddress.value = currentEmail?.address || "";
    userId.value = currentEmail?.userId || currentEmail?.user?.id || null;

    const resReceived = await fetch(
      `${BACKEND_URL}/messages/received_messages?id_email_address=${emailId}`
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

async function updateEmail() {
  updateError.value = null;
  successMessage.value = null;
  updating.value = true;

  try {
    const res = await fetch(`${BACKEND_URL}/email_address/${emailId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        address: editedAddress.value,
        userId: userId.value,
      }),
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(
        errorData.detail?.[0]?.msg || "Erreur lors de la mise à jour"
      );
    }

    const result = await res.json();
    successMessage.value = `Adresse mise à jour : ${editedAddress.value}`;
    originalAddress.value = editedAddress.value;
  } catch (err) {
    updateError.value = err.message;
  } finally {
    updating.value = false;
  }
}

function goToSendMessage() {
  router.push(`/message/send/${emailId}`);
}
</script>
