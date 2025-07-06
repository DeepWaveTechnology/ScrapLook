<template>
  <div class="p-8 max-w-3xl mx-auto bg-white rounded-lg shadow-lg border border-gray-300">
    <h1 class="text-4xl font-extrabold mb-8 text-indigo-700 text-center tracking-wide">
      Envoyer un message
    </h1>

    <div v-if="loading" class="flex justify-center mt-16">
      <ProgressSpinner style="width: 72px; height: 72px" class="text-indigo-600" />
    </div>

    <Message
      v-else-if="error"
      severity="error"
      class="mb-8 p-5 rounded border border-red-400 bg-red-50 text-red-700 cursor-pointer"
      @click="error = null"
    >
      {{ error }}
    </Message>

    <form v-else @submit.prevent="sendMessage" class="space-y-8">
      <table class="w-full table-fixed border-collapse rounded-md overflow-hidden shadow-sm">
        <tbody>
          <!-- Sujet -->
          <tr class="bg-indigo-50 border-b border-indigo-200">
            <td class="py-4 px-6 font-semibold text-indigo-700 w-36">
              Sujet (optionnel)
            </td>
            <td class="py-4 px-6">
              <InputText
                id="subject"
                v-model="subject"
                class="w-full p-3 border border-indigo-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Titre de votre message"
              />
            </td>
          </tr>

          <!-- Message -->
          <tr class="bg-white border-b border-gray-200">
            <td class="py-4 px-6 font-semibold text-indigo-700 align-top">
              Message <span class="text-red-500">*</span>
            </td>
            <td class="py-4 px-6">
              <Textarea
                id="body"
                v-model="body"
                rows="6"
                required
                class="w-full p-3 border border-indigo-300 rounded-md shadow-sm resize-y focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Rédigez votre message ici..."
              />
            </td>
          </tr>

          <!-- Destinataires -->
          <tr class="bg-indigo-50 border-b border-indigo-200">
            <td class="py-4 px-6 font-semibold text-indigo-700 align-top">
              Destinataires <span class="text-red-500">*</span>
            </td>
            <td class="py-4 px-6">
              <MultiSelect
                v-model="selectedRecipients"
                :options="allEmails"
                optionLabel="address"
                optionValue="id"
                filter
                filterBy="address"
                placeholder="Choisir des destinataires"
                display="chip"
                class="w-full"
                required
                panelClassName="max-h-56 overflow-auto"
              />
            </td>
          </tr>
        </tbody>
      </table>

      <div class="pt-6 border-t border-gray-300 flex justify-end">
        <Button
          label="Envoyer"
          icon="pi pi-send"
          type="submit"
          :loading="sending"
          class="bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 focus:ring-4 focus:ring-indigo-300 text-white font-semibold rounded-md px-8 py-3 transition"
        />
      </div>

      <Message
        v-if="successMessage"
        severity="success"
        class="mt-8 p-5 rounded border border-green-400 bg-green-50 text-green-700 cursor-pointer"
        @click="successMessage = null"
      >
        {{ successMessage }}
      </Message>

      <Message
        v-if="sendError"
        severity="error"
        class="mt-8 p-5 rounded border border-red-400 bg-red-50 text-red-700 cursor-pointer"
        @click="sendError = null"
      >
        {{ sendError }}
      </Message>
    </form>
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { BACKEND_URL } from "@/config";

const route = useRoute();
const router = useRouter();
const fromId = route.params.id_address_mail;

const subject = ref("");
const body = ref("");
const selectedRecipients = ref([]);
const allEmails = ref([]);
const loading = ref(true);
const sending = ref(false);
const error = ref(null);
const sendError = ref(null);
const successMessage = ref(null);

onMounted(async () => {
  try {
    const res = await fetch(`${BACKEND_URL}/user/all`);
    if (!res.ok) throw new Error(`Erreur ${res.status}`);
    const users = await res.json();

    // Pour chaque user, récupérer les emails
    for (const user of users) {
      const emailRes = await fetch(
        `${BACKEND_URL}/email_address/all?user_id=${user.id}`
      );
      if (!emailRes.ok) throw new Error(`Erreur ${emailRes.status}`);
      user.emails = await emailRes.json();
    }

    // Extraire tous les emails dans un tableau plat
    allEmails.value = users.flatMap(user => user.emails || []);
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});

async function sendMessage() {
  sendError.value = null;
  successMessage.value = null;

  if (!body.value.trim()) {
    sendError.value = "Le message ne peut pas être vide.";
    return;
  }

  if (selectedRecipients.value.length === 0) {
    sendError.value = "Veuillez choisir au moins un destinataire.";
    return;
  }

  sending.value = true;

  try {
    const res = await fetch(`${BACKEND_URL}/messages/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        subject: subject.value || null,
        body: body.value,
        fromId: fromId,
        recipients: selectedRecipients.value.map(id => ({ id })),
      }),
    });

    if (res.status !== 201) {
      const errData = await res.json();
      throw new Error(errData.detail?.[0]?.msg || "Erreur lors de l'envoi");
    }

    // Succès
    successMessage.value = "Message envoyé avec succès !";
    subject.value = "";
    body.value = "";
    selectedRecipients.value = [];
  } catch (err) {
    sendError.value = err.message;
  } finally {
    sending.value = false;
  }
}
</script>
