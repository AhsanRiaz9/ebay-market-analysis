<template>
  <table :class="'table ' + className" ref="tableRef"></table>
</template>

<script setup>
import { onMounted, ref, defineProps } from 'vue'
import 'datatables.net-bs5/css/dataTables.bootstrap5.min.css'
import 'datatables.net-bs5/js/dataTables.bootstrap5.min.js'
import 'datatables.net-bs5'
import $ from 'jquery'
import mitt from 'mitt'
const emitter = mitt()
const props = defineProps({
  data: Array,
  columns: Array,
  options: Object,
  className: String,
  isFooter: { type: String },
  isColumnFilter: { type: String },
  isToggleFilter: { type: String },
  isLanguageFilter: { type: String }
})
const fetchData = () => {
  const transformedData = props.data.map(item => Object.values(item));
  const table = $(tableRef.value).DataTable({
    autoWidth: false,
    data: transformedData,
    columns: props.columns,
    dom: '<"row align-items-center"<"col-md-6" l><"col-md-6" f>><"table-responsive my-3" rt><"row align-items-center" <"col-md-6" i><"col-md-6" p>><"clear">',
    lengthMenu: [5,10, 25, 50, 100],
    pageLength: 10,
    pagingType : 'simple_numbers',
    destroy: true,
    initComplete: () => {
      if (props.isFooter) {
        const footerRow = document.createElement('tr')
        props.columns.forEach((column) => {
          const footerCell = document.createElement('th')
          const input = column.title
          footerCell.append(input)
          footerRow.append(footerCell)
        })

        $(tableRef.value).append($('<tfoot>').append(footerRow))
      }
    }
  })
  const pageInfo = table.page.info();
const currentPage = pageInfo.page + 1; // DataTables uses zero-based indexing, so add 1 to get the current page number
console.log("Current page:", currentPage);
  emitter.on('hook:beforeDestroy', function () {
    table.destroy()
  })
}

const tableRef = ref(null)

onMounted(fetchData)
</script>

Was this response better or worse? Better Worse Same

<style scoped lang="css">
@import 'datatables.net-bs5/css/dataTables.bootstrap5.min.css';
</style>
