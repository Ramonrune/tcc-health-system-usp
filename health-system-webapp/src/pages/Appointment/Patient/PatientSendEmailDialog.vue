<template>
  <q-dialog :value="value" persistent full-width full-height>
    <div class="dialog-center" style="border-radius: 0px !important">
      <div class="title-container">
        <div class="title">Enviar e-mail</div>
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
            <BaseInputTitle title="Assunto" />
            <q-input
              filled
              v-model="subject"
              label="Digite o assunto"
              dense
              autogrow
              clearable
              :rules="[(val) => !!val || 'O assunto é obrigatório']"
            />

            <QuillEditor
              theme="snow"
              toolbar="full"
              ref="quillEditor"
              :rules="[(val) => !!val || 'A mensagem é obrigatória']"
              style="height: calc(100vh - 340px)"
            />
          </div>
        </div>
      </q-form>
      <div class="modal-footer">
        <div class="row q-mt-md">
          <q-btn
            no-caps
            unelevated
            color="grey-4"
            class="col q-mr-sm text-black"
            icon="fa-solid fa-arrow-left"
            label="Cancelar"
            @click="onClose"
            type="submit"
          />

          <q-btn
            no-caps
            unelevated
            :loading="loading"
            label="Enviar e-mail"
            icon="fa-solid fa-envelope"
            color="primary"
            type="submit"
            class="col"
            @click="handleSubmit()"
          />
        </div>
      </div>
    </div>
  </q-dialog>
</template>

<script setup>
import { QuillEditor } from "@vueup/vue-quill";
import "@vueup/vue-quill/dist/vue-quill.snow.css";

import BaseInputTitle from "src/components/BaseInputTitle.vue";
import {
  getAppointment,
  register,
  update,
} from "src/service/AppointmentService";
import { sendEmail } from "src/service/PatientService";
import { usePatientStore } from "src/stores/PatientStore";
import { showNegativeNotify, showPositiveNotify } from "src/util/plugins";
import { computed, onMounted, ref } from "vue";

const props = defineProps({
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
const quillEditor = ref();
const loading = ref(false);

const subject = ref("");

onMounted(async () => {});

const handleSubmit = async () => {
  const isValid = await formRef.value.validate();

  if (!isValid) {
    return;
  }

  const body = {
    id: patientStore.patient.id,
    subject: subject.value,
    html_content: quillEditor.value.getHTML(),
  };

  loading.value = true;

  let success = await sendEmail(body);

  loading.value = false;

  if (success === false) {
    showNegativeNotify(
      "Ocorreu um erro ao enviar o e-mail, por favor tente novamente mais tarde!"
    );
  } else {
    showPositiveNotify("E-mail enviado com sucesso!");
    props.onClose();
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

.modal-footer {
  position: fixed;
  bottom: 10px;
  right: 25px;
}
</style>
