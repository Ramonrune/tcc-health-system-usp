<template>
  <q-card ref="card" flat bordered class="card-main">
    <q-card-section class="card-header">
      <div class="ellipsis">
        <span>{{ props.label }}</span>
        <span class="timeframe-text">{{ props.timeframe }}</span>
      </div>
      <div class="row no-wrap q-gutter-x-sm">
        <slot name="options"></slot>
      </div>
    </q-card-section>
    <q-card-section class="">
      <slot></slot>
    </q-card-section>
  </q-card>
</template>

<script setup>
import { ref } from "vue";

const emits = defineEmits(["close"]);

const props = defineProps({
  label: { type: String, default: "" },
  timeframe: { type: String, default: "" },
});

const card = ref();
</script>

<style scoped lang="scss">
.card-main {
  border-radius: 10px 10px 0 0 !important;
  color: var(--Grey-800, #424242);
  font-family: Roboto;
  font-size: 14px;
  font-style: normal;
  font-weight: 500;
  line-height: 16px;
  letter-spacing: 0.15px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--Grey-300, #e0e0e0);

  height: 2.25rem;
  padding: 0 16px 0 16px;
}
.timeframe-text {
  font-size: 12px;
  font-weight: 300;
  margin-left: 0.5rem;
  color: #757575;
}
</style>
