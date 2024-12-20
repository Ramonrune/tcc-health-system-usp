<template>
  <q-btn
    unelevated
    color="primary"
    class="add-button"
    type="submit"
    icon="fa-solid fa-add"
    size="14px"
    @click="onAdd"
  >
    <q-tooltip> {{ title }} </q-tooltip>
  </q-btn>
</template>
<script>
export default {
  name: "AddButton",
  props: {
    title: {
      type: String,
      required: false,
    },
    handleClick: {
      type: Function,
    },
  },
  methods: {
    onAdd() {
      this.handleClick();
    },
  },
};
</script>
<style>
.add-button {
  border-radius: 80px;
  width: 35px;
}
</style>
