<template>
    <div>
    <div class="w-100 p-2 rounded-2 d-flex align-items-center px-4" style="background-color: white"><div class="w-25"><p class="platform">eBay</p></div>
    <div class="w-50 d-flex"><div class="searchbox"><search-icon/> <input type="text" placeholder="Search" class="searchbar"></div> 
    <button class="searchbtn">Search</button></div>
  </div>
    <div class="row" style="gap:30px 0; background-color: white; margin-block: 25px; padding: 20px;">
      <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
        <div class="section">
    <div class="d-flex justify-content-between"><div></div> <h6 class=" fw-semibold">Marketplace</h6><exclamation-circle-icon/></div>
      <v-select
      class="selectinput"
      clearable
  label="Select Marketplace"
  :items="['ebay.com.au']"
  variant="underlined"
></v-select>
      </div>
      </div>
      <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
        <div class="section">
    <div class="d-flex justify-content-between"><div></div> <h6 class="fw-semibold">Shipping location</h6><exclamation-circle-icon/></div>
      <v-select
      class="selectinput"
      clearable
  label="Select Shipping location"
  :items="['Australia']"
  variant="underlined"
></v-select>
      </div>
      </div>
      <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
        <div class="section">
    <div class="d-flex justify-content-between"><div></div> <h6 class="fw-semibold">Sale date range</h6><exclamation-circle-icon/></div>
      <!-- <v-select
      class="selectinput"
      clearable
  label="Select date range"
  :items="['Nothing to show here']"
  variant="underlined"
></v-select> -->
<input type="text" name="date" class="form-control range_flatpicker" placeholder="Range Date Picker">
<div class="bd-example">
    <FlatPicker model="inlinedate" :config="{ mode: 'range', minDate: 'today', dateFormat: 'Y-m-d', inline: true }" name="date" placeholder="date range picker" class="form-control d-none"></FlatPicker>
  </div>
      </div>
      </div>
      <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
        <div class="section">
    <div class="d-flex justify-content-between"><div></div> <h6 class="fw-semibold">Price</h6><exclamation-circle-icon/></div>
    <div
                class="mt-auto d-flex justify-content-around align-items-center px-4 pb-3"
              >
                <div class="w-25">
                  <input
                    
                    type="number"
                    class="pricerangeinput"
                   
                  />
                  <b class="text-center mx-auto d-block">MIN</b>
                </div>
                <div class="w-25">
                  <input
                    
                    type="number"
                    class="pricerangeinput"
                    
                  />
                  <b class="text-center mx-auto d-block">MAX</b>
                </div>
              </div>
      </div>
      </div>
      <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
        <div class="section">
    <div class="d-flex justify-content-between"><div></div> <h6 class="fw-semibold">Exclude phrase</h6><exclamation-circle-icon/></div>
      <v-select
      class="selectinput"
      clearable
  label="Exclude Phrase"
  :items="['Nothing to show here']"
  variant="underlined"
></v-select>
      </div>
      </div>
      <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
        <div class="section">
    <div class="d-flex justify-content-between"><div></div> <h6 class="fw-semibold">Condition</h6><exclamation-circle-icon/></div>
      <v-select
      class="selectinput"
      clearable
  label="Condition"
  :items="['Nothing to show here']"
  variant="underlined"
></v-select>
      </div>
      </div></div>
   <div class="py-3" style="background-color: white;">
  <KTDatatable
    :enable-items-per-page-dropdown="false"
    :table-data="results ? results : []"
    :table-header="headerConfig"
    :loading="loading"
    :total="total"
    :rowsPerPage="rowsPerPage"
    :currentPage="currentPage"
    @current-change="current_change"
    @items-per-page-change="items_per_page_change" 
    >

    <template v-slot:cell-title="{row:product}">
      <a :href="product.product_url" target="_blank">{{ product.title }}</a>
    </template>

    <template v-slot:cell-image="{ row: product }">
    <img :src="product.image" alt="product_image" width="100" height="100">
    </template>

  </KTDatatable>
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
import KTDatatable from '@/components/kt-datatable/KTDatatable.vue';
import { onMounted, ref } from 'vue';
import SearchIcon from '@/components/icons/outlined/svg-icons/SearchIcon.vue';
import { callProducts } from '@/service';
import FlatPicker from 'vue-flatpickr-component'
  export default {

  components: {ExclamationCircleIcon,KTDatatable,SearchIcon,FlatPicker},

  setup(){
    const currentPage = ref(1);
    const rowsPerPage = ref(10);
    const results = ref('')
    const total = ref(0)
    const loading = ref(false)
    // const data = ref({

    // })



    onMounted( async() => {
      loading.value = true
      try{
        await callProducts().then(data=> {
          results.value = data.results
          total.value = data.total_pages

          console.log(total.value) 
          loading.value = false
        })
      }
      catch (err){
        loading.value = false
      }
      finally{
        loading.value = false
      }
    })



    const headerConfig = ref([
      {
        name: "Image",
        key: "image",
        sortable: false,
      },
      {
        name: "Title",
        key: "title",
        sortable: true,
      },
      {
        name: "Sold Price",
        key: "sold_price",
        sortable: false,
      },
      {
        name: "Shipping Fee",
        key: "shipping_fee",
        sortable: false,
      },
      {
        name: "Ebay Item Id",
        key: "ebay_item_id",
        sortable: false,
      },
      {
        name: "Category",
        key: "category",
        sortable: false,
      },
      {
        name: "Product Model",
        key: "product_model",
        sortable: false,
      },
      {
        name: "Brand",
        key: "brand",
        sortable: false,
      },
      {
        name: "Color",
        key: "color",
        sortable: false,
      },
      {
        name: "Storage",
        key: "storage",
        sortable: false,
      },
      {
        name: "Lock Status",
        key: "lock_status",
        sortable: false,
      },
      {
        name: "Condition",
        key: "condition",
        sortable: false,
      },
      {
        name: "Location",
        key: "location",
        sortable: false,
      },
      {
        name: "Sold Date",
        key: "sold_date",
        sortable: false,
      },
      {
        name: "Created At",
        key: "created_at",
        sortable: false,
      },
    ]);
    
    
    const current_change = async (page_number) => {
      currentPage.value = page_number;
     await callProducts(page_number).then(data => {
      results.value = data.results
      total.value = data.total_pages 
      loading.value = false
      })
    };

    const items_per_page_change = (items_per_page) => {
      rowsPerPage.value = items_per_page;
    };

      return{
        headerConfig,
        items_per_page_change,
        current_change,
        results,
        total,
        loading,
        rowsPerPage,
        currentPage
      }

  }

  }
</script>
    <style scoped>
    *{
      color:black
    }
    .searchbox{
      border: 2px solid black;
      width: 70%;
      border-radius: 10px;
      padding-inline: 10px;
    }
    :deep(.v-field__outline) {
      --v-field-border-width: 2px ;
      --v-field-border-opacity: 1;
    }
    :deep(.v-label){
      opacity: 1;
    }
    .selectinput{
      color: black;
      font-weight: 600;
    }
    .section{
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
    .platform{
      /* border-bottom: 3px solid #3a57e8; */
      width: 8rem;
      font-size: 20px;
      font-weight: 700;
      color: #3a57e8;
      padding-bottom: .3rem;
      text-align: center;
      margin: 0;
    }
    .searchbar{
      width: 70%;
      padding: .3rem;
      outline: none;
    }
    .searchbtn{
      border: 2px solid black;
      color: black;
      border-radius: 14px;
      margin-inline: 13px;
      width: 20%;
      font-weight: 600;
      padding: .3rem .2rem;
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