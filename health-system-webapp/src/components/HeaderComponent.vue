<template>
  <div class="header">
    <div class="inline-breadcrumbs">
      <div class="header-title">
        <div v-for="(breadcrumb, key, index) of breadcrumbs" :key="index">
          <span
            :class="key === 0 ? 'breadcrumb-title-active' : 'breadcrumb-title'"
          >
            <span class="q-pr-xm">{{ breadcrumb.label }}</span>
          </span>
        </div>
      </div>

      <div class="right-content">
        <slot name="right-content"></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  breadcrumbs: Object,
});
</script>

<style scoped>
.header {
  border-bottom: 1px solid var(--Blue-Gray-A100, #cfd8dc);
  background: var(--Grey-50, #fafafa);
  padding-left: 16px;
  padding-top: 8px;
  padding-bottom: 8px;
}
.inline-breadcrumbs {
  display: flex;
}

.header-title {
  flex: 1;
  display: flex;
}
.breadcrumb-title {
  color: var(--Grey-800, #424242);
  font-family: Roboto;
  font-size: 16px;
  font-style: normal;
  font-weight: 400;
  line-height: 32px; /* 200% */
}

.breadcrumb-title-active {
  color: var(--primary-color);
  font-family: Roboto;
  font-size: 16px;
  font-style: normal;
  font-weight: 700;
  line-height: 32.016px;
}

.arrow-right {
  position: relative;
  top: 5px;
}

.right-content {
  display: flex;
}
</style>
