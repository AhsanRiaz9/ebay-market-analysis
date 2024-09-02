<template>
  <div>
    
    <div class="w-100 p-2 rounded-2 d-flex align-items-center px-4 main-head" style="background-color: white">
      <div class="w-25">
        <p class="platform">eBay</p>
      </div>
      <div class="w-50 d-flex align-items-center">
        <div class="searchbox"><search-icon /> <input @input="!toggle && searchdataApi()" v-model="searchKeyword" type="text"
            placeholder="Search" class="searchbar" /></div>
        <div></div>
      </div>
      <!-- <button class="searchbtn">Search</button> -->
    </div>
    <div class="row" style="gap: 30px 0; background-color: white; margin-block: 25px; padding: 20px">
      <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
        <div class="section">
          <div class="d-flex justify-content-between">
            <div></div>
            <h6 class="fw-semibold">Marketplace</h6>
            <exclamation-circle-icon />
          </div>
          <v-select v-model="data.name" clearable class="selectinput" label="Select marketplace"
            :items="['ebay.com.au']" @update:modelValue=" !toggle && callproductsApi()" variant="underlined"></v-select>
        </div>
      </div>
      <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
        <div class="section">
          <div class="d-flex justify-content-between">
            <div></div>
            <h6 class="fw-semibold">Shipping location</h6>
            <exclamation-circle-icon />
          </div>
          <v-select clearable class="selectinput" v-model="data.shippingLocation" label="Select shipping location"
            :items="['Australia']" variant="underlined" @update:modelValue=" !toggle && callproductsApi()"></v-select>
        </div>
      </div>
      <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
        <div class="section">
          <div class="d-flex justify-content-between">
            <div></div>
            <h6 class="fw-semibold">Data category</h6>
            <exclamation-circle-icon />
          </div>
          <v-select class="selectinput" v-model="data.dataCategory" label="Select data category"
            :items="['Active', 'Sold']" variant="underlined" @update:modelValue=" !toggle && callproductsApi()"></v-select>
        </div>
      </div>
      <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
        <div class="section">
          <div class="d-flex justify-content-between">
            <div></div>
            <h6 class="fw-semibold">Price</h6>
            <exclamation-circle-icon />
          </div>
          <div class="mt-auto gap-2 d-flex justify-content-around align-items-center px-4 pb-3">
            <div class="w-50">
              <input @change=" !toggle && checkPrice()" v-model="data.minPrice" type="number" class="pricerangeinput" />
              <b class="text-center mx-auto d-block">Min</b>
            </div>
            <div class="w-50">
              <input @change=" !toggle && checkPrice()" v-model="data.maxPrice" type="number" class="pricerangeinput" />
              <b class="text-center mx-auto d-block">Max</b>
            </div>
          </div>
        </div>
      </div>
      <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
        <div class="section">
          <div class="d-flex justify-content-between">
            <div></div>
            <h6 class="fw-semibold">Sale date range</h6>
            <exclamation-circle-icon />
          </div>

          <VueCtkDateTimePicker id="my_date" range :format="'YYYY-MM-DD'" formatted="YYYY-MM-DD" :onlyDate="true"
            color="#3a57e8" noTime="true" :custom-shortcuts="custom_shortcuts" v-model="date"
            @update:modelValue="!toggle && changeDateformat()" />
        </div>
      </div>
      <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
        <div class="section">
          <div input class="d-flex justify-content-between">
            <div></div>
            <h6 class="fw-semibold">Exclude phrase</h6>
            <exclamation-circle-icon />
          </div>
          <input class="pt-5 mt-2 exclude-phrase" v-model="data.excludedPhrase" @input=" !toggle && callproductsApi()"
            style="border-bottom: 2px solid black" placeholder="Comma separated phrase" type="text" />
        </div>
      </div>
      <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
        <div class="section">
          <div class="d-flex justify-content-between">
            <div></div>
            <h6 class="fw-semibold">Category</h6>
            <exclamation-circle-icon />
          </div>
          <v-select class="selectinput" v-model="data.categories" label="Select category"  :items="category  ? category?.map(items => ({ name: items?.name || items?.name, id: items?.ebay_category_id || items?.ebay_category_id })) : []"
            item-title="name" item-value="id"
            variant="underlined" @update:modelValue=" !toggle && callproductsApi()"></v-select>
        </div>
      </div>
      <div v-for="(item, index) in productfilter" :key="index" class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
        <div class="section" v-if="productfilter">
          <div class="d-flex justify-content-between">
            <div></div>
            <h6 class="fw-semibold">{{ index.charAt(0).toUpperCase() + index.slice(1) }}</h6>
            <v-tooltip v-if="index == 'product_models'" location='top'
              text="product Models can only be visible once category has been selected">
              <template v-slot:activator="{ props }">
                <exclamation-circle-icon v-bind="props" />
              </template>
            </v-tooltip>
            <exclamation-circle-icon v-else />
          </div>
          
          <v-autocomplete v-if="index != 'product_models'" style="font-weight: 700;" multiple v-model="data[index]" @update:modelValue=" !toggle && callproductsApi()"
            class="selectinput" clearable :label="index?.charAt(0).toUpperCase() + index?.slice(1)"
            :items="item && item?.map((items) => ({ name: items?.name || items?.value, id: items?.ebay_condition_id || items?.id }))"
            item-title="name" item-value="id" variant="underlined"></v-autocomplete>
          <v-autocomplete v-else-if="index == 'product_models' && data.categories" style="font-weight: 700;" multiple v-model="data[index]" @update:modelValue=" !toggle && callproductsApi()"
            class="selectinput" clearable :label="index?.charAt(0).toUpperCase() + index?.slice(1)"
            :items="item && item?.map((items) => ({ name: items?.name || items?.value, id: items?.ebay_condition_id || items?.id }))"
            item-title="name" item-value="id" variant="underlined"></v-autocomplete>
        </div>
      </div>

      <div class="form-check form-switch pl-0 custom-switch d-flex gap-2 align-items-center pt-3">
      <label style="color: black" for="flexSwitchCheckDefault3">Auto Search</label>
        <input style="height: 1.7em; width: 4em;" class="form-check-input ms-1 m-0" v-model="toggle" @click="() => {
         toggle = !toggle
        }" id="flexSwitchCheckDefault3" type="checkbox" />
        <label style="color: black" for="flexSwitchCheckDefault3">Manual Search</label>
      </div>
      <div v-if="toggle" class="d-flex"><button @click="manualSearch()" class="btn btn-primary ml-auto">Apply</button></div>



     
      <div v-if="data.dataCategory == 'Active'"
        class="w-100 position-relative rounded-3 stats p-4 d-flex justify-content-evenly">
        <div v-if="loading" class="skeleton d-flex"></div>
        <div class="d-flex gap-3">
          <div>
            <h5>${{ analytics?.avg_price }}</h5>
            <p style="font-size: 11px; display: inline; margin-right: 10px">Avg. active price</p>

            <v-tooltip location='top'
              text="The mean active price per item for similar listings, not including postage costs.">
              <template v-slot:activator="{ props }">
                <exclamation-circle-icon v-bind="props" />
              </template>
            </v-tooltip>
          </div>
          <div>
            <h5> ${{ analytics?.min_price }} - ${{ analytics?.max_price }}</h5>
            <p style="font-size: 11px; display: inline; margin-right: 10px">Active price range</p>
            <v-tooltip location='top'
              text="The minimun and maximum active price for similar lisitng, not including postage costs. ">
              <template v-slot:activator="{ props }">
                <exclamation-circle-icon v-bind="props" />
              </template>
            </v-tooltip>
          </div>
        </div>
        
        <div class="vertical-line"></div>
        <div class="d-flex gap-3">
          <div>
            <h5>${{ analytics?.avg_postage }}</h5>
            <p style="font-size: 11px; display: inline; margin-right: 10px">Avg. postage</p>
            <v-tooltip location='top'
              text="The average postage cost to be paid by the buyer this average doesn't include listings with free postage.">
              <template v-slot:activator="{ props }">
                <exclamation-circle-icon v-bind="props" />
              </template>
            </v-tooltip>
          </div>
          <div>
            <h5>{{analytics?.free_postage }}%</h5>
            <p style="font-size: 11px; display: inline; margin-right: 10px">Free postage</p>
            <v-tooltip location='top' text="The percentage of sale that included free postage.">
              <template v-slot:activator="{ props }">
                <exclamation-circle-icon v-bind="props" />
              </template>
            </v-tooltip>
          </div>
        </div>
        <div class="vertical-line"></div>
        <div class="d-flex gap-3">
          <div>
            <h5>{{ records }}</h5>
            <p style="font-size: 11px; margin-top: 10px">Total active listing</p>
          </div>
        </div>
      </div>
      <div v-if="data.dataCategory == 'Sold'"
        class="w-100 position-relative rounded-3 stats p-4 d-flex justify-content-evenly">
        <div v-if="loading" class="skeleton d-flex"></div>
        <div class="d-flex gap-3">
          <div>
            <h5>${{ analytics?.avg_price }}</h5>
            <p style="font-size: 11px;display:inline;margin-right: 10px">Avg. sold price</p>
            <v-tooltip location='top'
              text="The mean sold price per item for similar listings, not including postage costs.">
              <template v-slot:activator="{ props }">
                <exclamation-circle-icon v-bind="props" />
              </template>
            </v-tooltip>
          </div>
          <div>
            <h5>${{ analytics?.min_price }} - ${{ analytics?.max_price }}</h5>
            <p style="font-size: 11px; display: inline; margin-right: 10px">Sold price range</p>
            <v-tooltip location='top'
              text="The minimun and maximum sold price for similar lisitng, not including postage costs. ">
              <template v-slot:activator="{ props }">
                <exclamation-circle-icon v-bind="props" />
              </template>
            </v-tooltip>
          </div>
        </div>
        <div class="vertical-line"></div>
        <div class="d-flex gap-3">
          <div>
            <h5>${{ analytics?.avg_postage }}</h5>
            <p style="font-size: 11px; display: inline; margin-right: 10px">Avg. postage</p>
            <v-tooltip location='top'
              text="The average postage cost to be paid by the buyer this average doesn't include listings with free postage.">
              <template v-slot:activator="{ props }">
                <exclamation-circle-icon v-bind="props" />
              </template>
            </v-tooltip>

          </div>
          <div>
            <h5>{{ analytics?.free_postage }}%</h5>
            <p style="font-size: 11px; display: inline; margin-right: 10px">Free postage</p>
            <v-tooltip location='top' text="The percentage of sale that included free postage.">
              <template v-slot:activator="{ props }">
                <exclamation-circle-icon v-bind="props" />
              </template>
            </v-tooltip>
          </div>
        </div>
        <div class="vertical-line"></div>
        <div class="d-flex gap-3">
          <div>
            <h5>{{ records }}</h5>
            <p style="font-size: 11px; margin-top: 6px;">Total sold listing</p>
          </div>
          <div>
            <h5>{{ analytics?.sell_through }}%</h5>
            <p style="font-size: 11px; display: inline; margin-right: 10px">Sell through rate</p>
            <v-tooltip location='top' text="The percentage of similar items that sold. 
            Formula : (sold/active)*100
            ">
              <template v-slot:activator="{ props }">
                <exclamation-circle-icon v-bind="props" />
              </template>
            </v-tooltip>
          </div>
        </div>
      </div>


      <div class="py-3" style="background-color: white">
        <KTDatatable :enable-items-per-page-dropdown="true" :table-data="results ? results : []"
          :table-header="headerConfig" :loading="loading" :total="total ? total : total" :rowsPerPage="rowsPerPage"
          :currentPage="currentPage" @current-change="current_change" @items-per-page-change="items_per_page_change">
          <template v-slot:cell-title="{ row: product }">
            <a :href="product?.product_url" target="_blank">{{ product.title }}</a>
          </template>

          <template v-slot:cell-image="{ row: product }">
            <a :href="product?.product_url"><img :src="product.image" alt="product_image" width="100"
                height="100" /></a>
          </template>
          <template v-slot:cell-ebay_item_id="{ row: product }">
            <a :href="product.product_url" target="_blank">{{ product.ebay_item_id }}</a>
          </template>
        </KTDatatable>
      </div>
    </div>
  </div>
