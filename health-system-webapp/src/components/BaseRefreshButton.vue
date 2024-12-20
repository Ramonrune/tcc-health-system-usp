<template>
  <q-btn
    unelevated
    color="primary"
    class="refresh-button"
    type="submit"
    icon="fa-solid fa-refresh"
    size="14px"
    @click="onRefresh"
  >
    <q-tooltip> Atualizar </q-tooltip>
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
    onRefresh() {
      this.handleClick();
    },
  },
};
</script>
<style>
.refresh-button {
  border-radius: 80px;
  width: 35px;
}
</style>
