<template>
  <q-item
    :class="
      route.path === link
        ? 'active-item q-mb-xs'
        : 'inactive-item rounded-borders q-mb-xs'
    "
    class="text-grey-10 text-weight-medium"
    clickable
  >
    <q-item-section side>
      <MenuItemColor
        :icon="icon"
        :active="route.path === link"
        :key="route.path"
      />
    </q-item-section>

    <q-item-section>
      <q-item-label
        :class="route.path === link ? 'active-text' : 'inactive-text'"
        >{{ label }}</q-item-label
      >
    </q-item-section>
  </q-item>
</template>

<script>
import MenuItemColor from "./MenuItemIcon.vue";
import { defineComponent } from "vue";
import { useRoute } from "vue-router";

export default defineComponent({
  name: "MenuItem",
  components: { MenuItemColor },

  props: {
    label: {
      type: String,
      required: true,
    },

    link: {
      type: String,
    },

    icon: {
      type: String,
      default: "",
    },

    size: {
      type: String,
      default: "16px",
    },

    color: {
      type: String,
      default: "black",
    },
  },

  setup() {
    const route = useRoute();

    return {
      route,
    };
  },
});
</script>
<style>
.active-item {
  border-radius: 8px;
  background: var(--q-primary) !important;
  display: flex;
  margin-left: 8px;
  margin-right: 8px;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
  align-self: stretch;
}

.inactive-item {
  margin-left: 8px;
  margin-right: 8px;
}

.active-text {
  color: var(--White-Color, #fff);

  /* subtitle2. */
  font-family: Roboto;
  font-size: 14px;
  font-style: normal;
  font-weight: 600;
  line-height: 21.98px; /* 157% */
  letter-spacing: 0.1px;
}

.inactive-text {
  color: var(--Quasar-Grey-10, #162238);

  /* body2. */
  font-family: Roboto;
  font-size: 14px;
  font-style: normal;
  font-weight: 600;
  line-height: 20.02px; /* 143% */
  letter-spacing: 0.15px;
}

.q-item-section {
  color: #8d8c89;
  text-decoration: none;
  font-weight: 500;
  -webkit-transition: all 0.2s ease-in-out;
  transition: all 0.2s ease-in-out;
}
</style>