</template>

<script>
import ExclamationCircleIcon from '@/components/icons/outlined/svg-icons/ExclamationCircleIcon.vue'
import KTDatatable from '@/components/kt-datatable/KTDatatable.vue'
import { onMounted, ref } from 'vue'
import SearchIcon from '@/components/icons/outlined/svg-icons/SearchIcon.vue'
import { callProducts, productFilters, product_categories } from '@/service'
import { toast } from 'vue3-toastify'
import { useRoute, useRouter } from 'vue-router'
import VueCtkDateTimePicker from 'vue-ctk-date-time-picker'
import { useStore } from 'vuex'

export default {
  components: { ExclamationCircleIcon, KTDatatable, SearchIcon, VueCtkDateTimePicker },

  setup() {
    const searchKeyword = ref('')
    const currentPage = ref(1)
    const rowsPerPage = ref(10)
    const route_Phrase = ref('')
    const results = ref('')
    const category = ref([])
    const total = ref(0)
    const records = ref(0)
    const loading = ref(false)
    const date = ref('')
    const toggle = ref(false)
    const productfilter = ref([])
    const analytics = ref('')
    const filterNames = ref([])
    const router = useRouter()
    const route = useRoute()
    const store = useStore()
    const custom_shortcuts = [
      { key: 'thisWeek', label: 'This week', value: 'isoWeek' },
      { key: 'lastWeek', label: 'Last week', value: '-isoWeek' },
      { key: 'last7Days', label: 'Last 7 days', value: 7 },
      { key: 'last30Days', label: 'Last 30 days', value: 30 },
      { key: 'last90Days', label: 'Last 90 days', value: 90 }
    ]
    const data = ref({
      title: searchKeyword?.value,
      name: 'ebay.com.au',
      shippingLocation: 'Australia',
      excludedPhrase: null,
      date_range: null,
      maxPrice: '',
      minPrice: '',
      conditions: null,
      dataCategory: 'Active',
      colors: null,
      brands: null,
      storages: null,
      lock_statuses: null,
      page_size: rowsPerPage?.value,
      categories: null,

    })

function manualSearch () {
searchdataApi() 
  
}
    function handlelogout() {
      store.dispatch('handleAccesstoken', null)
      store.dispatch('handlerole', null)
      store.dispatch('handleuserpermissions', null)
      router.push('/auth/login')
    }

    let timeout
    async function callproductsApi(page_number = 1) {
      loading.value = true
      clearTimeout(timeout)
      timeout = setTimeout(async () => {
        try {
          let dataCopy = { ...data.value } || false
          for (let x in dataCopy) {
            if (dataCopy[x] == null) {
              dataCopy[x] = ''
            }
          }
          await callProducts(page_number, dataCopy).then((data) => {
            if (data) {
              results.value = data.results
              total.value = data.total_pages
              records.value = data.total_records
              rowsPerPage.value = data.page_size
              analytics.value = data.analytics
            }
            loading.value = false
          })
        } catch (err) {
          console.log(err)
          loading.value = false
        }
      }, 1500)
    }
    let timeeout
    function searchdataApi() {
      loading.value = true
      clearTimeout(timeeout)
      timeeout = setTimeout(() => {
        if (!searchKeyword.value.startsWith(' ')) {
          let filter = searchKeyword.value.trim()
          if (data.value.title != filter) {
            data.value.title = filter
            callproductsApi()
          }
        } else {
          let filter = searchKeyword.value.trim()
          if (data.value.title != filter) {
            data.value.title = filter
            callproductsApi()
          }
        }
      }, 1500)
    }

    function changeDateformat() {
      if (date.value) {
        let start = date.value.start
        let end = date.value.end || ''
        let dateJoin
        if (start && end) {
          dateJoin = start.concat(' to ', end)
        }
        else {
          if (start) {
            date.value = { "start": start }
          }
        }
        data.value.date_range = dateJoin || start
        callproductsApi()
      }
      else {
        data.value.date_range = date.value
        callproductsApi()
      }
    }

    // function addComa () {

    //   if(data.value.excludePhrase && !data.value.excludePhrase.endsWith(',') && !data.value.excludePhrase.slice(-1).endsWith(' ') ){
    //     data.value.excludePhrase += ','
    //   }
    // }

    function checkPrice() {
      if (data.value.maxPrice || data.value.minPrice) {
        if (data.value.maxPrice < 0 || data.value.minPrice < 0) {
          toast.error('Min/Max price should be greater or equal to zero', { autoClose: 3000 })
        }
        else if (data.value.maxPrice < data.value.minPrice) {
          toast.error('Max price should be greater or equal Min price', { autoClose: 3000 })
        }
        else {
          callproductsApi()
        }
      }
    }

    onMounted(async () => {

      route_Phrase.value = route.query.value
      try {
        const response = await product_categories()

        if (response) {
          category.value = response
        }
      }
      catch (err) {
        console.log(err)
      }
      const today = new Date();
      function formatDate(date) {
        return new Intl.DateTimeFormat('en-CA').format(date);
      }
      const startDate = formatDate(new Date(today.setDate(today.getDate() - 30)));
      const endDate = formatDate(new Date());
      date.value = { 'start': startDate, 'end': endDate, 'shortcut': 30 }
      data.value.date_range = date.value.start.concat(' to ', date.value.end)


      loading.value = true
      try {
        const response = await productFilters()
        if (response.detail) {
          toast.error('Session has expired, Please login again', {
            autoClose: 6000
          })
          setTimeout(() => {
            handlelogout()
          }, 3000)
        } else {
          productfilter.value = response
          filterNames.value.push(...Object.keys(response))
        }
      } catch (err) {
        console.log(err)
      }
      try {
        let dataCopy = { ...data.value } || false
        for (let x in dataCopy) {
          if (dataCopy[x] == null) {
            dataCopy[x] = ''
          }
        }
        await callProducts(undefined, dataCopy).then((data) => {
          results.value = data.results
          total.value = data.total_pages
          records.value = data.total_records
          rowsPerPage.value = data.page_size
          analytics.value = data.analytics
          loading.value = false
        })
      } catch (err) {
        loading.value = false
      } finally {
        loading.value = false
      }


      searchKeyword.value = route_Phrase.value
      if(searchKeyword.value){
        searchdataApi()
      }
    })

    const headerConfig = ref([
      {
        name: 'Image',
        key: 'image',
        sortable: false
      },
      {
        name: 'Title',
        key: 'title',
        sortable: true
      },
      {
        name: 'Sold Price',
        key: 'sold_price',
        sortable: false
      },
      {
        name: 'Shipping Fee',
        key: 'shipping_fee',
        sortable: false
      },
      {
        name: 'Ebay Item Id',
        key: 'ebay_item_id',
        sortable: false
      },
      {
        name: 'Product Model',
        key: 'product_model',
        sortable: false
      },
      {
        name: 'Brand',
        key: 'brand',
        sortable: false
      },
      {
        name: 'Color',
        key: 'color',
        sortable: false
      },
      {
        name: 'Storage',
        key: 'storage',
        sortable: false
      },
      {
        name: 'Lock Status',
        key: 'lock_status',
        sortable: false
      },
      {
        name: 'Condition',
        key: 'condition',
        sortable: false
      },
      {
        name: 'Sold Date',
        key: 'sold_date',
        sortable: false
      },
      {
        name: 'Created At',
        key: 'created_at',
        sortable: false
      }
    ])

    const current_change = async (page_number) => {
      currentPage.value = page_number
      callproductsApi(page_number)
    }

    const items_per_page_change = (items_per_page) => {
      rowsPerPage.value = items_per_page
      data.value.page_size = items_per_page
      loading.value = true
      currentPage.value = 1
      callproductsApi(currentPage.value)
    }

    return {
      headerConfig,
      items_per_page_change,
      current_change,
      results,
      total,
      loading,
      rowsPerPage,
      currentPage,
      data,
      callproductsApi,
      records,
      checkPrice,
      searchdataApi,
      searchKeyword,
      custom_shortcuts,
      changeDateformat,
      date,
      productfilter,
      filterNames,
      analytics,
      category,
      route_Phrase,
      toggle,
      manualSearch

    }
  }
}
</script>

