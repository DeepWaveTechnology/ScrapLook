<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Envoyer un message</h1>

    <div v-if="loading" class="flex justify-center mt-12">
      <ProgressSpinner style="width: 60px; height: 60px" />
    </div>

    <Message v-else-if="error" severity="error" class="p-4 mb-4">
      {{ error }}
    </Message>

    <form v-else @submit.prevent="sendMessage" class="space-y-6 max-w-md">
      <div>
        <label for="subject" class="block font-medium mb-1">Sujet (optionnel)</label>
        <InputText id="subject" v-model="subject" class="w-full" />
      </div>

      <div>
        <label for="body" class="block font-medium mb-1">Message</label>
        <Textarea
          id="body"
          v-model="body"
          rows="6"
          class="w-full"
          required
        />
      </div>

      <div>
        <label class="block font-medium mb-1">Destinataires</label>
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
        />
      </div>

      <Button
        label="Envoyer"
        icon="pi pi-send"
        type="submit"
        :loading="sending"
        class="bg-blue-600 hover:bg-blue-700 text-white"
      />

      <Message
        v-if="successMessage"
        severity="success"
        class="mt-4"
        @click="successMessage = null"
      >
        {{ successMessage }}
      </Message>

      <Message
        v-if="sendError"
        severity="error"
        class="mt-4"
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
import ProgressSpinner from "primevue/progressspinner";
import Message from "primevue/message";
import InputText from "primevue/inputtext";
import Textarea from "primevue/textarea";
import MultiSelect from "primevue/multiselect";
import Button from "primevue/button";

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
    const res = await fetch("http://127.0.0.1:8000/user/all");
    if (!res.ok) throw new Error(`Erreur ${res.status}`);
    const users = await res.json();

    // Pour chaque user, récupérer les emails
    for (const user of users) {
      const emailRes = await fetch(
        `http://127.0.0.1:8000/email_address/all?user_id=${user.id}`
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
    const res = await fetch("http://127.0.0.1:8000/messages/", {
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
