<template>
  <div class="max-w-xl mx-auto mt-12 p-8 bg-white shadow-lg rounded-lg">
    <h2 class="text-2xl font-bold mb-6 text-center text-purple-800">Créer un utilisateur</h2>

    <Message v-if="successMessage" severity="success" class="mb-4">
      {{ successMessage }}
    </Message>

    <Message v-if="errorMessage" severity="error" class="mb-4">
      {{ errorMessage }}
    </Message>

    <form @submit.prevent="submitForm" class="space-y-6">
      <div>
        <label class="block text-sm font-semibold text-gray-700 mb-1">Nom</label>
        <InputText v-model="form.name" class="w-full" placeholder="Nom complet" />
      </div>

      <div>
        <label class="block text-sm font-semibold text-gray-700 mb-1">Mot de passe</label>
        <Password v-model="form.password" class="w-full" toggleMask promptLabel="Entrer mot de passe" />
      </div>

      <Button
        label="Créer l'utilisateur"
        type="submit"
        class="w-full bg-purple-600 hover:bg-purple-700 text-white"
        :loading="loading"
      />
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const form = ref({
  name: '',
  password: '',
})

const loading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const router = useRouter()

async function submitForm() {
  loading.value = true
  successMessage.value = ''
  errorMessage.value = ''

  try {
    const { data: result } = await api.post('/user/', form.value)

    successMessage.value = `Utilisateur "${result.name}" créé avec succès !`
    form.value.name = ''
    form.value.password = ''

    // Optionnel : rediriger vers /users
    // router.push('/users')

  } catch (err) {
    errorMessage.value =
      err.response?.data?.detail?.[0]?.msg || err.message || 'Erreur lors de la création'
  } finally {
    loading.value = false
  }
}
</script>
