<template>
  <q-layout
    view="hHh lpR fFf"
    class="overflow-auto"
    style="height: 100svh !important"
  >
    <q-header :height-hint="60" bordered reveal :reveal-offset="100">
      <q-toolbar
        class="flex justify-between"
        style="padding: 0.75rem 2rem; height: 60px"
      >
        <RouterLink to="/auth" aria-label="home" class="logo">
          Health System
        </RouterLink>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view class="q-pb-md" :class="{ 'q-pt-sm': !isMobile }" />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { computed, provide, ref } from "vue";
import { useQuasar } from "quasar";

defineOptions({
  name: "AuthorizationLayout",
});

const quasar = useQuasar();

const isMobile = computed(() => {
  return quasar.screen.lt.sm;
});

provide("isMobile", isMobile);
</script>

<style scoped lang="scss">
.q-header {
  background-color: transparent;
  backdrop-filter: blur(1px);
}

// .q-header--hidden{
//   background-color: red;
// }

.q-layout {
  height: inherit !important;
  background: url("src/assets/images/login_background.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* Child Styles */

:deep(button) {
  height: 3rem;
  font-size: 1rem;
}

:deep(.radial-blue-btn) {
  background: linear-gradient(135deg, #007fff 0%, #0036b3 100%);
  color: #fbfbfd;
  font-weight: 500;
}

:deep(.hr-lines) {
  position: relative;
  display: flex;
  text-align: center;

  &:before,
  &:after {
    content: "";
    display: inline-block;
    border-top: 1px solid $grey-5;
    transform: translateY(50%);
    flex: 1;
  }

  &:before {
    margin-right: 1rem;
  }

  &:after {
    margin-left: 1rem;
  }
}
</style>
