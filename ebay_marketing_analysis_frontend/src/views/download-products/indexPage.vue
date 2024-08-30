<template>
  <div>
    <div class="w-100 m-auto d-flex gap-4 p-4" style="background-color: white">
      <input placeholder="Please enter the text here." type="text" style="width: 40%;" v-model="data.scraping_url"
        class="analysis-input">
      <input placeholder="Notes" type="text" style="width: 15%;" v-model="data.notes" class="analysis-input">
      <div class="form-check form-switch pl-0 custom-switch d-flex gap-2 align-items-center">
        <input style="height: 1.7em; width: 4em;" class="form-check-input ms-1" v-model="data.both_listing" @click="() => {
          data.both_listing = !data.both_listing
        }" id="flexSwitchCheckDefault3" type="checkbox" />
        <label style="color: black" for="flexSwitchCheckDefault3">Select Both Category</label>
      </div>
      <button @click="callanalysisApi" class="btn btn-primary ml-auto">Download</button>
    </div>
  </div>
  <div style="background-color: white; margin-top: 1rem; padding-inline: 1rem;">
    <KTDatatable :table-data="result.results || []" :table-header="headerConfig" :loading="loading"
      :total="result.total_pages" :enable-items-per-page-dropdown="true" :rowsPerPage="rowsPerPage"
      :currentPage="currentPage" @current-change="current_change" @items-per-page-change="items_per_page_change">
      <template v-slot:cell-description="{ row: product }">
        <router-link @click="store.dispatch('handleproductLink', product?.notes)"
          :to="{ name: 'default.product-research' }">
          <p class="descrip-text">{{ product?.url }}</p>
        </router-link>
      </template>


      <template v-slot:cell-notes="{ row: product }">
        <p class=" btn-primary">{{ product?.notes }}</p>
      </template>
      <template v-slot:cell-status="{ row: product }">
        <p class="">{{ product?.status }}</p>
      </template>
      <template v-slot:cell-is_sold_listing="{ row: product }">
        <p v-if="product?.is_sold_listing" class="">Sold</p>
        <p v-else class="">Active</p>
      </template>
      <template v-slot:cell-action="{ row: product }">
        <button v-if="product?.status != 'Running'" @click="() => redownload_data = product" data-bs-toggle="modal"
          data-bs-target="#confirmation" class="btn btn-primary">Re-download</button>
      </template>
    </KTDatatable>
  </div>
  <div class="modal fade" id="confirmation" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Disclaimer !</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body ">
          <p class="text-black">Do you still want to re-download as this task is in 'pending' process</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-danger text-light" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="recallDownload(redownload_data)">Continue</button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import KTDatatable from '@/components/kt-datatable/KTDatatable.vue';
import { scraping_info, product_processes } from '@/service';
import { onMounted, ref } from 'vue';
import { toast } from 'vue3-toastify';
import { useStore } from 'vuex';
export default {
  components: { KTDatatable },

  setup() {
    const currentPage = ref(1)
    const result = ref('')
    const redownload_data = ref('')
    const store = useStore()
    const rowsPerPage = ref(10)
    const loading = ref(false)
    const list = ref([])
    const data = ref({
      scraping_url: '',
      both_listing: false,
      notes: ''
    })


    const current_change = async (page_number) => {
      loading.value = true
      currentPage.value = page_number
      product_processes(`?page=${page_number}&page_size=${rowsPerPage.value}`).then((response) => {
        result.value = response
        loading.value = false
      })
        .catch((error) => {
          toast.error(error, {
            autoClose: 2000
          })
        })
      loading.value = false
    }

    const items_per_page_change = (items_per_page) => {
      loading.value = true
      rowsPerPage.value = items_per_page
      product_processes(`?page_size=${items_per_page}`).then((response) => {
        result.value = response
        loading.value = false
      })
        .catch((error) => {
          toast.error(error, {
            autoClose: 2000
          })
        })
      loading.value = false
    }




    function recallDownload(value) {
      let copy = { ...value }
      copy.scraping_url = copy.url
      data.value = copy;
      callanalysisApi()
    }


    async function callProduct_process(value='') {
      product_processes(value).then((response) => {
        result.value = response
        rowsPerPage.value = result.value.page_size
      })
        .catch((error) => {
          toast.error(error, {
            autoClose: 2000
          })
        })
    }
    onMounted(async () => {
      await callProduct_process()
    })

    async function callanalysisApi() {

      try {
        const response = await scraping_info(data.value)

        if (response.message) {
          toast.success('Background job started, Please wait !', {
            autoClose: 2000
          })
          await callProduct_process(`?page=${currentPage.value}&page_size=${rowsPerPage.value}`)

        }
        else {
          toast.error('Something went wrong !', {
            autoClose: 2000
          })
        }
        for (let x in data?.value) {
          console.log(x)
          if (x == 'both_listing') {
            data.value[x] = false
          }
          else {
            data.value[x] = ''
          }
        }


      }
      catch (err) {
        console.log('Error in the api')
      }
    }


    const headerConfig = [

      {
        name: 'Description',
        key: 'description',
        sortable: false
      },
      {
        name: 'Notes',
        key: 'notes',
        sortable: false
      },
      {
        name: 'Status',
        key: 'status',
        sortable: false
      },
      {
        name: 'Listing Type',
        key: 'is_sold_listing',
        sortable: false
      },
      {
        name: 'Action',
        key: 'action',
        sortable: false
      }

    ]

    return {
      headerConfig,
      rowsPerPage,
      currentPage,
      data,
      callanalysisApi,
      list,
      result,
      recallDownload,
      current_change,
      items_per_page_change,
      loading,
      store,
      redownload_data
    }
  }
}
</script>

<style scoped>
input::placeholder {
  color: black;
}

.descrip-text {
  white-space: nowrap;
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.Category-Select {
  border-bottom: 1px solid black;
}

.analysis-input {
  border-bottom: 1px solid black;
}

:deep(.v-input__details) {
  display: none !important;
}

:deep(.v-field__input, .v-input > *) {
  color: black !important;
}

:deep(#my_date-input)::placeholder {
  color: black !important;
  font-weight: 600 !important;
  font-size: 17px;
}
</style>