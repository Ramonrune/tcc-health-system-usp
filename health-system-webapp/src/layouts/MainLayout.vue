<template>
  <q-layout view="hHh Lpr lFf" class="layout">
    <q-header
      class="row justify-between items-center"
      style="padding: 12px 16px; z-index: 9000"
    >
      <q-toolbar-title class="row items-center q-gutter-xs">
        <RouterLink to="/home" aria-label="home" class="logo text-white">
          Health System
        </RouterLink>
      </q-toolbar-title>
    </q-header>

    <q-drawer
      v-model="drawer"
      class="menu"
      show-if-above
      bordered
      :width="260"
      :breakpoint="500"
      :mini="!drawer || miniState"
    >
      <div class="mini">
        <q-btn
          class="mini-btn"
          size="10px"
          dense
          unelevated
          color="white"
          text-color="black"
          :icon="miniState ? 'chevron_right' : 'chevron_left'"
          @click="miniState = !miniState"
        />
      </div>

      <q-scroll-area class="menu-body" style="margin-top: 0px !important">
        <q-list padding :class="miniState ? '' : 'q-mr-sm'">
          <div v-for="item in menuItems" :key="item.id">
            <MenuItem
              :label="!miniState ? item.label : ''"
              :icon="item.icon"
              :key="item.label"
              :to="item.link"
              :action="item.action"
              :link="item.link"
              size="20px"
              color="primary"
              tag="router-link"
            />
          </div>
        </q-list>
      </q-scroll-area>

      <div
        class="row q-pa-sm items-center cursor-pointer"
        :class="miniState ? 'justify-center' : 'justify-between'"
      >
        <div class="row items-center" style="gap: 12px">
          <div class="column" v-if="!miniState">
            <div style="font-size: 11px; font-weight: 410; white-space: nowrap">
              {{ user.name }}
            </div>
            <div style="font-size: 9px; font-weight: 400; white-space: nowrap">
              {{ user.email }}
            </div>
          </div>
        </div>

        <q-btn
          :label="miniState ? '' : 'Sair'"
          icon="logout"
          size="10px"
          dense
          flat
          @click="handleLogoff"
        />
      </div>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from "vue";
import MenuItem from "src/components/MenuItem.vue";
import { useAuthStore } from "src/stores/AuthStore";

defineOptions({
  name: "MainLayout",
});

const authStore = useAuthStore();
const drawer = ref(true);
const miniState = ref(false);
const user = ref(authStore.user);
const menuItems = ref([
  {
    id: "home",
    label: "Home",
    icon: "home",
    link: "/home",
  },
  {
    id: "appointment",
    label: "Atendimento",
    icon: "appointment",
    link: "/appointment",
  },
  {
    id: "patient",
    label: "Paciente",
    icon: "patient",
    link: "/patient",
  },
]);

const handleLogoff = () => {
  localStorage.clear();
  window.location.href = "/";
};
</script>

<style lang="scss">
.mini {
  padding: 0px 8px;
  display: flex;
  justify-content: flex-end;
  border-radius: 4px;
  margin-top: 12px;

  .mini-btn {
    box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.08);
  }
}

.menu {
  color: #454646;
  background: #f0f1f3;
}

.menu-body {
  height: calc(100% - 84px);
  margin-top: 20px;
}
</style>
