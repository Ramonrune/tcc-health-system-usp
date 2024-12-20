<template>
  <q-dialog :value="value" persistent>
    <div class="dialog-center">
      <div class="title-container">
        <div class="title">Novo paciente</div>
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
          <div class="row q-col-gutter-md" v-if="!exist">
            <div class="col-8">
              <BaseInputTitle title="Nome" />
              <q-input
                filled
                class="q-pb-md"
                v-model="name"
                label="Digite o nome do paciente"
                dense
                clearable
                :rules="[(val) => !!val || 'O nome é obrigatório']"
              />
            </div>
            <div class="col-4">
              <BaseInputTitle title="Data de nascimento" />
              <q-input
                v-model="birth_date"
                label="Informe a data de nascimento"
                type="date"
                filled
                dense
                :rules="[
                  (val) => !!val || 'A data de nascimento é obrigatória',
                ]"
              />
            </div>
          </div>

          <BaseInputTitle title="CPF" />
          <q-input
            filled
            v-model="cpf"
            mask="###.###.###-##"
            label="Digite o CPF do paciente"
            dense
            class="q-pb-md"
            clearable
            @update:model-value="handleSearch"
            :rules="[validateCpfField]"
          />

          <BaseInputTitle title="E-mail" v-if="!exist" />
          <q-input
            v-if="!exist"
            v-model="email"
            label="Informe o e-mail"
            type="email"
            filled
            dense
            :rules="[(val) => !!val || 'E-mail é obrigatório']"
          />

          <BaseInputTitle title="Telefone" v-if="!exist" />

          <q-input
            v-if="!exist"
            v-model="phone"
            label="Informe o telefone"
            mask="(##) #####-####"
            filled
            dense
            :rules="[(val) => !!val || 'O telefone é obrigatório']"
          />
        </div>

        <div class="row q-mt-md">
          <q-btn
            no-caps
            unelevated
            color="grey-4"
            icon="fa-solid fa-arrow-left"
            class="col q-mr-sm text-black"
            label="Cancelar"
            @click="onClose"
            type="submit"
          />

          <q-btn
            no-caps
            unelevated
            :loading="loading"
            label="Cadastrar"
            icon="fa-solid fa-save"
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
import { getPatientByCpf, register } from "src/service/PatientService";
import { usePatientStore } from "src/stores/PatientStore";
import { getOnlyNumbers } from "src/util/number";
import { showNegativeNotify, showPositiveNotify } from "src/util/plugins";
import { validateCpf } from "src/util/validate";
import { ref } from "vue";

const props = defineProps({
  value: {
    type: Boolean,
    default: () => true,
  },
  onClose: {
    type: Function,
  },
  onSuccess: {
    type: Function,
  },
});

const formRef = ref();
const cpf = ref("");
const name = ref("");
const email = ref("");
const birth_date = ref("");
const phone = ref("");
const loading = ref(false);
const exist = ref(true);

const handleSearch = async (val) => {
  const cpf = getOnlyNumbers(val);

  if (cpf.length != 11) {
    return;
  }

  loading.value = true;

  const patient = await getPatientByCpf({
    cpf: getOnlyNumbers(val),
  });

  if (patient === null) {
    loading.value = false;
    exist.value = false;
    showNegativeNotify(
      "Paciente não encontrado, preencha os dados necessários para continuar!"
    );
    return;
  } else {
    const body = {
      name: patient.name,
      birth_date: patient.birth_date,
      cpf: patient.cpf,
      email: patient.email,
      phone: patient.phone,
    };

    const response = await register(body);
    loading.value = false;

    if (response.status === 201) {
      showPositiveNotify("Paciente cadastrado com sucesso!");
      props.onSuccess();
    } else if (response.status === 409) {
      showNegativeNotify("Paciente já cadastrado!");
    } else {
      showNegativeNotify(
        "Um erro ocorreu ao cadastrar o paciente, por favor tente novamente mais tarde!"
      );
    }
  }
};
const validateCpfField = (ev) => {
  if (ev.length === 14 && validateCpf(cpf.value)) {
    return true;
  }
  if (ev.length !== 14) {
    return "Informe o CPF!";
  }

  return "CPF inválido!";
};

const handleSubmit = async () => {
  const isValid = await formRef.value.validate();

  if (!isValid) {
    return;
  }

  const body = {
    name: name.value,
    birth_date: birth_date.value,
    cpf: getOnlyNumbers(cpf.value),
    email: email.value,
    phone: getOnlyNumbers(phone.value),
  };

  loading.value = true;
  const response = await register(body);
  loading.value = false;

  if (response.status === 201) {
    showPositiveNotify("Paciente cadastrado com sucesso!");
    props.onSuccess();
  } else if (response.status === 409) {
    showNegativeNotify("Paciente já cadastrado!");
  } else {
    showNegativeNotify(
      "Um erro ocorreu ao cadastrar o paciente, por favor tente novamente mais tarde!"
    );
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
