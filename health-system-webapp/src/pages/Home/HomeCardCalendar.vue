<template>
  <BaseDashboardCard label="Atendimentos" timeframe="Mês atual">
    <Qalendar :events="events" :config="config" style="height: 400px" />
  </BaseDashboardCard>
</template>

<script setup>
import { Qalendar } from "qalendar";
import BaseDashboardCard from "src/components/BaseDashboardCard.vue";
import { getAppointmentCalendar } from "src/service/DashboardService";
import { onBeforeMount, ref } from "vue";

const config = ref({ defaultMode: "month" });
const events = ref([
  {
    title: "10 Atendimentos",
    time: { start: "2024-12-17", end: "2024-12-17" },
    color: "yellow",
    isEditable: false,
  },
]);

onBeforeMount(async () => {
  const items = await getAppointmentCalendar();
  let evts = [];
  for (let item of items) {
    if (item["count"] === 0) {
      continue;
    }
    evts.push({
      title: item["count"] + " atendimento(s)",
      time: { start: item["period"], end: item["period"] },
      color: "yellow",
      isEditable: false,
    });
  }

  console.log(evts);

  events.value = evts;
});
</script>

<style>
@import "qalendar/dist/style.css";

.mode-is-month {
  border: none !important;
}

.calendar-header {
  display: none !important;
}
</style>
