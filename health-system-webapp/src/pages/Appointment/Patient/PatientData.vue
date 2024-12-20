<template>
  <q-form ref="formRef" v-if="loadingPatient === false">
    <div class="row q-pt-md q-col-gutter-sm">
      <div class="col" style="max-width: 250px">
        <img
          :src="image"
          @error="onImageError"
          alt="Click to upload"
          width="200px"
          class="q-ml-lg cursor-pointer"
          @click="triggerFileInput"
        />
        <input
          type="file"
          accept="image/*"
          ref="fileInput"
          style="display: none"
          @change="onFileChange"
        />
      </div>
      <div class="col flex-1">
        <div class="row q-col-gutter-sm">
          <div class="col-9">
            <BaseInputTitle title="Nome" />
            <q-input
              v-model="form.name"
              label="Informe o nome"
              filled
              dense
              :rules="[(val) => !!val || 'O nome é obrigatório']"
            />
          </div>

          <div class="col-3">
            <BaseInputTitle title="Data de nascimento" />
            <q-input
              v-model="form.birth_date"
              label="Informe a data de nascimento"
              type="date"
              filled
              dense
              :rules="[(val) => !!val || 'A data de nascimento é obrigatória']"
            />
          </div>
        </div>

        <div class="row q-col-gutter-sm">
          <div class="col-5">
            <BaseInputTitle title="E-mail" />
            <q-input
              v-model="form.email"
              label="Informe o e-mail"
              disabled
              readonly
              type="email"
              filled
              dense
              :rules="[(val) => !!val || 'E-mail é obrigatório']"
            />
          </div>

          <div class="col-4">
            <BaseInputTitle title="CPF" />

            <q-input
              v-model="form.cpf"
              label="Informe o CPF"
              mask="###.###.###-##"
              disabled
              readonly
              filled
              dense
              :rules="[validateCpfField]"
            />
          </div>

          <div class="col-3">
            <BaseInputTitle title="Telefone" />

            <q-input
              v-model="form.phone"
              label="Informe o telefone"
              mask="(##) #####-####"
              filled
              dense
              :rules="[(val) => !!val || 'O telefone é obrigatório']"
            />
          </div>
        </div>

        <div class="row q-col-gutter-sm">
          <div class="col">
            <BaseInputTitle title="Gênero" />
            <q-select
              v-model="form.gender"
              label="Informe o gênero"
              :options="genderOptions"
              class="col"
              filled
              dense
            />
          </div>

          <div class="col">
            <BaseInputTitle title="Altura (cm)" />
            <q-input
              v-model="form.height"
              label="Informe a altura (cm)"
              type="number"
              filled
              dense
              :rules="[(val) => !!val || 'A altura é obrigatória']"
            />
          </div>

          <div class="col">
            <BaseInputTitle title="Peso (kg)" />
            <q-input
              v-model="form.weight"
              class="col"
              label="Informe o peso (kg)"
              type="number"
              filled
              dense
              :rules="[(val) => !!val || 'O peso é obrigatório']"
            />
          </div>

          <div class="col">
            <BaseInputTitle title="Tipo Sanguíneo" />
            <q-select
              v-model="form.blood_type"
              label="Informe o tipo sanguíneo"
              :options="bloodTypeOptions"
              filled
              dense
            />
          </div>
          <q-toggle v-model="form.smookes" label="Fumante" dense class="col" />
        </div>
        <div class="q-mt-md float-right">
          <q-btn
            no-caps
            unelevated
            :loading="loading"
            label="Salvar"
            color="primary"
            icon="fa fa-save"
            type="submit"
            @click="handleSubmit()"
          />
        </div>
      </div>
    </div>
  </q-form>
</template>

<script setup>
import { onBeforeMount, ref } from "vue";
import { usePatientStore } from "src/stores/PatientStore";
import { validateCpf } from "src/util/validate";
import {
  getPatient,
  getPatientPicture,
  update,
  uploadProfilePicture,
} from "src/service/PatientService";
import { showNegativeNotify, showPositiveNotify } from "src/util/plugins";
import BaseInputTitle from "src/components/BaseInputTitle.vue";

