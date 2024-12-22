<template>
  <div>
    <HeaderComponent :breadcrumbs="breadcrumbs">
      <template v-slot:right-content>
        <div class="q-mr-md q-pt-xs">
          <q-icon
            name="fa-solid fa-envelope"
            size="24px"
            class="cursor-pointer"
            @click="handleSendEmail"
          >
            <q-tooltip>Enviar e-mail</q-tooltip>
          </q-icon>
        </div>
      </template>
    </HeaderComponent>

    <div class="q-pa-md">
      <q-tabs v-model="tab" align="left" no-caps dense>
        <q-tab name="patient" label="Dados gerais" />
        <q-tab name="exam" label="Exames" />
        <q-tab name="medication" label="Medicamentos" />
        <q-tab name="disease" label="Doenças" />
        <q-tab name="appointment" label="Atendimentos" />
      </q-tabs>

      <PatientData v-show="tab === 'patient'" />
      <PatientExam v-show="tab === 'exam'" />
      <PatientMedication v-show="tab === 'medication'" />
      <PatientDisease v-show="tab === 'disease'" />
      <PatientAppointment v-show="tab === 'appointment'" />
    </div>

    <PatientSendEmailDialog
      v-model="openModal"
      v-if="openModal"
      :onClose="onClose"
    />
  </div>
</template>

<script setup>
import { ref } from "vue";
import HeaderComponent from "src/components/HeaderComponent.vue";
import { usePatientStore } from "src/stores/PatientStore";
import PatientData from "./PatientData.vue";
import PatientExam from "./PatientExam.vue";
import PatientMedication from "./PatientMedication.vue";
import PatientDisease from "./PatientDisease.vue";
import PatientAppointment from "./PatientAppointment.vue";
import PatientSendEmailDialog from "./PatientSendEmailDialog.vue";

defineOptions({
  name: "PatientPage",
});

const tab = ref("patient");
const patientStore = usePatientStore();

const breadcrumbs = ref([
  {
    label: patientStore.patient.name,
  },
]);

const openModal = ref(false);

const handleSendEmail = () => {
  openModal.value = true;
};

const onClose = () => {
  openModal.value = false;
};
</script>
