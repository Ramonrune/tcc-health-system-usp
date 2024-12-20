<template>
  <q-dialog :value="value" persistent>
    <div class="dialog-center">
      <div class="title-container">
        <div class="title">Novo atendimento</div>
        <div>
          <q-icon
            name="fa-solid fa-close"
            size="24px"
            class="cursor-pointer"
            color="grey"
            @click="onClose"
          />
        </div>
      </div>

      <q-separator class="q-mb-md" />
      <q-form ref="formRef">
        <div>
          <div>
            <BaseInputTitle title="CPF" />
            <q-input
              filled
              v-model="cpf"
              mask="###.###.###-##"
              label="Digite o CPF do paciente"
              dense
              hint="Formato: 123.456.789-00"
              clearable
              :rules="[validateCpfField]"
            />
          </div>
        </div>

        <div class="row q-mt-md">
          <q-btn
            no-caps
            unelevated
            color="grey-4"
            class="col q-mr-sm text-black"
            label="Cancelar"
            @click="onClose"
            type="submit"
          />

          <q-btn
            no-caps
            unelevated
            :loading="loading"
            label="Iniciar atendimento"
            color="primary"
            type="submit"
            class="col"
            @click="handleSubmit()"
          />
        </div>
      </q-form>
    </div>
  </q-dialog>
</template>

<script setup>
import BaseInputTitle from "src/components/BaseInputTitle.vue";
import { getPatientByCpf } from "src/service/PatientService";
import { usePatientStore } from "src/stores/PatientStore";
import { getOnlyNumbers } from "src/util/number";
import { showNegativeNotify } from "src/util/plugins";
import { validateCpf } from "src/util/validate";
import { ref } from "vue";
import { useRouter } from "vue-router";

defineProps({
  value: {
    type: Boolean,
    default: () => true,
  },
  onClose: {
    type: Function,
  },
});

const patientStore = usePatientStore();

const formRef = ref();
const cpf = ref("");
const loading = ref(false);

const validateCpfField = (ev) => {
  if (ev.length === 14 && validateCpf(cpf.value)) {
    return true;
  }
  if (ev.length !== 14) {
    return "Informe o CPF!";
  }

  return "CPF inválido!";
};

const router = useRouter();
const handleSubmit = async () => {
  const isValid = await formRef.value.validate();

  if (!isValid) {
    return;
  }

  loading.value = true;
  const patient = await getPatientByCpf({
    cpf: getOnlyNumbers(cpf.value),
  });

  console.log(patient);
  if (patient === null) {
    loading.value = false;
    showNegativeNotify(
      "Paciente não encontrado! Acesse a tela de pacientes para realizar o cadastro!"
    );
    return;
  } else {
    loading.value = false;
    patientStore.setPatient(patient);
    router.push({
      path: "/patient/data",
    });
  }
};
</script>

<style scoped>
.title-container {
  display: flex;
  min-width: 400px !important;
}

.title {
  color: var(--Grey-10, #162238);

  /* Headline/H5 */
  font-family: Roboto;
  font-size: 24px;
  font-style: normal;
  font-weight: 700;
  line-height: 32px; /* 133.333% */
  flex: 1;
}
</style>

<style>
.q-dialog__inner--minimized {
  padding: 0px !important;
}
textarea:focus,
input:focus {
  outline: none;
}
</style>
