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
      <p class="text-lg text-purple-700 mb-4" v-if="originalAddress">
        Adresse email actuelle :
        <strong>{{ originalAddress }}</strong>
      </p>
      <p v-else>Adresse email actuelle : <strong>Inconnue</strong></p>

      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Modifier l'adresse email :
        </label>
        <InputText
          v-model="editedAddress"
          class="w-full max-w-md"
          @keydown.enter.prevent
        />
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
      <EmailDetailsReceived
        :messages="receivedMessages"
        :idEmailAddress="emailId"
      />
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

    let currentEmail = null;
    if (
      Array.isArray(dataSent) &&
      dataSent.length > 0 &&
      dataSent[0]?.fromEmail
    ) {
      currentEmail = dataSent[0].fromEmail;
    }

    if (currentEmail && currentEmail.address) {
      originalAddress.value = currentEmail.address;
      editedAddress.value = currentEmail.address;
      userId.value = currentEmail.userId || currentEmail.user?.id || null;
    } else {
      originalAddress.value = "Adresse inconnue";
      editedAddress.value = "";
      userId.value = null;
    }

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

  const trimmedAddress = editedAddress.value.trim();

  if (!trimmedAddress) {
    updateError.value = "L'adresse email ne peut pas être vide.";
    return;
  }

  // Validation du format email avec ta regex
  const emailRegex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
  if (!emailRegex.test(trimmedAddress)) {
    updateError.value = "L'adresse email n'est pas valide.";
    return;
  }

  // Vérification qu'il n'y ait pas de chiffre dans la partie domaine après le '@'
  const domainPart = trimmedAddress.split("@")[1];
  if (/\d/.test(domainPart)) {
    updateError.value =
      "La partie domaine de l'adresse email ne doit pas contenir de chiffre.";
    return;
  }

  if (trimmedAddress === originalAddress.value) {
    updateError.value = "L'adresse est identique à l'originale.";
    return;
  }

  if (!userId.value) {
    updateError.value = "Utilisateur introuvable pour cette adresse.";
    return;
  }

  updating.value = true;

  try {
    const res = await fetch(`${BACKEND_URL}/email_address/${emailId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        address: trimmedAddress,
        userId: userId.value,
      }),
    });

    if (!res.ok) {
      let errorData;
      try {
        errorData = await res.json();
      } catch {
        errorData = null;
      }
      throw new Error(
        errorData?.detail?.[0]?.msg || "Erreur lors de la mise à jour"
      );
    }

    await reloadEmailAddress();

    successMessage.value = `Adresse mise à jour avec succès.`;
  } catch (err) {
    updateError.value = err.message;
  } finally {
    updating.value = false;
  }
}

// Fonction pour recharger l'adresse mail depuis le backend
async function reloadEmailAddress() {
  try {
    const resSent = await fetch(
      `${BACKEND_URL}/messages/sent_messages?id_email_address=${emailId}`
    );
    if (!resSent.ok) throw new Error(`Erreur ${resSent.status}`);

    const dataSent = await resSent.json();
    sentMessages.value = Array.isArray(dataSent) ? dataSent : [];

    let currentEmail = null;
    if (
      Array.isArray(dataSent) &&
      dataSent.length > 0 &&
      dataSent[0]?.fromEmail
    ) {
      currentEmail = dataSent[0].fromEmail;
    }

    if (currentEmail && currentEmail.address) {
      originalAddress.value = currentEmail.address;
      editedAddress.value = currentEmail.address;
      userId.value = currentEmail.userId || currentEmail.user?.id || null;
    } else {
      originalAddress.value = "Adresse inconnue";
      editedAddress.value = "";
      userId.value = null;
    }
  } catch (err) {
    error.value = err.message;
  }
}

function goToSendMessage() {
  router.push(`/message/send/${emailId}`);
}
</script>
