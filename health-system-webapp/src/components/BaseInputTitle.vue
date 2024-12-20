<template>
  <div class="input-title required">{{ title }}</div>
</template>
<script>
export default {
  name: "BaseInputTitle",
  props: {
    title: {
      type: String,
      required: false,
    },
  },
  methods: {},
};
</script>

<style>
.input-title {
  color: #364461;
  font-style: 14px;
  font-weight: 500;
}

.required:after {
  color: red;
  content: "*";
  margin-left: 4px;
}
</style>
