<template>
  <BaseDashboardCard
    label="Quantidade de atendimentos"
    timeframe="Últimos 180 dias"
  >
    <template #default>
      <VChart
        ref="echart"
        :option="chartOptions"
        style="width: auto; height: 200px"
      />
    </template>
  </BaseDashboardCard>
</template>

<script setup>
import { graphic } from "echarts/core";
import VChart, { INIT_OPTIONS_KEY } from "vue-echarts";

import BaseDashboardCard from "src/components/BaseDashboardCard.vue";
import { onBeforeMount, provide, ref, useTemplateRef } from "vue";
import { getDateMinusMonth } from "src/util/date";
import { getAppointmentsPerMonth } from "src/service/DashboardService";

const initOptions = {
  renderer: "svg",
};

const echart = useTemplateRef("echart");

provide(INIT_OPTIONS_KEY, initOptions);

const options = {
  tooltip: {
    trigger: "axis",
    // showContent: false,
    axisPointer: {
      type: "shadow",
    },
    padding: 8,
    borderWidth: 1,
    borderColor: "#1E60FB",
    borderRadius: 8,

    formatter: "{b}</br><strong>{c}</strong>",
  },
  grid: {
    top: "10%",
    bottom: "15%",
    right: "10%",
    left: "10%",
  },
  xAxis: {
    type: "category",
    boundaryGap: false,
    axisTick: { show: false },
    axisLine: { show: false },
    axisLabel: {
      interval: 0,
      rich: {
        val: {
          color: "#424242",
          fontSize: 10,
          fontWeight: 500,
        },
        sub: {
          color: "#757575",
          fontSize: 10,
          fontWeight: 500,
        },
      },
    },
    data: [],
  },
  yAxis: {
    type: "value",
    boundaryGap: false,
    axisLabel: {
      formatter: function (value) {
        if (value >= 1000000) return (value / 1000000).toFixed(1) + "M";
        if (value >= 1000) return (value / 1000).toFixed(1) + "k";
        return value;
      },
    },
  },
  series: {
    data: [],
    type: "line",
    showSymbol: false,
    lineStyle: {
      color: "#0047EE",
      width: 1,
      type: "dashed",
    },
    areaStyle: {
      color: new graphic.LinearGradient(0, 0, 0, 1, [
        {
          offset: 0,
          color: "rgba(0, 71, 238, 0.40)",
        },
        {
          offset: 1,
          color: "rgba(37, 96, 205, 0.00)",
        },
      ]),
    },
  },
};

onBeforeMount(async () => {
  let appointments = await getAppointmentsPerMonth();
  appointments = appointments.map((e) => e.total);
  chartOptions.value.series.data = appointments;
});

const chartOptions = ref(options);

chartOptions.value.xAxis.data = getLast6Months();

function getLast6Months() {
  const last12Months = [];
  for (let i = 6; i >= 0; i--) last12Months.push(getDateMinusMonth(i));
  return last12Months;
}
</script>
