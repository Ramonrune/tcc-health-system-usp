<template>
  <q-dialog :value="value" persistent>
    <div class="dialog-center">
      <div class="title-container">
        <div class="title">{{ isEdit ? "Editar" : "Novo" }} exame</div>
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
            <BaseInputTitle title="Nome do exame" />
            <q-input
              filled
              v-model="name"
              label="Digite o nome do exame"
              dense
              clearable
              :rules="[(val) => !!val || 'Nome é obrigatório']"
            />

            <BaseInputTitle title="Data do exame" />
            <q-input
              v-model="date"
              label="Data da realização do exame"
              type="date"
              filled
              dense
              :rules="[(val) => !!val || 'A data do exame é obrigatória']"
            />

            <BaseInputTitle title="Anotações" />
            <q-input
              filled
              v-model="note"
              label="Digite suas anotações"
              dense
              autogrow
              clearable
              :rules="[(val) => !!val || 'A anotação do exame é obrigatória']"
            />
          </div>

          <BaseInputTitle title="Anexo" />
          <q-file
            :loading="loadingData"
            filled
            bottom-slots
            v-model="file"
            label="Arquivo"
            accept=".jpg, .png, .png, .zip, .pdf"
            counter
            dense
            :rules="[(val) => !!val || 'Arquivo é obrigatório']"
          >
            <template v-slot:prepend>
              <q-icon name="cloud_upload" @click.stop.prevent />
            </template>

            <template v-slot:hint>
              Suporte a arquivos .pdf, .jpg, .png, .zip
            </template>
          </q-file>
        </div>

        <div class="row q-mt-md">
          <q-btn
            no-caps
            unelevated
            color="grey-4"
            class="col q-mr-sm text-black"
            label="Cancelar"
            icon="fa-solid fa-arrow-left"
            @click="onClose"
            type="submit"
          />

          <q-btn
            no-caps
            unelevated
            :loading="loading"
            label="Salvar"
            color="primary"
            icon="fa-solid fa-save"
            :disable="loadingData"
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
import {
  getExam,
  getExamDocumentFileFormat,
  register,
  update,
  uploadExamDocument,
} from "src/service/ExamService";
import { usePatientStore } from "src/stores/PatientStore";
import { convertDate } from "src/util/date";
import { showNegativeNotify, showPositiveNotify } from "src/util/plugins";
import { computed, onMounted, ref } from "vue";

const props = defineProps({
  value: {
    type: Boolean,
    default: () => true,
  },
  onSuccess: {
    type: Function,
  },
  onClose: {
    type: Function,
  },
  id: {
    type: String,
  },
});

const patientStore = usePatientStore();

const formRef = ref();
const loading = ref(false);
const loadingData = ref(false);

const name = ref("");
const date = ref("");
const note = ref("");
const file = ref();

const isEdit = computed(() => props.id);

onMounted(async () => {
  if (isEdit.value) {
    loadingData.value = true;
    const exam = await getExam({ id: props.id });
    name.value = exam.name;
    date.value = convertDate(exam.date);
    note.value = exam.note;
    file.value = await getExamDocumentFileFormat({ id: props.id });
    loadingData.value = false;
  }
});

const handleSubmit = async () => {
  const isValid = await formRef.value.validate();

  if (!isValid) {
    return;
  }

  loading.value = true;
  let success = false;

  if (props.id) {
    const body = {
      id: props.id,
      name: name.value,
      note: note.value,
      patient_id: patientStore.patient.id,
      date: date.value,
      file_extension: "." + file.value.name.split(".").pop(),
    };
    await update(body);

    await uploadExamDocument({
      id: props.id,
      file: file.value,
      patient_id: patientStore.patient.id,
      file_extension: "." + file.value.name.split(".").pop(),
    });

    success = true;
  } else {
    const body = {
      name: name.value,
      note: note.value,
      patient_id: patientStore.patient.id,
      date: date.value,
      file_extension: "." + file.value.name.split(".").pop(),
    };

    let id = await register(body);
    await uploadExamDocument({
      id: id,
      file: file.value,
      patient_id: patientStore.patient.id,
      file_extension: "." + file.value.name.split(".").pop(),
    });

    success = true;
  }

  loading.value = false;

  if (success === false) {
    showNegativeNotify(
      "Ocorreu um erro ao salvar o exame, por favor tente novamente mais tarde!"
    );
  } else {
    showPositiveNotify("Dados do exame salvos com sucesso!");
    props.onSuccess();
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
