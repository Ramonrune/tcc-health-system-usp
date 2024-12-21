<template>
  <q-dialog :value="value" persistent full-width full-height>
    <div class="dialog-center" style="border-radius: 0px !important">
      <div class="title-container">
        <div class="title">Análise do atendimento</div>
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
      <div class="row q-col-gutter-md">
        <div class="col-8">
          <div class="text-h6 text-bold">Resumo geral do atendimento</div>

          <div class="text-h7 text-bold q-pb-sm q-mt-md">Dados gerais</div>
          <q-separator />

          <div class="row q-col-gutter-lg q-mt-xs q-mb-lg">
            <div class="column flex-center no-wrap q-gutter-y-xs ellipsis">
              <div
                class="colored-box"
                style="background-color: rgb(230, 240, 255)"
              >
                <q-icon
                  name="fa-solid fa-person-cane"
                  size="24px"
                  style="color: rgb(33, 64, 125)"
                />
              </div>
              <div class="text-1">{{ getItem("Age") }}</div>
              <div class="text-2">Idade</div>
            </div>

            <div class="column flex-center no-wrap q-gutter-y-xs ellipsis">
              <div
                class="colored-box"
                style="background-color: rgb(230, 240, 255)"
              >
                <q-icon
                  name="fa-solid fa-calendar"
                  size="24px"
                  style="color: rgb(33, 64, 125)"
                />
              </div>
              <div class="text-1">{{ getItem("Date") }}</div>
              <div class="text-2">Data</div>
            </div>
          </div>

          <div class="text-h7 text-bold q-pb-sm q-mt-md">Diagnósticos</div>
          <q-separator />

          <div class="row q-col-gutter-md q-mt-xs q-mb-lg">
            <div
              class="column flex-center no-wrap q-gutter-y-xs ellipsis"
              v-for="item in getItems('Diagnosis')"
              :key="item"
            >
              <div
                class="colored-box"
                style="background-color: rgb(255, 247, 232)"
              >
                <q-icon
                  name="fa-solid fa-disease"
                  size="24px"
                  style="color: rgb(238, 127, 0)"
                />
              </div>
              <div class="text-1">{{ item }}</div>
              <div class="text-2">Diagnóstico</div>
            </div>
          </div>

          <div class="text-h7 text-bold q-pb-sm q-mt-md">Tratamentos</div>
          <q-separator />

          <div class="row q-col-gutter-md q-mt-xs q-mb-lg">
            <div
              class="column flex-center no-wrap q-gutter-y-xs ellipsis"
              v-for="item in getItems('TreatmentName')"
              :key="item"
            >
              <div
                class="colored-box"
                style="background-color: rgb(231, 238, 254)"
              >
                <q-icon
                  name="fa-solid fa-hospital"
                  size="24px"
                  style="color: rgb(0, 71, 238)"
                />
              </div>
              <div class="text-1">{{ item }}</div>
              <div class="text-2">Nome do tratamento</div>
            </div>
          </div>

          <div class="text-h7 text-bold q-pb-sm q-mt-md">Anotações</div>
          <q-separator class="q-mb-md" />
          <BaseTextAnnotation
            :text="annotation"
            :annotations="textNotes"
            v-if="annotation"
          />
        </div>

        <div class="col-4">
          <div class="text-h7 text-bold q-pb-sm q-mt-md">
            Dados identificados
          </div>

          <q-separator />

          <div
            v-for="entity in entities"
            :key="entity.id"
            class="q-mb-sm q-mt-sm"
          >
            <div>
              <strong>Dado:</strong>
              {{ translateCategoryToPortuguese(entity.category) }}
            </div>
            <div><strong>Texto:</strong> {{ entity.entity_text }}</div>
            <div class="q-mb-sm">
              <strong>Confiança:</strong> {{ entity.confidence }}
            </div>

            <q-separator />
          </div>
        </div>
      </div>
    </div>
  </q-dialog>
</template>

<script setup>
import BaseInputTitle from "src/components/BaseInputTitle.vue";
import BaseTextAnnotation from "src/components/BaseTextAnnotation.vue";
import {
  getAppointment,
  getAppointmentEntities,
} from "src/service/AppointmentService";
import { usePatientStore } from "src/stores/PatientStore";
import { nextTick, onMounted, ref } from "vue";

