<template>
  <q-dialog :value="value" persistent>
    <div class="dialog-center">
      <div class="title-container">
        <div class="title">{{ isEdit ? "Editar" : "Nova" }} doença</div>
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
            <BaseInputTitle title="Selecione a doença" />
            <q-select
              filled
              v-model="model"
              use-input
              hide-selected
              fill-input
              input-debounce="0"
              dense
              label="Digite o nome da doença"
              class="q-mb-md"
              option-label="name"
              option-value="id"
              :options="options"
              @filter="filterFn"
              hint="Digite pelo menos 3 caracteres"
              :rules="[(val) => !!val || 'O nome é obrigatório']"
            >
              <template v-slot:no-option>
                <q-item>
                  <q-item-section class="text-grey">
                    Sem resultados
                  </q-item-section>
                </q-item>
              </template>
            </q-select>

            <BaseInputTitle title="Anotações" />
            <q-input
              filled
              v-model="note"
              label="Digite suas anotações"
              dense
              autogrow
              clearable
              :rules="[(val) => !!val || 'A anotação da doença é obrigatória']"
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
  getDisease,
  getDiseases,
  register,
  update,
} from "src/service/DiseaseService";
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

const note = ref("");
const model = ref(null);

const options = ref([]);

const isEdit = computed(() => props.id);

onMounted(async () => {
  if (isEdit.value) {
    loadingData.value = true;
    const disease = await getDisease({ id: props.id });

    options.value = [disease.disease];
    model.value = disease.disease;

    note.value = disease.note;

    loadingData.value = false;
  }
});

const filterFn = (val, update, abort) => {
  setTimeout(() => {
    update(async () => {
      if (val === "") {
        options.value = [];
      } else {
        const diseases = await getDiseases({ name: val.toLowerCase() });
        const needle = val.toLowerCase();
        options.value = diseases.filter(
          (v) => v.name.toLowerCase().indexOf(needle) > -1
        );
      }
    });
  }, 1500);
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
      disease_id: model.value.id,
      note: note.value,
    };
    success = await update(body);

    success = true;
  } else {
    const body = {
      patient_id: patientStore.patient.id,
      disease_id: model.value.id,
      note: note.value,
    };

    success = await register(body);
  }

  loading.value = false;

  if (success === false) {
    showNegativeNotify(
      "Ocorreu um erro ao salvar a doença, por favor tente novamente mais tarde!"
    );
  } else {
    showPositiveNotify("Dados da doença salvos com sucesso!");
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
