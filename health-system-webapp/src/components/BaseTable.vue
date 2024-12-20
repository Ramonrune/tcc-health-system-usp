<template>
  <q-table
    flat
    class="table-sticky-header custom-table"
    :loading="loading"
    bordered
    :rows="rows"
    :columns="columns.filter((column) => column.visible)"
    :row-key="rowKey"
    :hide-pagination="hidePagination"
    :rows-per-page-options="rowsPerPageOptions"
  >
    <template v-slot:body-cell="props">
      <q-td :props="props">
        <div v-if="props.col.name === 'actions'">
          <q-btn
            v-if="actionColumns.includes('view')"
            flat
            padding="sm"
            size="10px"
            icon="fa-solid fa-eye"
            color="grey-7"
            @click="handleView(props.row)"
            class="q-mr-sm"
          >
            <q-tooltip>Visualizar</q-tooltip>
          </q-btn>

          <q-btn
            v-if="actionColumns.includes('download')"
            flat
            padding="sm"
            size="10px"
            icon="fa-solid fa-download"
            color="grey-7"
            @click="handleDownload(props.row)"
            class="q-mr-sm"
          >
            <q-tooltip>Download</q-tooltip>
          </q-btn>

          <q-btn
            v-if="actionColumns.includes('edit')"
            flat
            padding="sm"
            size="10px"
            icon="fa-solid fa-edit"
            color="grey-7"
            @click="handleEdit(props.row)"
            class="q-mr-sm"
          >
            <q-tooltip>Editar</q-tooltip>
          </q-btn>
          <q-btn
            v-if="actionColumns.includes('remove')"
            padding="sm"
            flat
            size="10px"
            icon="fa-solid fa-trash"
            color="grey-7"
            @click="handleDelete(props.row)"
          >
            <q-tooltip>Remover</q-tooltip>
          </q-btn>
        </div>
        <span v-else> {{ props.row[props.col.field] }}</span>
      </q-td>
    </template>
  </q-table>
</template>

<script setup>
const props = defineProps({
  rows: {
    type: Array,
    default: () => [],
  },
  columns: {
    type: Array,
    default: () => [],
  },
  rowKey: {
    type: String,
    default: "id",
  },
  hidePagination: {
    type: Boolean,
    default: true,
  },
  rowsPerPageOptions: {
    type: Array,
    default: () => [0],
  },
  loading: {
    type: Boolean,
    default: false,
  },
  onDeleteItem: {
    type: Function,
  },
  onUpdateItem: {
    type: Function,
  },
  onDownloadItem: {
    type: Function,
  },
  onViewItem: {
    type: Function,
  },
  actionColumns: {
    type: Array,
  },
});

function handleDelete(row) {
  props.onDeleteItem(row);
}

function handleEdit(row) {
  props.onUpdateItem(row);
}

function handleDownload(row) {
  props.onDownloadItem(row);
}

function handleView(row) {
  props.onViewItem(row);
}
</script>
