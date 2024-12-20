<script setup>
import { Recogito } from "@recogito/recogito-js";
import "@recogito/recogito-js/dist/recogito.min.css";
import { onMounted, ref, watch } from "vue";

const content = ref(null);
const props = defineProps({
  text: {
    type: String,
    required: true,
  },
  annotations: {
    type: Array,
    default: () => [
      {
        "@context": "http://www.w3.org/ns/anno.jsonld",
        type: "Annotation",
        body: [
          {
            type: "TextualBody",
            value: "aaaa",
            purpose: "commenting",
          },
        ],
        target: {
          selector: [
            {
              type: "TextQuoteSelector",
              exact: "bem",
            },
            {
              type: "TextPositionSelector",
              start: 10,
              end: 13,
            },
          ],
        },
        id: "#5e3f4769-f731-493e-91c1-7339a4c687d1",
      },
    ],
  },
});

const emit = defineEmits(["update:annotations"]);

var creatorFormatter = function (annotation) {
  if (annotation.creator === "http://example.org/user1") {
    return { style: "backgroundColor: red" };
  } else if (annotation.creator === "http://example.org/user1") {
    return { style: "backgroundColor: green" };
  } else {
    return { style: "backgroundColor: green" };
  }
};

const initRecogito = () => {
  const r = new Recogito({
    content: content.value,
    locale: "pt-BR",
    widgets: [{ widget: "COMMENT" }],
    formatter: creatorFormatter,
  });

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
  <div v-if="text" ref="content" v-html="text" />
</template>
