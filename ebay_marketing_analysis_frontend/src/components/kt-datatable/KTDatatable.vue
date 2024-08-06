<template>
  <div class="dataTables_wrapper dt-bootstrap4 no-footer position-relative">
    <div class="table-responsive">
      <div class="row w-100 justify-content-end py-1">
      <div
        class=" w-100 d-flex align-items-center justify-content-end"
      >
      <!-- <input class=" mx-4 p-1 rounded-2" type="text"> -->
        <el-pagination
          v-model:current-page="pagination.page"
          :page-size="pagination.rowsPerPage"
          @current-change="currentPageChange"
          layout="prev, pager, next"
          :total='total*10'
          background
        >
        </el-pagination>
      </div>
    </div>
      <table
        :class="[loading && 'overlay overlay-block']"
        class="table align-middle table-row-dashed fs-6 gy-5 dataTable no-footer"
        id="kt_customers_table"
        role="grid"
      >
      
        <!--begin::Table head-->
        <thead>
          <!--begin::Table row-->
          <tr
            class="text-start text-gray-400 fw-bolder fs-7 text-uppercase gs-0"
            role="row"
          >
            <template v-for="(cell, i) in tableHeader" :key="i">
              <th
                @click="
                  sort(
                    cell.sortingField ? cell.sortingField : cell.key,
                    cell.sortable
                  )
                "
                :class="[
                  cell.name && '',
                  cell.sortable !== false && 'sorting',
                  tableHeader.length - 1 === i && 'text-end',
                  currentSort ===
                    `${cell.sortingField ? cell.sortingField : cell.key}desc` &&
                    'sorting_desc',
                  currentSort ===
                    `${cell.sortingField ? cell.sortingField : cell.key}asc` &&
                    'sorting_asc',
                ]"
                tabindex="0"
                rowspan="1"
                colspan="1"
                style="cursor: pointer"
              >
                {{ cell.name }}
              </th>
            </template>
          </tr>
          <!--end::Table row-->
        </thead>
        <!--end::Table head-->
        <!--begin::Table body-->
        <tbody class="fw-bold text-gray-600">
          <template v-if="getItems.length">
            <template v-for="(item, i) in getItems" :key="i">
              <tr class="odd">
                <template v-for="(cell, i) in tableHeader" :key="i">
                  <td :class="{ 'text-end': tableHeader.length - 1 === i }">
                    <slot :name="`cell-${cell.key}`" :row="item">
                      {{item[cell.key] }}
                    </slot>
                  </td>
                </template>
                <!--end::Item=-->
              </tr>
            </template>
          </template>
          <template v-else>
            <tr class="odd">
              <td colspan="8" class="dataTables_empty">
                {{ emptyTableText }}
              </td>
            </tr>
          </template>
        </tbody>
        <div
          v-if="loading"
          class="overlay-layer loader card-rounded bg-opacity-5"
        >
        <!-- bg-dark -->
          <div class="spinner-border spin-load text-primary mx-auto" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        <!--end::Table body-->
      </table>
    </div>

    <div class="row w-100 justify-content-end pt-3">
      <div
        class="col-sm-12 col-md-5 d-flex align-items-center justify-content-center justify-content-md-start"
      >
        <div
          v-if="enableItemsPerPageDropdown"
          class="dataTables_length"
          id="kt_customers_table_length"
        >
          <label
            ><select
              name="kt_customers_table_length"
              class="form-select form-select-sm form-select-solid"
              @change="setItemsPerPage"
            >
              <option value="10">10</option>
              <option value="25">25</option>
              <option value="50">50</option>
              <option value="100">100</option>
              <option value="500">500</option>
              <option value="1000">1000</option>
              <option value="2000">2000</option>
              <option value="3000">3000</option>
              <option value="4000">4000</option>
              <option value="5000">5000</option>
              <option value="10000">10000</option>
            </select></label
          >
        </div>
      </div>
      <div
        class=" d-flex align-items-center w-auto"
      >
      <el-pagination
      v-model:current-page="pagination.page"
      :page-size="pagination.rowsPerPage"
      @current-change="currentPageChange"
          :total="total*10"
          layout="prev, pager, next"
          background
        >
        </el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import arraySort from "array-sort";

import { computed, defineComponent, ref, onMounted, watch, getCurrentInstance } from "vue";

