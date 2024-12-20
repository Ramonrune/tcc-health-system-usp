<template>
  <div>
    <HeaderComponent :breadcrumbs="breadcrumbs" />

    <div class="q-pa-md">
      <div class="row q-col-gutter-sm">
        <div class="col">
          <div class="row q-col-gutter-md">
            <BaseSearch @update:model-value="handleSearch" style="flex: 1" />
            <q-input
              v-model="startDate"
              label="Data inicial"
              type="date"
              filled
              dense
              :rules="[(val) => !!val || 'A data inicial é obrigatória']"
            />

            <q-input
              v-model="endDate"
              label="Data final"
              type="date"
              filled
              dense
              :rules="[(val) => !!val || 'A data inicial é obrigatória']"
            />
          </div>
        </div>
        <div>
          <BaseRefreshButton class="q-mr-sm" :handle-click="refresh" />

          <BaseAddButton title="Adicionar" :handle-click="handleAdd" />
        </div>
      </div>

      <BaseTable
        class="table-custom"
        :rows="tableRowsTmp"
        :columns="tableColumns"
        :loading="isLoading"
        row-key="id"
        :actionColumns="['view']"
        :onViewItem="onViewItem"
      />
    </div>

    <AppointmentDialog
      v-if="appointmentModal"
      v-model="appointmentModal"
      :onClose="onClose"
    />
  </div>
</template>

<script setup>
import { onBeforeMount, ref, watch } from "vue";

import BaseAddButton from "src/components/BaseAddButton.vue";
import BaseSearch from "src/components/BaseSearch.vue";
import BaseTable from "src/components/BaseTable.vue";
import HeaderComponent from "src/components/HeaderComponent.vue";
import AppointmentDialog from "./AppointmentDialog.vue";
import { getAppointments } from "src/service/AppointmentService";
import { getPatientByCpf } from "src/service/PatientService";
import { Loading } from "quasar";
import { usePatientStore } from "src/stores/PatientStore";
import { useRouter } from "vue-router";
import { getToday } from "src/util/date";
import BaseRefreshButton from "src/components/BaseRefreshButton.vue";

defineOptions({
  name: "PatientPage",
});

const patientStore = usePatientStore();

const breadcrumbs = ref([
  {
    label: "Atendimento",
  },
]);

const appointmentModal = ref(false);

const onClose = () => {
  appointmentModal.value = false;
};

const tableRows = ref([]);
const tableRowsTmp = ref([]);

const startDate = ref(getToday());
const endDate = ref(getToday());

watch(startDate, (newVal, oldVal) => {
  refresh();
});

watch(endDate, (newVal, oldVal) => {
  refresh();
});

const handleAdd = () => {
  appointmentModal.value = true;
};

const tableColumns = ref([
  {
    name: "date_entered",
    required: true,
    label: "Data",
    align: "left",
    field: "date_entered",
    sortable: true,
    visible: true,
    style: "width: 50px;",
  },
  {
    name: "cpf",
    required: true,
    label: "CPF",
    align: "left",
    field: "cpf",
    sortable: true,
    visible: true,
    style: "width: 50px;",
  },
  {
    name: "name",
    required: true,
    label: "Nome",
    align: "left",
    field: "name",
    sortable: true,
    visible: true,
  },
  {
    name: "age",
    required: true,
    label: "Idade",
    align: "left",
    field: "age",
    sortable: true,
    visible: true,
    style: "width: 50px;",
  },
  {
    name: "actions",
    required: true,
    label: "Ações",
    align: "left",
    field: "actions",
    sortable: true,
    visible: true,
    style: "width: 50px;",
  },
]);

const isLoading = ref(false);

const handleSearch = (text) => {
  if (text === "") {
    tableRowsTmp.value = Object.assign([], tableRows.value);
  } else {
    tableRowsTmp.value = tableRows.value.filter((e) =>
      e.name.toLowerCase().includes(text.toLowerCase())
    );
  }
};

const refresh = async () => {
  isLoading.value = true;
  const appointments = await getAppointments({
    start_date: startDate.value,
    end_date: endDate.value,
  });
  isLoading.value = false;

  tableRows.value = appointments;
  tableRowsTmp.value = Object.assign([], appointments);
};

const router = useRouter();

const onViewItem = async (item) => {
  Loading.show({
    message: "Buscando dados do paciente...",
  });
  const patient = await getPatientByCpf({
    cpf: item.cpf,
  });

  Loading.hide();

  patientStore.setPatient(patient);
  router.push({
    path: "/patient/data",
  });
};
onBeforeMount(() => {
  refresh();
});
</script>
