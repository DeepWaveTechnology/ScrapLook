<template>
  <div class="max-w-xl mx-auto mt-12 p-8 bg-white shadow-lg rounded-lg">
    <h2 class="text-2xl font-bold mb-6 text-center text-purple-800">Connexion</h2>

    <Message v-if="successMessage" severity="success" class="mb-4">
      {{ successMessage }}
    </Message>

    <Message v-if="errorMessage" severity="error" class="mb-4">
      {{ errorMessage }}
    </Message>

    <form @submit.prevent="submitForm" class="space-y-6">
      <div>
        <label class="block text-sm font-semibold text-gray-700 mb-1">Nom d'utilisateur</label>
        <InputText v-model="form.name" class="w-full" />
      </div>

      <div>
        <label class="block text-sm font-semibold text-gray-700 mb-1">Mot de passe</label>
        <Password
          v-model="form.password"
          class="w-full"
          toggleMask
          promptLabel="Entrer mot de passe"
        />
      </div>

      <Button
        label="Connexion"
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
import { useAuth } from '@/composables/useAuth' // ✅ Ajouté
import { BACKEND_URL } from '@/config'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
import Message from 'primevue/message'

const form = ref({
  name: '',
  password: '',
})

const loading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const router = useRouter()
const { login } = useAuth() // ✅ Appel du composable

async function submitForm() {
  loading.value = true
  successMessage.value = ''
  errorMessage.value = ''

  const payload = new URLSearchParams()
  payload.append('username', form.value.name)
  payload.append('password', form.value.password)

  try {
    const response = await fetch(`${BACKEND_URL}/auth/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: payload,
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || "Erreur d'authentification")
    }

    // ✅ Appel du login du composable
    login(data.access_token, form.value.name)

    successMessage.value = 'Connexion réussie !'
    router.push('/')
  } catch (err) {
    errorMessage.value = err.message
  } finally {
    loading.value = false
  }
}
</script>
