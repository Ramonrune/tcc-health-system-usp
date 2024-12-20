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
      :actionColumns="['edit', 'remove']"
    />

    <PatientMedicationDialog
      v-if="openModal"
      v-model="openModal"
      :onClose="handleClose"
      :onSuccess="onSuccess"
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
import PatientMedicationDialog from "./PatientMedicationDialog.vue";
import { showNegativeNotify, showPositiveNotify } from "src/util/plugins";
import { useQuasar } from "quasar";
import { getPatientMedications, remove } from "src/service/MedicationService";
import BaseRefreshButton from "src/components/BaseRefreshButton.vue";

defineOptions({
  name: "PatientMedication",
});

const patientStore = usePatientStore();

const isLoading = ref(true);

const tableRows = ref([]);
const tableRowsTmp = ref([]);
const idUpdate = ref();

const tableColumns = ref([
  {
    name: "date",
    required: true,
    label: "Data",
    align: "left",
    field: "date",
    sortable: true,
    visible: true,
    style: "width: 50px;",
  },
  {
    name: "name",
    required: true,
    label: "Nome do medicamento",
    align: "left",
    field: "name",
    sortable: true,
    visible: true,
    style: "width: 300px;",
    classes: "text-ellipsis",
  },
  {
    name: "therapeutic_class",
    required: true,
    label: "Classe",
    align: "left",
    field: "therapeutic_class",
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
const handleAdd = () => {
  openModal.value = true;
};

const handleRefresh = () => {
  refresh();
};

const handleClose = () => {
  idUpdate.value = null;
  openModal.value = false;
};

const onSuccess = async () => {
  openModal.value = false;
  idUpdate.value = null;
  await refresh();
};

const refresh = async () => {
  isLoading.value = true;
  const medications = await getPatientMedications({
    patient_id: patientStore.patient.id,
  });

  tableRows.value = medications;
  tableRowsTmp.value = Object.assign([], medications);
  isLoading.value = false;
};

const q = useQuasar();

const onDeleteItem = (row) => {
  q.dialog({
    title: "Remover",
    message: `Deseja realmente remover o medicamento ${row.name}?`,
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    const ok = await remove({
      id: row.patient_medication_id,
    });

    if (ok) {
      showPositiveNotify("Medicamento removido com sucesso!");
      await refresh();
    } else {
      showNegativeNotify(
        "Ocorreu um problema ao remover o medicamento, por favor tente novamente mais tarde!"
      );
    }
  });
};

const onUpdateItem = (row) => {
  idUpdate.value = row.patient_medication_id;
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
