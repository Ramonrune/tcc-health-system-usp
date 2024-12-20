<template>
  <div>
    <HeaderComponent :breadcrumbs="breadcrumbs" />

    <div class="q-pa-md">
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
    </div>

    <PatientDialog
      v-if="modal"
      v-model="modal"
      :onClose="onClose"
      :onSuccess="onSuccess"
    />
  </div>
</template>

<script setup>
import { onBeforeMount, ref } from "vue";
import { Loading, useQuasar } from "quasar";

import BaseAddButton from "src/components/BaseAddButton.vue";
import BaseSearch from "src/components/BaseSearch.vue";
import BaseTable from "src/components/BaseTable.vue";
import HeaderComponent from "src/components/HeaderComponent.vue";
import BaseRefreshButton from "src/components/BaseRefreshButton.vue";
import PatientDialog from "./PatientDialog.vue";
import {
  getDoctorPatients,
  getPatientByCpf,
  remove,
} from "src/service/PatientService";
import { showNegativeNotify, showPositiveNotify } from "src/util/plugins";
import { usePatientStore } from "src/stores/PatientStore";
import { useRouter } from "vue-router";

defineOptions({
  name: "PatientPage",
});

const patientStore = usePatientStore();

const breadcrumbs = ref([
  {
    label: "Paciente",
  },
]);

const tableRows = ref([]);
const tableRowsTmp = ref([]);
const isLoading = ref(false);
const modal = ref(false);

const onClose = () => {
  modal.value = false;
};

const onSuccess = () => {
  modal.value = false;
  refresh();
};

const handleAdd = () => {
  modal.value = true;
};

const handleRefresh = () => {
  refresh();
};

const refresh = async () => {
  isLoading.value = true;
  const patients = await getDoctorPatients();
  isLoading.value = false;
  tableRows.value = patients;
  tableRowsTmp.value = Object.assign([], tableRows.value);
};

onBeforeMount(() => {
  refresh();
});

const q = useQuasar();
const router = useRouter();

const onDeleteItem = (row) => {
  q.dialog({
    title: "Remover",
    message: `Deseja realmente remover o paciente?`,
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    const ok = await remove({
      id: row.id,
    });

    if (ok) {
      showPositiveNotify("Paciente removido com sucesso!");
      await refresh();
    } else {
      showNegativeNotify(
        "Ocorreu um problema ao remover o paciente, por favor tente novamente mais tarde!"
      );
    }
  });
};

const onUpdateItem = async (row) => {
  Loading.show({
    message: "Buscando dados do paciente...",
  });
  const patient = await getPatientByCpf({
    cpf: row.cpf,
  });

  Loading.hide();
  if (patient === null) {
    showNegativeNotify("Paciente não encontrado!");
    return;
  }

  patientStore.setPatient(patient);
  router.push({
    path: "/patient/data",
  });
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

const tableColumns = ref([
  {
    name: "date_entered",
    required: true,
    label: "Data de cadastro",
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
    style: "width: 100px;",
  },
  {
    name: "name",
    required: true,
    label: "Nome",
    align: "left",
    field: "name",
    sortable: true,
    visible: true,
    classes: "text-ellipsis",
    style: "max-width: 150px;",
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
    style: "width: 100px;",
  },
]);
</script>
