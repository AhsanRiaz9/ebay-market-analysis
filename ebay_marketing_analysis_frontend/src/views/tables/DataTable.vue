<template>
  <div class="row">
    <div class="col-sm-12">
      <div class="card">
        <div class="card-header d-flex justify-content-between">
          <div class="header-title">
            <h4 class="card-title">Bootstrap Datatables</h4>
          </div>
        </div>
        <div class="card-body">
          <p>Images in Bootstrap are made responsive with <code>.img-fluid</code>. <code>max-width: 100%;</code> and <code>height: auto;</code> are applied to the image so that it scales with the parent element.</p>
          <div class="table-responsive border-bottom my-3">
            <data-table v-if="list && list.results" :data= "list && list.results ? list.results : []" :columns="DataTableOptions.columns" isFooter="bootstrap-data-table" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import DataTable from '@/components/DataTable.vue'
import {ref } from 'vue';
export default{
  props:{list:Array},
  components:{
DataTable
  },
  setup (){
    const data = ref([])
    const DataTableOptions = {columns: [{ title: 'Name' }, { title: 'Contact' }, { title: 'Email' }, { title: 'Role' }, { title: 'Actions' }],}
return {
  DataTableOptions,
  data
}
  }
}
</script>
