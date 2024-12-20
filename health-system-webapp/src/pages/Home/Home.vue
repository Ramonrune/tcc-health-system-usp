<template>
  <div>
    <HeaderComponent :breadcrumbs="breadcrumbs" />

    <TesTE text="Olá, tudo bem?" />
    <div class="q-pa-md">
      <div class="row q-col-gutter-md q-pb-md">
        <div class="col">
          <HomeCardOverview />
        </div>

        <div class="col">
          <HomeCardAppointments />
        </div>
      </div>

      <HomeCardCalendar />
    </div>
  </div>
</template>

<script setup>
import HeaderComponent from "src/components/HeaderComponent.vue";
import { ref } from "vue";
import HomeCardOverview from "./HomeCardOverview.vue";
import HomeCardAppointments from "./HomeCardAppointments.vue";
import HomeCardCalendar from "./HomeCardCalendar.vue";
import TesTE from "./TesTE.vue";

defineOptions({
  name: "HomePage",
});

const breadcrumbs = ref([
  {
    label: "Dashboard",
  },
]);
</script>
