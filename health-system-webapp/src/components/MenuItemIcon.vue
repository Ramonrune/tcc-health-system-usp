<template>
  <q-icon
    v-if="icon === 'home'"
    name="fa-solid fa-house"
    size="24px"
    :style="'color: ' + currentColor"
  />

  <q-icon
    v-if="icon === 'patient'"
    name="fa-solid fa-hospital-user"
    size="24px"
    :style="'color: ' + currentColor"
  />

  <q-icon
    v-if="icon === 'appointment'"
    name="fa-solid fa-calendar-days"
    size="24px"
    :style="'color: ' + currentColor"
  />
</template>
<script setup>
import { ref, onMounted } from "vue";

// Define props
const props = defineProps({
  icon: {
    type: String,
    default: "",
  },
  active: {
    type: Boolean,
    default: false,
  },
});

const currentColor = ref("#000");

onMounted(() => {
  currentColor.value = props.active ? "#fff" : "#162238";
});
</script>
