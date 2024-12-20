<template>
  <div>
    <q-input
      type="text"
      v-model:model-value="inputValue"
      :model-value="modelValue"
      label="Buscar"
      :debounce="debounce"
      color="primary"
      outlined
      dense
      @update:model-value="handleSearch"
    >
      <template #prepend>
        <q-icon name="fa-solid fa-search" size="14px" />
      </template>
    </q-input>
  </div>
</template>

<script>
export default {
  name: "BaseSearch",
  emits: ["update:modelValue"],
  data() {
    return {
      inputValue: "",
    };
  },
  props: {
    modelValue: { type: String, default: "" },
    showTopLabel: { type: Boolean, default: true },
    debounce: { type: Number, default: 500 },
  },
  methods: {
    handleSearch(val) {
      this.$emit("update:modelValue", val);
    },
  },
};
</script>
