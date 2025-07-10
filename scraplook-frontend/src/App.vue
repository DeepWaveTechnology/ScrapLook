<template>
  <Header />
  <router-view />
</template>

<script setup>
import Header from './components/Header.vue';
import { watch } from 'vue';
import { useAuth } from '@/composables/useAuth';
import { startWatching, stopWatching } from '@/watchers/accessTokenWatcher';

const { isLoggedIn } = useAuth()
watch(isLoggedIn, (val) => {
  if (val) {
    startWatching();
  } else {
    stopWatching();
  }
});
</script>