export default defineComponent({
  name: "kt-datatable",
  emits: ["current-change", "sort", "items-per-page-change"],
  props: {
    tableHeader: {
      type: Array,
      required: true,
    },
    tableData: { type: Array, required: true },
    emptyTableText: { type: String, default: "No data found" },
    loading: { type: Boolean, default: false },
    currentPage: { type: Number, default: 1 },
    enableItemsPerPageDropdown: { type: Boolean, default: true },
    total: { type: Number, default: 0 },
    rowsPerPage: { type: Number, default: 10 },
    order: { type: String, default: "asc" },
    sortLabel: { type: String, default: "" },
  },
  setup(props, { emit }) {
    const data = ref(props.tableData);
    const currentSort = ref("");
    const order = ref(props.order);
    const label = ref(props.sortLabel);
    const pagination = ref({
      page: 1,
      rowsPerPage: props.rowsPerPage,
    });

    const vnodeProps = getCurrentInstance().vnode.props || {};
    watch(
      () => props.tableData,
      (first) => {
        data.value = first;
        pagination.value.page = props.currentPage;
        pagination.value.rowsPerPage = props.rowsPerPage;
      }
    );
    onMounted(() => {
      currentSort.value = label.value + order.value;
      pagination.value.page = props.currentPage ? props.currentPage : 1;
      pagination.value.rowsPerPage = props.rowsPerPage;
    });

    const getItems = computed(() => {
      if ("onCurrentChange" in vnodeProps) {
        return data.value;
      } else {
        const clone = JSON.parse(JSON.stringify(data.value));
        const startFrom =
          pagination.value.page * pagination.value.rowsPerPage -
          pagination.value.rowsPerPage;
        return clone.splice(startFrom, pagination.value.rowsPerPage);
      }
    });

    const currentPageChange = (val) => {
      emit("current-change", val);
    };

    const sort = (columnName, sortable) => {
      if (sortable === false) {
        return;
      }

      if ("onSort" in vnodeProps) {
        if (order.value === "asc") {
          order.value = "desc";
          emit("sort", { columnName: columnName, order: "desc" });
        } else {
          order.value = "asc";
          emit("sort", { columnName: columnName, order: "asc" });
        }
      } else {
        if (order.value === "asc") {
          order.value = "desc";
          arraySort(data.value, columnName, { reverse: false });
        } else {
          order.value = "asc";
          arraySort(data.value, columnName, { reverse: true });
        }
      }
      currentSort.value = columnName + order.value;
    };

    const setItemsPerPage = (event) => {
      emit("items-per-page-change", parseInt(event.target.value));
    };

    return {
      pagination,
      currentPageChange,
      getItems,
      sort,
      currentSort,
      setItemsPerPage,
    };
  },
});
</script>

<style scoped>
table.dataTable {
  clear: both;
  margin-top: 6px !important;
  margin-bottom: 6px !important;
  max-width: none !important;
  border-collapse: separate !important;
  border-spacing: 0;
}

table.dataTable > thead th.sorting {
  position: relative;
}

table.dataTable > thead th.sorting:after {
  position: absolute;
}

.el-pagination.is-background .btn-next,
.el-pagination.is-background .btn-prev,
.el-pagination.is-background .el-pager li {
  background: none;

  border-radius: 0.475rem;
  font-weight: 500;
  font-size: 1.075rem;
  font-family: Poppins, Helvetica, sans-serif;
}
.el-pagination.is-background .el-pager li:not(.disabled):hover{
  color: #97989a;
}
.el-pagination.is-background .el-pager li:not(.disabled).active {
  background-color: #4CBC9A;
}
.el-pagination.is-background .el-pager li:not(.disabled).active:hover {
  color: white;
}
.el-pagination.is-background .btn-next:hover,
.el-pagination.is-background .btn-prev:hover{
color:#4CBC9A;
}
table.dataTable td.dataTables_empty,
table.dataTable th.dataTables_empty {
  text-align: center;
}

div.dataTables_wrapper div.dataTables_processing {
  position: absolute;
  top: 50%;
  left: 50%;
}
.loader{
  width: 100%;
  height: 100%;
  backdrop-filter: blur(5px)  ;
  position: absolute;
  top: 0;
}
.spin-load{
width: 100px;
height: 100px;
font-size: xx-large;
position: relative;
top: 50%;
left: 50%;
}

</style>
