<template>
  <div class="q-mt-md">
    <div class="row q-pb-md q-col-gutter-sm">
      <div class="col">
        <BaseSearch @update:model-value="handleSearch" />
      </div>

      <div>
        <BaseRefreshButton class="q-mr-sm" :handle-click="handleRefresh" />

        <BaseAddButton title="Adicionar" :handle-click="handleAdd" />
      </div>
    </div>

    <BaseTable
      class="table-custom"
      :rows="tableRowsTmp"
      :columns="tableColumns"
      :loading="isLoading"
      row-key="id"
      :onDeleteItem="onDeleteItem"
      :onUpdateItem="onUpdateItem"
      :onViewItem="onViewItem"
      :actionColumns="['view', 'edit', 'remove']"
    />

    <PatientAppointmentDialog
      v-if="openModal"
      v-model="openModal"
      :onClose="handleClose"
      :onSuccess="onSuccess"
      :id="idUpdate"
    />

    <PatientAppointmentAnalyseDialog
      v-if="openAnalyzeModal"
      v-model="openAnalyzeModal"
      :onClose="handleCloseAnalyze"
      :id="idUpdate"
    />
  </div>
</template>

<script setup>
import { onBeforeMount, ref } from "vue";
import { usePatientStore } from "src/stores/PatientStore";
import BaseTable from "src/components/BaseTable.vue";
import BaseSearch from "src/components/BaseSearch.vue";
import BaseAddButton from "src/components/BaseAddButton.vue";
import PatientAppointmentDialog from "./PatientAppointmentDialog.vue";
import { showNegativeNotify, showPositiveNotify } from "src/util/plugins";
import { useQuasar } from "quasar";
import { getPatientAppointments, remove } from "src/service/AppointmentService";
import BaseRefreshButton from "src/components/BaseRefreshButton.vue";
import PatientAppointmentAnalyseDialog from "./PatientAppointmentAnalyseDialog.vue";

defineOptions({
  name: "PatientAppointment",
});

const patientStore = usePatientStore();

const isLoading = ref(true);

const tableRows = ref([]);
const tableRowsTmp = ref([]);
const idUpdate = ref();

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
    name: "annotation",
    required: true,
    label: "Notas",
    align: "left",
    field: "annotation",
    sortable: true,
    visible: true,
    classes: "text-ellipsis",
    style: "max-width: 150px;",
  },
  {
    name: "actions",
    required: true,
    label: "Ações",
    align: "left",
    field: "actions",
    sortable: true,
    visible: true,
    style: "width: 100px;",
  },
]);

const openModal = ref(false);
const openAnalyzeModal = ref(false);
const handleAdd = () => {
  openModal.value = true;
};

const handleClose = () => {
  idUpdate.value = null;
  openModal.value = false;
};

const handleCloseAnalyze = () => {
  idUpdate.value = null;
  openAnalyzeModal.value = false;
};

const onSuccess = async () => {
  openModal.value = false;
  idUpdate.value = null;
  await refresh();
};

const refresh = async () => {
  isLoading.value = true;
  const appointments = await getPatientAppointments({
    patient_id: patientStore.patient.id,
  });

  tableRows.value = appointments;
  tableRowsTmp.value = Object.assign([], appointments);
  isLoading.value = false;
};

const q = useQuasar();

const onViewItem = (row) => {
  idUpdate.value = row.appointment_id;

  openAnalyzeModal.value = true;
};

const onDeleteItem = (row) => {
  q.dialog({
    title: "Remover",
    message: `Deseja realmente remover o atendimento?`,
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    const ok = await remove({
      id: row.appointment_id,
    });

    if (ok) {
      showPositiveNotify("Atendimento removido com sucesso!");
      await refresh();
    } else {
      showNegativeNotify(
        "Ocorreu um problema ao remover o atendimento, por favor tente novamente mais tarde!"
      );
    }
  });
};

const onUpdateItem = (row) => {
  idUpdate.value = row.appointment_id;
  openModal.value = true;
};

const handleSearch = (text) => {
  if (text === "") {
    tableRowsTmp.value = Object.assign([], tableRows.value);
  } else {
    tableRowsTmp.value = tableRows.value.filter((e) =>
      e.name.toLowerCase().includes(text.toLowerCase())
    );
  }
};

const handleRefresh = () => {
  refresh();
};
onBeforeMount(async () => {
  await refresh();
});
</script>

<style lang="scss">
.table-custom {
  width: 100%;
  height: calc(100vh - 250px);
  border-radius: 10px;

  .q-table__top {
    padding: 0;
  }
}
</style>