<style scoped>
.skeleton {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  backdrop-filter: blur(2px);
  border-radius: 14px;
}

.stats {
  background: #f1f1f2;
}

p {
  margin-bottom: 0px;
}

.vertical-line {
  width: 2px;
  height: 100%;
  background-color: black;
  margin: 0 20px;
  border-radius: 20px;
}

:deep(#my_date-input) {
  border: none !important;
  border-bottom: 2px solid black !important;
  border-radius: 0px;
  margin-top: 12px;
  font-size: 14px;
  width: 100%;
}

:deep(.field-label) {
  color: black !important;
}

:deep(#my_date-input)::placeholder {
  color: black !important;
  font-weight: 600 !important;
  font-size: 17px;
}

.main-head {
  min-height: 50px;
}

.exclude-phrase::placeholder {
  color: black;
  font-weight: 600;
}

* {
  color: black;
}

.searchbox {
  border: 2px solid black;
  width: 70%;
  max-height: 40px;
  border-radius: 10px;
  padding-inline: 10px;
}

:deep(.v-field__outline) {
  --v-field-border-width: 2px;
  --v-field-border-opacity: 1;
}

:deep(.v-label) {
  opacity: 1;
}

.selectinput {
  color: black;
  font-weight: 600;
}

.section {
  background-color: white;
  border: 1px solid #dddfe2;
  text-align: center;
  border-radius: 20px;
  padding: 12px;
  /* padding-bottom: 35px; */
  min-height: 130px;
  display: flex;
  flex-direction: column;
}

.platform {
  /* border-bottom: 3px solid #3a57e8; */
  width: 8rem;
  font-size: 20px;
  font-weight: 700;
  color: #3a57e8;
  padding-bottom: 0.3rem;
  text-align: center;
  margin: 0;
}

.searchbar {
  width: 70%;
  padding: 0.3rem;
  outline: none;
}

.searchbtn {
  border: 2px solid black;
  color: black;
  border-radius: 14px;
  margin-inline: 13px;
  width: 20%;
  font-weight: 600;
  padding: 0.3rem 0.2rem;
  background-color: transparent;
}

.pricerangeinput {
  border: none;
  outline: none;
  border-bottom: 0.1rem solid black;
  width: 100%;
  text-align: center;
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>
