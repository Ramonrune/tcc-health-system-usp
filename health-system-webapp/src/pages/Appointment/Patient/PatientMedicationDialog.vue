<template>
  <q-dialog :value="value" persistent>
    <div class="dialog-center">
      <div class="title-container">
        <div class="title">{{ isEdit ? "Editar" : "Novo" }} medicamento</div>
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
            <BaseInputTitle title="Selecione o medicamento" />
            <q-select
              filled
              v-model="model"
              use-input
              hide-selected
              fill-input
              input-debounce="0"
              class="q-mb-md"
              dense
              label="Selecione o nome do medicamento"
              option-label="name"
              option-value="id"
              :options="options"
              @filter="filterFn"
              hint="Digite pelo menos 3 caracteres"
              :rules="[(val) => !!val || 'O medicamento é obrigatório']"
            >
              <template v-slot:no-option>
                <q-item>
                  <q-item-section class="text-grey">
                    Sem resultados
                  </q-item-section>
                </q-item>
              </template>
              <template v-slot:option="scope">
                <q-item v-bind="scope.itemProps">
                  <q-item-section>
                    <q-item-label>{{ scope.opt.name }}</q-item-label>
                    <q-item-label caption
                      >{{ scope.opt.lab }} CNPJ:
                      {{ scope.opt.lab_cnpj }}</q-item-label
                    >
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
              :rules="[
                (val) => !!val || 'A anotação do medicamento é obrigatória',
              ]"
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
  getMedication,
  getMedications,
  register,
  update,
} from "src/service/MedicationService";
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
    const medication = await getMedication({ id: props.id });

    options.value = [medication.medication];
    model.value = medication.medication;

    note.value = medication.note;

    loadingData.value = false;
  }
});

const filterFn = (val, update, abort) => {
  setTimeout(() => {
    update(async () => {
      if (val === "") {
        options.value = [];
      } else {
        const medications = await getMedications({ name: val.toLowerCase() });
        const needle = val.toLowerCase();
        options.value = medications.filter(
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
      medication_id: model.value.id,
      note: note.value,
    };
    success = await update(body);

    success = true;
  } else {
    const body = {
      patient_id: patientStore.patient.id,
      medication_id: model.value.id,
      note: note.value,
    };

    success = await register(body);
  }

  loading.value = false;

  if (success === false) {
    showNegativeNotify(
      "Ocorreu um erro ao salvar o medicamento, por favor tente novamente mais tarde!"
    );
  } else {
    showPositiveNotify("Dados do medicamento salvos com sucesso!");
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
