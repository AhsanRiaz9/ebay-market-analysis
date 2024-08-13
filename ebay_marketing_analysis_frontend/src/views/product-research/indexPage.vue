<template>
  <div>
    <div class="w-100 p-2 rounded-2 d-flex align-items-center px-4 main-head" style="background-color: white">
      <div class="w-25"><p class="platform">eBay</p></div>
      <div class="w-50 d-flex align-items-center">
        <div class="searchbox"><search-icon /> <input @input="searchdataApi" v-model="searchKeyword" type="text" placeholder="Search" class="searchbar" /></div>
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
          <v-select v-model="data.name" clearable class="selectinput" label="Select Marketplace" :items="['ebay.com.au']" @update:modelValue="callproductsApi" variant="underlined"></v-select>
        </div>
      </div>
      <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
        <div class="section">
          <div class="d-flex justify-content-between">
            <div></div>
            <h6 class="fw-semibold">Shipping location</h6>
            <exclamation-circle-icon />
          </div>
          <v-select clearable class="selectinput" v-model="data.shippingLocation" label="Select Shipping location" :items="['Australia']" variant="underlined" @update:modelValue="callproductsApi"></v-select>
        </div>
      </div>
      <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
        <div class="section">
          <div class="d-flex justify-content-between">
            <div></div>
            <h6 class="fw-semibold">Data Category</h6>
            <exclamation-circle-icon />
          </div>
          <v-select class="selectinput" v-model="data.dataCategory" label="Select Shipping location" :items="['Active', 'Sold']" variant="underlined" @update:modelValue="callproductsApi"></v-select>
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
              <input @change="checkPrice" v-model="data.minPrice" type="number" class="pricerangeinput" />
              <b class="text-center mx-auto d-block">MIN</b>
            </div>
            <div class="w-50">
              <input @change="checkPrice" v-model="data.maxPrice" type="number" class="pricerangeinput" />
              <b class="text-center mx-auto d-block">MAX</b>
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

          <VueCtkDateTimePicker id="my_date" range :format="'YYYY-MM-DD'" formatted="YYYY-MM-DD" :onlyDate="true" color="#3a57e8" noTime="true" :custom-shortcuts="custom_shortcuts" v-model="date" @update:modelValue="changeDateformat" />
        </div>
      </div>
      <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
        <div class="section">
          <div input class="d-flex justify-content-between">
            <div></div>
            <h6 class="fw-semibold">Exclude phrase</h6>
            <exclamation-circle-icon />
          </div>
          <input class="pt-5 mt-2 exclude-phrase" v-model="data.excludedPhrase" @input="callproductsApi" style="border-bottom: 2px solid black" placeholder="comma Separated Phrase" type="text" />
        </div>
      </div>
      <div v-for="(item, index) in productfilter" :key="index" class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
        <div class="section" v-if="productfilter">
          <div class="d-flex justify-content-between">
            <div></div>
            <h6 class="fw-semibold">{{ index }}</h6>
            <exclamation-circle-icon />
          </div>
          <v-autocomplete multiple v-model="data[index]" @update:modelValue="callproductsApi" class="selectinput" clearable :label="index" :items="item && item?.map((items) => ({ name: items?.name || items?.value, id: items?.ebay_condition_id || items?.id }))" item-title="name" item-value="id" variant="underlined"></v-autocomplete>
        </div>
      </div>
      <div v-if="data.dataCategory == 'Active'" class="w-100 position-relative rounded-3 stats p-4 d-flex justify-content-evenly">
        <div v-if="loading" class="skeleton d-flex"></div>
        <div class="d-flex gap-3">
          <div>
            <h5>AU$ {{analytics?.avg_price?.toFixed(2)}}</h5>
            <p>Avg. listing price</p>
          </div>
          <div>
            <h5>AU ${{ analytics?.min_price }} - AU ${{analytics?.max_price}}</h5>
            <p>listing price range</p>
          </div>
        </div>
        <div class="vertical-line"></div>
        <div class="d-flex gap-3">
          <div>
            <h5>AU$ {{analytics?.avg_postage?.toFixed(2)}}</h5>
            <p>Avg. postage</p>
          </div>
          <div>
            <h5>{{analytics?.free_postage?.toFixed(0)}}%</h5>
            <p>Free postage</p>
          </div>
        </div>
        <div class="vertical-line"></div>
        <div class="d-flex gap-3">
          <div>
            <h5>{{ records }}</h5>
            <p>Total active listing</p>
          </div>
        </div>
      </div>
      <div v-if="data.dataCategory == 'Sold'" class="w-100 position-relative rounded-3 stats p-4 d-flex justify-content-evenly">
      <div v-if="loading" class="skeleton d-flex"></div>
        <div class="d-flex gap-3">
          <div>
            <h5>AU$ {{ analytics?.avg_price?.toFixed(2) }}</h5>
            <p>Avg. listing price</p>
          </div>
          <div>
            <h5>AU$ {{ analytics?.min_price }} - AU$ {{ analytics?.max_price }}</h5>
            <p>listing price range</p>
          </div>
        </div>
        <div class="vertical-line"></div>
        <div class="d-flex gap-3">
          <div>
            <h5>AU$ {{ analytics?.avg_postage?.toFixed(0) }}</h5>
            <p>Avg. postage</p>
          </div>
          <div>
            <h5>{{analytics?.free_postage}} %</h5>
            <p>Free postage</p>
          </div>
        </div>
        <div class="vertical-line"></div>
        <div class="d-flex gap-3">
          <div>
            <h5>{{records}}</h5>
            <p>Total active listing</p>
          </div>
          <div>
            <h5>{{analytics?.sell_through?.toFixed(2)}} %</h5>
            <p>Sell through rate</p>
          </div>
        </div>

      </div>

      <div class="py-3" style="background-color: white">
        <KTDatatable :enable-items-per-page-dropdown="true" :table-data="results ? results : []" :table-header="headerConfig" :loading="loading" :total="total ?total : total " :rowsPerPage="rowsPerPage" :currentPage="currentPage" @current-change="current_change" @items-per-page-change="items_per_page_change">
          <template v-slot:cell-title="{ row: product }">
            <a :href="product.product_url" target="_blank">{{ product.title }}</a>
          </template>

          <template v-slot:cell-image="{ row: product }">
            <img :src="product.image" alt="product_image" width="100" height="100" />
          </template>
          <template v-slot:cell-ebay_item_id="{ row: product }">
            <a :href="product.product_url" target="_blank">{{ product.ebay_item_id }}</a>
          </template>
        </KTDatatable>
      </div>
    </div>
  </div>
