<template>
  <div id="app">
    <Navbar v-if="isAuthenticated" />
    <router-view />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/store'
import Navbar from '@/components/Navbar.vue'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
</script>

<style>
#app {
  min-height: 100vh;
  background-color: #f8f9fa;
}
</style>
