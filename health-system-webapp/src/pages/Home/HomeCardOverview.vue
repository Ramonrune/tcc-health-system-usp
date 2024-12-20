<template>
  <BaseDashboardCard
    label="Visão geral do fluxo de trabalho"
    timeframe="Últimos 30 dias"
  >
    <div class="content">
      <div class="column flex-center no-wrap q-gutter-y-xs ellipsis">
        <div class="colored-box" style="background-color: rgb(231, 238, 254)">
          <q-icon
            name="fa-solid fa-calendar-days"
            size="24px"
            style="color: #0277bd"
          />
        </div>
        <div class="text-1">{{ totals.total_appointments }}</div>
        <div class="text-2">Atendimentos</div>
      </div>

      <div class="column flex-center no-wrap q-gutter-y-xs ellipsis">
        <div class="colored-box" style="background-color: rgb(230, 240, 255)">
          <q-icon
            name="fa-solid fa-person-cane"
            size="24px"
            style="color: rgb(33, 64, 125)"
          />
        </div>
        <div class="text-1">{{ totals.mean_age }}</div>
        <div class="text-2">Idade média</div>
      </div>

      <div class="column flex-center no-wrap q-gutter-y-xs ellipsis">
        <div class="colored-box" style="background-color: rgb(225, 245, 254)">
          <q-icon
            name="fa-solid fa-person"
            size="24px"
            style="color: rgb(0, 104, 139)"
          />
        </div>
        <div class="text-1">{{ totals.total_males }}</div>
        <div class="text-2">Homens</div>
      </div>

      <div class="column flex-center no-wrap q-gutter-y-xs ellipsis">
        <div class="colored-box" style="background-color: rgb(255, 230, 240)">
          <q-icon
            name="fa-solid fa-person-dress"
            size="24px"
            style="color: rgb(194, 24, 91)"
          />
        </div>
        <div class="text-1">{{ totals.total_females }}</div>
        <div class="text-2">Mulheres</div>
      </div>
    </div>
  </BaseDashboardCard>
</template>

<script setup>
import BaseDashboardCard from "src/components/BaseDashboardCard.vue";
import { getOverview } from "src/service/DashboardService";
import { onBeforeMount, ref } from "vue";

const totals = ref({
  mean_age: "",
  total_appointments: "",
  total_females: "",
  total_males: "",
});
onBeforeMount(async () => {
  const overview = await getOverview();
  totals.value = overview;
});
</script>

<style scoped lang="scss">
.content {
  // display: flex;
  // justify-content: space-around;
  // flex-wrap: nowrap;
  display: grid;
  grid-auto-flow: column;
  grid-template-columns: repeat(auto-fit, minmax(0, 1fr));

  height: 200px;
  padding-left: map-get($space-md, x);
  padding-right: map-get($space-md, x);
}

.colored-box {
  width: 48px;
  height: 48px;
  border-radius: 8px;

  display: flex;
  align-items: center;
  justify-content: center;
}

.text-1 {
  color: var(--Quasar-Grey-10, #162238);
  text-align: center;
  font-size: 24px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px;
}

.text-2 {
  color: var(--Quasar-Grey-Blue-08, #455a64);
  text-align: center;
  font-size: 12px;
  font-weight: 400;
  line-height: 12px;
}
</style>
