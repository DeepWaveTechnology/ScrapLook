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
        <InputText v-model="editedAddress" class="w-full max-w-md" @keydown.enter.prevent />
      </div>

      <Button label="Mettre à jour" icon="pi pi-save" class="bg-purple-600 hover:bg-purple-700 text-white mb-6"
        @click="updateEmail" :loading="updating" />

      <Button label="Envoyer un message" icon="pi pi-send" class="ml-4 bg-blue-600 hover:bg-blue-700 text-white mb-6"
        @click="goToSendMessage" />

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
import api from "@/api"

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

// -------- Récupération des infos de l’adresse email ----------
async function getEmailAddressInformation(idEmailAddress) {
  try {
    const { data: currentEmail } = await api.get(`/email_address/${idEmailAddress}`)

    if (currentEmail && currentEmail.address) {
      originalAddress.value = currentEmail.address
      editedAddress.value = currentEmail.address
      userId.value = currentEmail.userId || currentEmail.user?.id || null
    } else {
      originalAddress.value = "Adresse inconnue"
      editedAddress.value = ""
      userId.value = null
    }
  } catch (err) {
    error.value = err.response?.data?.detail || err.message
  }
}

// -------- Chargement des messages envoyés et reçus ----------
onMounted(async () => {
  await getEmailAddressInformation(emailId)

  try {
    const { data: dataSent } = await api.get(`/messages/sent_messages`, {
      params: { id_email_address: emailId },
    })
    sentMessages.value = Array.isArray(dataSent) ? dataSent : []

    const { data: dataReceived } = await api.get(`/messages/received_messages`,
        {
      params: { id_email_address: emailId },
    })
    receivedMessages.value = Array.isArray(dataReceived) ? dataReceived : []
  } catch (err) {
    error.value = err.response?.data?.detail || err.message
  } finally {
    loading.value = false
  }
})

// -------- Mise à jour de l'adresse email ----------
async function updateEmail() {
  updateError.value = ""
  successMessage.value = ""

  const trimmedAddress = editedAddress.value.trim()

  const emailRegex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/
  if (!trimmedAddress) {
    updateError.value = "L'adresse email ne peut pas être vide."
    return
  }
  if (!emailRegex.test(trimmedAddress)) {
    updateError.value = "L'adresse email n'est pas valide."
    return
  }
  const domainPart = trimmedAddress.split("@")[1]
  if (/\d/.test(domainPart)) {
    updateError.value = "La partie domaine de l'adresse email ne doit pas contenir de chiffre."
    return
  }
  if (trimmedAddress === originalAddress.value) {
    updateError.value = "L'adresse est identique à l'originale."
    return
  }
  if (!userId.value) {
    updateError.value = "Utilisateur introuvable pour cette adresse."
    return
  }

  updating.value = true

  try {
    await api.patch(`/email_address/${emailId}`, {
      address: trimmedAddress,
      userId: userId.value,
    })

    await getEmailAddressInformation(emailId)
    successMessage.value = "Adresse mise à jour avec succès."
  } catch (err) {
    updateError.value =
      err.response?.data?.detail?.[0]?.msg ||
      err.response?.data?.detail ||
      "Erreur lors de la mise à jour"
  } finally {
    updating.value = false
  }
}
function goToSendMessage() {
  router.push(`/message/send/${emailId}`);
}
</script>