</template>

<!-- <script>
  import { onMounted, ref } from 'vue'
  import { Navigation } from 'swiper'
  import { useStore } from 'vuex'
  // import { Swiper, SwiperSlide } from 'swiper/vue'
  // import AnalyticsWidget from '@/components/widgets/AnalyticsWidget.vue'
  import AOS from 'aos'
  export default {
    components: {
      // SwiperSlide,
      // AnalyticsWidget
    },
    setup() {
      const store = useStore()
      const modules = [Navigation]
      const grossSaleChart = ref({
        series: [
          {
            name: 'total',
            data: [94, 80, 94, 80, 94, 80, 94]
          },
          {
            name: 'pipline',
            data: [72, 60, 84, 60, 74, 60, 78]
          }
        ],
        options: {
          chart: {
            fontFamily: '"Inter", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"',
            height: 245,
            type: 'area',
            toolbar: {
              show: false
            },
            sparkline: {
              enabled: false
            }
          },
          colors: ['#3a57e8', '#079aa2'],
          dataLabels: {
            enabled: false
          },
          stroke: {
            curve: 'smooth',
            width: 3
          },
          yaxis: {
            show: true,
            labels: {
              show: true,
              minWidth: 19,
              maxWidth: 19,
              style: {
                colors: '#8A92A6'
              },
              offsetX: -5
            }
          },
          legend: {
            show: false
          },
          xaxis: {
            labels: {
              minHeight: 22,
              maxHeight: 22,
              show: true,
              style: {
                colors: '#8A92A6'
              }
            },
            lines: {
              show: false // or just here to disable only x axis grids
            },
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug']
          },
          grid: {
            show: false
          },
          fill: {
            type: 'gradient',
            gradient: {
              shade: 'dark',
              type: 'vertical',
              shadeIntensity: 0,
              gradientToColors: undefined, // optional, if not defined - uses the shades of same color in series
              inverseColors: true,
              opacityFrom: 0.4,
              opacityTo: 0.1,
              stops: [0, 50, 80],
              colors: ['#3a57e8', '#4bc7d2']
            }
          },
          tooltip: {
            enabled: true
          }
        }
      })
      const earningChart = ref({
        series: [55, 75],
        options: {
          chart: {
            height: 260,
            type: 'radialBar'
          },
          colors: ['#4bc7d2', '#3a57e8'],
          plotOptions: {
            radialBar: {
              hollow: {
                margin: 10,
                size: '50%'
              },
              track: {
                margin: 10,
                strokeWidth: '50%'
              },
              dataLabels: {
                show: false
              }
            }
          }
        }
      })
      const conversionChart = ref({
        series: [
          {
            name: 'Successful deals',
            data: [30, 50, 35, 60, 40, 60, 60, 30, 50, 35]
          },
          {
            name: 'Failed deals',
            data: [40, 50, 55, 50, 30, 80, 30, 40, 50, 55]
          }
        ],
        options: {
          chart: {
            type: 'bar',
            height: 230,
            stacked: true,
            toolbar: {
              show: false
            }
          },
          colors: ['#3a57e8', '#4bc7d2'],
          plotOptions: {
            bar: {
              horizontal: false,
              columnWidth: '28%',
              endingShape: 'rounded',
              borderRadius: 5
            }
          },
          legend: {
            show: false
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
          },
          xaxis: {
            categories: ['S', 'M', 'T', 'W', 'T', 'F', 'S', 'M', 'T', 'W'],
            labels: {
              minHeight: 20,
              maxHeight: 20,
              style: {
                colors: '#8A92A6'
              }
            }
          },
          yaxis: {
            title: {
              text: ''
            },
            labels: {
              minWidth: 19,
              maxWidth: 19,
              style: {
                colors: '#8A92A6'
              }
            }
          },
          fill: {
            opacity: 1
          },
          tooltip: {
            y: {
              formatter: function (val) {
                return '$ ' + val + ' thousands'
              }
            }
          }
        }
      })
      const swiperItems = ref([
        {
          size: 90,
          amount: '560K',
          subTitle: 'Total Sales',
          color: 'primary'
        },
        {
          size: 80,
          amount: '185K',
          subTitle: 'Total Profit',
          color: 'info'
        },
        {
          size: 70,
          amount: '375K',
          subTitle: 'Total Cost',
          color: 'primary'
        },
        {
          size: 60,
          amount: '742K',
          subTitle: 'Revenue',
          color: 'info'
        },
        {
          size: 50,
          amount: '150K',
          subTitle: 'Net Income',
          color: 'primary'
        },
        {
          size: 40,
          amount: '4600',
          subTitle: 'Today',
          color: 'info'
        },
        {
          size: 30,
          amount: '11.2M',
          subTitle: 'Members',
          color: 'primary'
        }
      ])
      onMounted(() => {
        AOS.init({
          disable: function () {
            var maxWidth = 996
            return window.innerWidth < maxWidth
          },
          once: true,
          duration: 800
        })
      })
      return { modules,store, grossSaleChart, earningChart, conversionChart, swiperItems }
    }
  }
  </script> -->

