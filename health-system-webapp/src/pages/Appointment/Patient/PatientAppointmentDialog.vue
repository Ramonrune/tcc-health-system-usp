<template>
  <q-dialog :value="value" persistent>
    <div class="dialog-center">
      <div class="title-container">
        <div class="title">{{ isEdit ? "Editar" : "Novo" }} atendimento</div>
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
            <BaseInputTitle title="Anotações" />
            <q-input
              filled
              v-model="annotation"
              label="Digite suas anotações"
              dense
              autogrow
              clearable
              :input-style="{ minHeight: '200px' }"
              :rules="[
                (val) => !!val || 'A anotação do atendimento é obrigatória',
              ]"
            />
            <q-btn
              no-caps
              unelevated
              :label="
                listening === false
                  ? 'Gravar atendimento por audio'
                  : 'Parar gravação'
              "
              icon="fa-solid fa-microphone"
              color="primary"
              type="submit"
              @click="listenAudio"
            />
          </div>
        </div>

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
            label="Salvar"
            icon="fa-solid fa-save"
            color="primary"
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
  getAppointment,
  register,
  update,
} from "src/service/AppointmentService";
import { usePatientStore } from "src/stores/PatientStore";
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

const annotation = ref("");

const isEdit = computed(() => props.id);

onMounted(async () => {
  if (isEdit.value) {
    loadingData.value = true;
    const appointment = await getAppointment({ id: props.id });

    annotation.value = appointment.annotation;

    loadingData.value = false;
  }
});

const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

// Configure recognition settings
recognition.lang = "pt-BR"; // Set language
recognition.interimResults = false; // Set to true for live updates of the transcript
recognition.continuous = true; // Keep listening until explicitly stopped
recognition.addEventListener("result", (event) => {
  const transcript = Array.from(event.results)
    .map((result) => result[0].transcript)
    .join("");

  annotation.value = transcript;
});

const listening = ref(false);
const listenAudio = async () => {
  if (listening.value === false) {
    recognition.start();
    listening.value = true;
  } else {
    recognition.stop();
    listening.value = false;
  }
};

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
      patient_id: patientStore.patient.id,
      annotation: annotation.value,
    };
    success = await update(body);

    success = true;
  } else {
    const body = {
      patient_id: patientStore.patient.id,
      annotation: annotation.value,
    };

    success = await register(body);
  }

  loading.value = false;

  if (success === false) {
    showNegativeNotify(
      "Ocorreu um erro ao salvar o atendimento, por favor tente novamente mais tarde!"
    );
  } else {
    showPositiveNotify("Dados do atendimento salvos com sucesso!");
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