defineOptions({
  name: "PatientData",
});

const patientStore = usePatientStore();

const loading = ref(false);
const loadingPatient = ref(true);

const bloodTypeOptions = ref([
  "Não informado",
  "A+",
  "A-",
  "B+",
  "B-",
  "AB+",
  "AB-",
  "O+",
  "O-",
]);

const genderOptions = ref([
  { label: "Não informado", value: "U" },
  { label: "Masculino", value: "M" },
  { label: "Feminino", value: "F" },
  { label: "Outro", value: "O" },
]);

const DEFAULT_PICTURE =
  "https://www.transparentpng.com/download/user/gray-user-profile-icon-png-fP8Q1P.png";

const image = ref(DEFAULT_PICTURE);

const fileInput = ref();

const form = ref();
const formRef = ref();

onBeforeMount(async () => {
  loadingPatient.value = true;

  const list = [
    getPatient({ id: patientStore.patient.id }),
    getPatientPicture({ id: patientStore.patient.id }),
  ];
  const [patient, patientPicture] = await Promise.all(list);

  image.value = patientPicture;

  if (!patient) {
    loadingPatient.value = false;
    return;
  }

  let gender = genderOptions.value.filter((e) => e.value === patient.gender);

  if (gender.length === 0) {
    gender = { label: "Não informado", value: "N" };
  } else {
    gender = gender[0];
  }

  let smookes = false;
  if (patient.smookes === 1) {
    smookes = true;
  }

  let bloodType = patient.blood_type;
  if (bloodType === null) {
    bloodType = "Não informado";
  }

  form.value = {
    birth_date: patient.birth_date,
    blood_type: bloodType,
    cpf: patient.cpf.replaceAll(".", "").replaceAll("-", ""),
    email: patient.email,
    gender: gender,
    height: patient.height,
    name: patient.name,
    phone: patient.phone,
    smookes: patient.smookes,
    weight: patient.weight,
  };
  loadingPatient.value = false;
});

const validateCpfField = (ev) => {
  ev = ev.replaceAll(".", "").replaceAll("-", "");
  if (ev.length === 11 && validateCpf(form.value.cpf)) {
    return true;
  }
  if (ev.length !== 11) {
    return "Informe o CPF!";
  }

  return "CPF inválido!";
};

const handleSubmit = async () => {
  const isValid = await formRef.value.validate();
  if (!isValid) {
    return;
  }

  let bloodType = form.value.blood_type;

  if (bloodType === "Não informado") {
    bloodType = null;
  }
  let body = {
    id: patientStore.patient.id,
    name: form.value.name,
    birth_date: form.value.birth_date,
    cpf: form.value.cpf.replaceAll(".", "").replaceAll("-", ""),
    email: form.value.email,
    phone: form.value.phone
      .replaceAll("(", "")
      .replaceAll(")", "")
      .replaceAll(" ", "")
      .replaceAll("-", ""),
    weight: form.value.weight,
    height: form.value.height,
    gender: form.value.gender.value,
    blood_type: bloodType,
    smookes: form.value.smookes === false ? 0 : 1,
  };

  loading.value = true;
  const ok = await update(body);
  loading.value = false;

  if (ok) {
    showPositiveNotify("Dados do paciente salvos com sucesso!");
  } else {
    showNegativeNotify(
      "Ocorreu um erro ao salvar os dados do paciente, por favor tente novamente mais tarde!"
    );
  }
};

const onImageError = (event) => {
  event.target.src = DEFAULT_PICTURE;
};

const onFileChange = async (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      image.value = e.target.result; // Update the image source
    };
    reader.readAsDataURL(file); // Convert image file to Base64 URL
    await uploadPicture(file);
  }
};

const triggerFileInput = () => {
  fileInput.value.click();
};

const uploadPicture = async (file) => {
  const { status } = await uploadProfilePicture({
    id: patientStore.patient.id,
    file: file,
  });

  if (status) {
    showPositiveNotify("Foto atualizada com sucesso!");
  } else {
    showNegativeNotify(
      "Ocorreu um erro ao atualizar a foto, tente novamente mais tarde!"
    );
  }
};
</script>
