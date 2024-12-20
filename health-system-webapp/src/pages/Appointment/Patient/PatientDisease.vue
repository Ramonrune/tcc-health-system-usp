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

    <PatientDiseaseDialog
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
import PatientDiseaseDialog from "./PatientDiseaseDialog.vue";
import { showNegativeNotify, showPositiveNotify } from "src/util/plugins";
import { useQuasar } from "quasar";
import { getPatientDiseases, remove } from "src/service/DiseaseService";
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
    label: "Nome da doença",
    align: "left",
    field: "name",
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
  const medications = await getPatientDiseases({
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
    message: `Deseja realmente remover a doença ${row.name}?`,
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    const ok = await remove({
      id: row.patient_disease_id,
    });

    if (ok) {
      showPositiveNotify("Doença removida com sucesso!");
      await refresh();
    } else {
      showNegativeNotify(
        "Ocorreu um problema ao remover a doença, por favor tente novamente mais tarde!"
      );
    }
  });
};

const onUpdateItem = (row) => {
  idUpdate.value = row.patient_disease_id;
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
