<template>
  <div class="max-w-xl mx-auto mt-12 p-8 bg-white shadow-lg rounded-lg">
    <h2 class="text-2xl font-bold mb-6 text-center text-pink-700">
      Ajouter une adresse email
    </h2>

    <Message v-if="successMessage" severity="success" class="mb-4">
      {{ successMessage }}
    </Message>

    <Message v-if="errorMessage" severity="error" class="mb-4">
      {{ errorMessage }}
    </Message>

    <form @submit.prevent="submitForm" class="space-y-6">
      <div>
        <label class="block text-sm font-semibold text-gray-700 mb-1">
          Adresse email
        </label>
        <InputText
          v-model="form.address"
          class="w-full"
          placeholder="exemple@domaine.com"
        />
      </div>

      <Button
        label="Ajouter l'email"
        type="submit"
        class="w-full bg-pink-600 hover:bg-pink-700 text-white"
        :loading="loading"
        :disabled="!form.address || !isValidEmail(form.address)"
      />
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRoute } from "vue-router";
import api from '@/api'

// Récupération de l'ID utilisateur depuis l'URL
const route = useRoute();
const userId = route.params.userId;

// Données du formulaire
const form = ref({
  address: "",
  userId,
});

// États de l'interface
const loading = ref(false);
const successMessage = ref("");
const errorMessage = ref("");

// Validation du format email
function isValidEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

// Soumission du formulaire
async function submitForm() {
  successMessage.value = ''
  errorMessage.value = ''

  if (!isValidEmail(form.value.address)) {
    errorMessage.value = "Veuillez entrer une adresse email valide."
    return
  }

  loading.value = true

  try {
    const { data } = await api.post('/email_address/', form.value)

    successMessage.value = `Email ajouté avec succès : ${form.value.address}`
    form.value.address = ''
  } catch (err) {
    const msg =
      err.response?.data?.detail?.[0]?.msg ||
      err.response?.data?.detail ||
      err.message
    errorMessage.value = msg
  } finally {
    loading.value = false
  }
}
</script>