<script>
import ExclamationCircleIcon from '@/components/icons/outlined/svg-icons/ExclamationCircleIcon.vue'
import KTDatatable from '@/components/kt-datatable/KTDatatable.vue'
import { onMounted, ref } from 'vue'
import SearchIcon from '@/components/icons/outlined/svg-icons/SearchIcon.vue'
import { callProducts, productFilters} from '@/service'
import { toast } from 'vue3-toastify'
import VueCtkDateTimePicker from 'vue-ctk-date-time-picker'

export default {
  components: { ExclamationCircleIcon, KTDatatable, SearchIcon, VueCtkDateTimePicker },
  setup() {
    const searchKeyword = ref('')
    const currentPage = ref(1)
    const rowsPerPage = ref(10)
    const results = ref('')
    const total = ref(0)
    const records = ref(0)
    const loading = ref(false)
    const date = ref('')
    const productfilter = ref([])
    const analytics = ref('')
    const filterNames = ref([])
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
      dateRange: null,
      maxPrice: '',
      minPrice: '',
      conditions: null,
      dataCategory: 'Active',
      colors: null,
      brands: null,
      storages: null,
      lock_statuses: null,
      page_size : rowsPerPage?.value
    })

    let timeout
    async function callproductsApi(page_number=1) {
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
          dateJoin = start.concat('-', end)
        }
        data.value.dateRange = dateJoin || start
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
        } else {
          callproductsApi()
        }
      }
    }

    onMounted(async () => {
      loading.value = true
      try {
        const response = await productFilters()
        if(response.detail){
          toast.error('Session has expired, Please login again',{
            autoClose:6000
          })
        }
        else {
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
        await callProducts(undefined,dataCopy).then((data) => {
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
        name: 'Ranking',
        key:'ranking',
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
      analytics
    }
  }
}
</script>

<style scoped>
.skeleton{
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
p{
  margin-bottom:0px;
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