const props = defineProps({
  value: {
    type: Boolean,
    default: () => true,
  },
  onClose: {
    type: Function,
  },
  id: {
    type: String,
  },
});

const patientStore = usePatientStore();

const loadingData = ref(false);

const annotation = ref("");
const textNotes = ref([]);
const entities = ref([]);

const getItems = (item) => {
  let vals = entities.value.filter((e) => e.category === item);
  vals = vals.filter((e) => e.confidence > 0.95);
  return vals.map((e) => e.entity_text.toLowerCase());
};

const getItem = (item) => {
  let vals = entities.value.filter((e) => e.category === item);

  if (vals.length > 0) {
    return vals[0].entity_text.toLowerCase();
  }

  return "Não disponível";
};

const translateCategoryToPortuguese = (category) => {
  const translations = {
    AdministrativeEvent: "Evento Administrativo",
    Age: "Idade",
    Allergen: "Alergeno",
    BodyStructure: "Estrutura Corporal",
    CareEnvironment: "Ambiente De Cuidados",
    ConditionQualifier: "Qualificador De Condição",
    ConditionScale: "Escala De Condição",
    Course: "Curso",
    Date: "Data",
    Diagnosis: "Diagnóstico",
    Direction: "Direção",
    Dosage: "Dosagem",
    Employment: "Emprego",
    Ethnicity: "Etnia",
    ExaminationName: "Nome Do Exame",
    Expression: "Expressão",
    FamilyRelation: "Parentesco",
    Frequency: "Frequência",
    Gender: "Gênero",
    GeneOrProtein: "Gene Ou Proteína",
    HealthcareProfession: "Profissão De Saúde",
    LivingStatus: "Estado De Vida",
    MeasurementUnit: "Unidade De Medida",
    MeasurementValue: "Valor De Medida",
    MedicationClass: "Classe De Medicação",
    MedicationForm: "Forma De Medicação",
    MedicationName: "Nome Da Medicação",
    MedicationRoute: "Via De Administração",
    MutationType: "Tipo De Mutação",
    RelationalOperator: "Operador Relacional",
    SubstanceUse: "Uso De Substância",
    SubstanceUseAmount: "Quantidade De Uso De Substância",
    SymptomOrSign: "Sintoma Ou Sinal",
    Time: "Tempo",
    TreatmentName: "Nome Do Tratamento",
    Variant: "Variante",
  };

  return translations[category] || category;
};

onMounted(async () => {
  loadingData.value = true;
  let [appointment, entits] = await Promise.all([
    getAppointment({ id: props.id }),
    getAppointmentEntities({ id: props.id }),
  ]);

  annotation.value = appointment.annotation;

  entits = entits.sort((a, b) => {
    const categoryA = a.category.toLowerCase();
    const categoryB = b.category.toLowerCase();
    return categoryA < categoryB ? -1 : categoryA > categoryB ? 1 : 0;
  });

  let notes = [];
  for (let entity of entits) {
    notes.push({
      category: entity.category,
      "@context": "http://www.w3.org/ns/anno.jsonld",
      type: "Annotation",
      body: [
        {
          type: "TextualBody",
          value: entity.entity_text,
          purpose: "commenting",
        },
      ],
      target: {
        selector: [
          {
            type: "TextQuoteSelector",
            exact: "simply",
          },
          {
            type: "TextPositionSelector",
            start: entity.offset - 1,
            end: entity.offset + entity.entity_text.length,
          },
        ],
      },
      id: entity.id,
    });
  }

  entities.value = entits;
  textNotes.value = notes;

  loadingData.value = false;
});
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

.colored-box {
  width: 48px;
  height: 48px;
  border-radius: 8px;

  display: flex;
  align-items: center;
  justify-content: center;
}

.text-1 {
  color: var(--Quasar-Grey-10, #162238);
  text-align: center;
  font-size: 14px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px;
}

.text-2 {
  color: var(--Quasar-Grey-Blue-08, #455a64);
  text-align: center;
  font-size: 12px;
  font-weight: 400;
  line-height: 12px;
}
</style>
