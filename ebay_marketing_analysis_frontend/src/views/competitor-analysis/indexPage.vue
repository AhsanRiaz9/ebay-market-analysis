<template>
  <div class="d-flex justify-content-between align-content-center first-header">
    <div>
      <p class="m-0 fw-bold fs-4 text-primary text-decoration-underline " style="line-height: 60px;">eBay</p>
    </div>
    <div class="d-flex gap-4 w-75 align-items-center">
      <div class="searchbox">
        <SearchIcon /> <input type="text" placeholder="Search" class="searchbar" />
      </div><v-select class="w-25" label="Select" :items="['California']"></v-select><button
        class="btn btn-primary">Search</button>
    </div>
    <div></div>
  </div>
  <div style="gap: 30px 0;" class="row py-4 ">
    <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
      <div class="section">
        <div class="d-flex justify-content-between">
          <div></div>
          <h6 class="fw-semibold">Sell through</h6>
          <exclamation-circle-icon />
        </div>
        <h1 class="p-3 fw-bolder">553.66%</h1>
      </div>
    </div>
    <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
      <div class="section">
        <div class="d-flex justify-content-between">
          <div></div>
          <h6 class="fw-semibold">Active Listing</h6>
          <exclamation-circle-icon />
        </div>
        <h1 class=" fw-bolder">164</h1>
      </div>
    </div>
    <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
      <div class="section">
        <div class="d-flex justify-content-between">
          <div></div>
          <h6 class="fw-semibold">Sold Items</h6>
          <exclamation-circle-icon />
        </div>
        <h1 class=" fw-bolder">908</h1>
      </div>
    </div>
    <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
      <div class="section">
        <div class="d-flex justify-content-between">
          <div></div>
          <h6 class="fw-semibold">Sale Earnings</h6>
          <exclamation-circle-icon />
        </div>
        <h1 class=" fw-bolder">$ 240,481</h1>
      </div>
    </div>
  </div>
  <div class="row">
    <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
      <div class="section">
        <div class="d-flex justify-content-between">
          <div></div>
          <h6 class="fw-semibold">Feedback score</h6>
          <exclamation-circle-icon />
        </div>
        <h1 class="p-3 fw-bolder">21,355</h1>
      </div>
    </div>
    <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
      <div class="section">
        <div class="d-flex justify-content-between">
          <div></div>
          <h6 class="fw-semibold">Successful listing</h6>
          <exclamation-circle-icon />
        </div>
        <h1 class="p-3 fw-bolder">106</h1>
      </div>
    </div>
    <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
      <div class="section">
        <div class="d-flex justify-content-between">
          <div></div>
          <h6 class="fw-semibold">Average Price</h6>
          <exclamation-circle-icon />
        </div>
        <h1 class="p-3 fw-bolder">$264.85</h1>
      </div>
    </div>
    <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
      <div class="d-flex align-items-center flex-column gap-2">
        <button class="btn btn-primary">Watching</button>
        <button class="btn btn-primary">View Scannned Items</button>
      </div>
    </div>
  </div>
  <div style="background-color: white;" class="row py-4 mt-4">
    <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
      <div class="section border-0">
        <div class="d-flex justify-content-between">
          <div></div>
          <h6 class="fw-semibold">30 Day Sales</h6>
          <exclamation-circle-icon />
        </div>
        <div class="mt-auto gap-2 d-flex justify-content-around align-items-center px-4 pb-3">
          <div class="w-50">
            <input type="number" class="pricerangeinput" />
            <b class="text-center mx-auto d-block text-black">Min</b>
          </div>
          <div class="w-50">
            <input type="number" class="pricerangeinput" />
            <b class="text-center mx-auto d-block text-black">Max</b>
          </div>
        </div>
      </div>
    </div>
    <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
      <div class="section border-0">
        <div class="d-flex justify-content-between">
          <div></div>
          <h6 class="fw-semibold">Total Sales</h6>
          <exclamation-circle-icon />
        </div>
        <div class="mt-auto gap-2 d-flex justify-content-around align-items-center px-4 pb-3">
          <div class="w-50">
            <input type="number" class="pricerangeinput" />
            <b class="text-center mx-auto d-block text-black">Min</b>
          </div>
          <div class="w-50">
            <input type="number" class="pricerangeinput" />
            <b class="text-center mx-auto d-block text-black">Max</b>
          </div>
        </div>
      </div>
    </div>
    <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
      <div class="section border-0">
        <div class="d-flex justify-content-between">
          <div></div>
          <h6 class="fw-semibold">Current Price</h6>
          <exclamation-circle-icon />
        </div>
        <div class="mt-auto gap-2 d-flex justify-content-around align-items-center px-4 pb-3">
          <div class="w-50">
            <input type="number" class="pricerangeinput" />
            <b class="text-center mx-auto d-block text-black">Min</b>
          </div>
          <div class="w-50">
            <input type="number" class="pricerangeinput" />
            <b class="text-center mx-auto d-block text-black">Max</b>
          </div>
        </div>
      </div>
    </div>
    <div class="col-lg-4 col-md-6 col-sm-12 col-xl-3">
      <div class="d-flex justify-content-center align-items-center h-100">
        <button class="filter-btn button">Filter</button>
      </div>
    </div>
  </div>
  <div style="background-color: white; margin-top: 1rem; padding-block: 1rem">
    <KTDatatable :enable-items-per-page-dropdown="true" :table-data="[]"
      :table-header="headerConfig" :loading="loading" :total="1" :rowsPerPage="rowsPerPage"
      :currentPage="currentPage" @current-change="current_change" @items-per-page-change="items_per_page_change">


    </KTDatatable>

  </div>
</template>

<script>
import SearchIcon from '@/components/icons/outlined/svg-icons/SearchIcon.vue'
import KTDatatable from '@/components/kt-datatable/KTDatatable.vue';
import { ref } from 'vue';
export default {
  components: { SearchIcon, KTDatatable },
  setup () {
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
      }])

      return {
        headerConfig
      }
}

}
</script>

<style scoped>
.input-section {
  border-bottom: 1px solid black;
}

.first-header {
  background-color: white;
  padding: 15px;
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
  justify-content: space-evenly;
}

:deep(.v-input__details) {
  display: none !important;
}

.searchbox {
  border: 3px solid black;
  width: 70%;
  /* max-height: 40px; */
  border-radius: 20px;
  padding: 5px;
}

.searchbar {
  width: 90%;
  padding: 0.3rem;
  outline: none;
}

:deep(.v-input > *) {
  color: black !important;
}

:deep(.v-input) {
  background-color: transparent !important;
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

.filter-btn {
  border: 2px solid #3a57e8;
  border-radius: 18px;
  padding: 14px;
  width: 50%;
}

button {
  transition: .5s;
  color: #3a57e8;
  font-weight: 600;
}

.button:hover {
  background-color: #3a57e8;
  color: white;
}
</style>