<script setup>
import { Recogito } from "@recogito/recogito-js";
import "@recogito/recogito-js/dist/recogito.min.css";
import { onMounted, readonly, ref, watch } from "vue";

const content = ref(null);
const props = defineProps({
  text: {
    type: String,
    required: true,
  },
  annotations: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(["update:annotations"]);

var creatorFormatter = function (annotation) {
  return annotation.underlying.category ? annotation.underlying.category : "";
};
const rec = ref();
const initRecogito = () => {
  const r = new Recogito({
    content: content.value,
    locale: "pt-BR",
    widgets: [{ widget: "COMMENT" }],
    formatter: creatorFormatter,
    readonly: true,
  });

  rec.value = r;

  watch(
    () => props.annotations,
    (newAnnotations) => {
      r.setAnnotations(newAnnotations);
    },
    { immediate: true }
  );

  r.on("createAnnotation", () => {
    console.log(r.getAnnotations());
    emit("update:annotations", r.getAnnotations());
  });

  r.on("updateAnnotation", () => {
    emit("update:annotations", r.getAnnotations());
  });

  r.on("deleteAnnotation", () => {
    emit("update:annotations", r.getAnnotations());
  });
};

onMounted(initRecogito);
</script>

<template>
  <div v-if="text" ref="content" class="analyze" v-html="text" />
</template>

<style>
.analyze {
  line-height: 48px;
  background: #efefef;
  padding: 16px;
  border-radius: 16px;
}

.r6o-editor {
  display: none !important;
}
</style>
