<template>
  <div class="p-6 max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <h2
        class="text-3xl font-extrabold bg-gradient-to-r from-yellow-400 via-red-500 to-pink-500 bg-clip-text text-transparent"
      >
        Liste des utilisateurs
      </h2>
      <RouterLink to="/create/user">
        <Button
          icon="pi pi-user-plus"
          label="Ajouter un utilisateur"
          class="p-button-sm p-button-success"
        />
      </RouterLink>
    </div>

    <div v-if="loading" class="flex justify-center mt-12">
      <ProgressSpinner
        style="width: 60px; height: 60px"
        class="text-pink-500"
      />
    </div>

    <Message
      v-else-if="error"
      severity="error"
      :closable="false"
      class="text-lg font-semibold bg-red-100 border border-red-400 text-red-700 rounded-md p-4"
    >
      {{ error }}
    </Message>

    <div v-else>
      <Divider />

      <DataView
        :value="users"
        layout="list"
        :rows="6"
        class="border border-gray-200 rounded-lg shadow-lg"
        :paginator="true"
        style="background: white"
      >
        <template #list="{ items }">
          <div>
            <div
              v-for="user in items"
              :key="user.id"
              class="p-6 border-b border-gray-300 last:border-none"
            >
              <div class="flex justify-between items-start mb-2">
                <div class="text-xl font-semibold text-purple-900">
                  <span>{{ getFirstName(user.name) }}</span>
                  <span class="ml-2 font-normal text-purple-700">
                    {{ getLastName(user.name) }}
                  </span>
                </div>
                <RouterLink :to="`/create/mail${user.id}`">
                  <Button
                    icon="pi pi-envelope"
                    label="Ajouter un email"
                    class="p-button-sm p-button-secondary"
                  />
                </RouterLink>
              </div>

              <ul
                class="list-disc list-inside text-purple-800 space-y-1 max-w-md ml-2"
              >
                <li
                  v-for="email in user.emails"
                  :key="email.id"
                  class="flex items-center gap-4"
                >
                  <RouterLink
                    :to="`/email/${email.id}`"
                    class="text-pink-600 hover:underline cursor-pointer"
                    title="Voir l’email"
                  >
                    {{ email.address }}
                  </RouterLink>
                  <Button
                    icon="pi pi-trash"
                    class="p-button-sm p-button-danger"
                    @click="deleteEmail(email.id, user.id)"
                    title="Supprimer l'email"
                  />
                </li>
              </ul>

              <Divider />
            </div>
          </div>
        </template>
      </DataView>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { RouterLink } from "vue-router";

const users = ref([]);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    const res = await fetch("http://127.0.0.1:8000/user/all");
    if (!res.ok) throw new Error(`Erreur ${res.status}`);
    users.value = await res.json();

    for (const user of users.value) {
      const emailRes = await fetch(
        `http://127.0.0.1:8000/email_address/all?user_id=${user.id}`
      );
      if (!emailRes.ok) throw new Error(`Erreur ${emailRes.status}`);
      user.emails = await emailRes.json();
    }
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});

function getFirstName(fullName) {
  if (!fullName) return "";
  const parts = fullName.trim().split(" ");
  return parts[0] || "";
}

function getLastName(fullName) {
  if (!fullName) return "";
  const parts = fullName.trim().split(" ");
  return parts.length > 1 ? parts.slice(1).join(" ") : "";
}

async function deleteEmail(emailId, userId) {
  const confirmed = confirm("Voulez-vous vraiment supprimer cette adresse email ?");
  if (!confirmed) return;

  try {
    const res = await fetch(`http://127.0.0.1:8000/email_address/${emailId}`, {
      method: "DELETE",
    });
    if (!res.ok) throw new Error(`Erreur ${res.status}`);

    // Retirer l’email supprimé de la liste
    const user = users.value.find((u) => u.id === userId);
    if (user) {
      user.emails = user.emails.filter((e) => e.id !== emailId);
    }
  } catch (err) {
    alert("Erreur lors de la suppression : " + err.message);
  }
}

</script>
