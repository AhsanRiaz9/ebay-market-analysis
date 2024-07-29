<template>
   
  <b-row>
    <b-col sm="12">
      <div class="card">
        <div class="card-header d-flex justify-content-between">
          <div class="header-title">
            <h4 class="card-title">User List</h4>
          </div>
        </div>
        <div class="card-body px-0">
          <div v-if="loading" class="loader-container">
        <div class="mx-auto" style="width: fit-content" role="status">
          <img
            height="300"
            width="300"
            src="/img/Evitare loader.gif"
            alt=""
          />
        </div>
      </div>
          <KTDatatable
          v-else
        :table-data="users ? users : []"
        :loading="loading"
        :table-header="headerConfig"
        :total="total"
        :enable-items-per-page-dropdown="false"
        :rowsPerPage="rowsPerPage"
        :currentPage="currentPage"
        @current-change="current_change"
        @items-per-page-change="items_per_page_change"
      >
      <template v-slot:id="{ row: product }">
          {{ product.id }}
        </template>
      <template v-slot:email="{ row: product }">
          {{ product.email }}
        </template>
      <template v-slot:name="{ row: product }">
          {{ product.name }}
        </template>
      <template v-slot:role="{ row: product }">
          {{ product.role }}
        </template>
      <template v-slot:phone_number="{ row: product }">
          {{ product.phone_number }}
        </template>
      <template v-slot:cell-actions="{row:product}">
      <span class="px-2">
        <a class="btn btn-sm btn-icon btn-warning "  href="#" aria-label="Edit" data-bs-original-title="Edit">
                                    <span class="btn-inner">
                                       <svg class="icon-20" width="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                          <path d="M11.4925 2.78906H7.75349C4.67849 2.78906 2.75049 4.96606 2.75049 8.04806V16.3621C2.75049 19.4441 4.66949 21.6211 7.75349 21.6211H16.5775C19.6625 21.6211 21.5815 19.4441 21.5815 16.3621V12.3341" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                          <path fill-rule="evenodd" clip-rule="evenodd" d="M8.82812 10.921L16.3011 3.44799C17.2321 2.51799 18.7411 2.51799 19.6721 3.44799L20.8891 4.66499C21.8201 5.59599 21.8201 7.10599 20.8891 8.03599L13.3801 15.545C12.9731 15.952 12.4211 16.181 11.8451 16.181H8.09912L8.19312 12.401C8.20712 11.845 8.43412 11.315 8.82812 10.921Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                          <path d="M15.1655 4.60254L19.7315 9.16854" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                       </svg>
                                    </span>
                                 </a>
      </span>
                                 <span>
                                  <a  class="btn btn-sm btn-icon btn-danger" data-bs-toggle="tooltip" data-bs-placement="top" href="#" aria-label="Delete" data-bs-original-title="Delete">
                                    <span class="btn-inner" @click="deleteUser(product.id)">
                                       <svg class="icon-20" width="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="currentColor">
                                          <path d="M19.3248 9.46826C19.3248 9.46826 18.7818 16.2033 18.4668 19.0403C18.3168 20.3953 17.4798 21.1893 16.1088 21.2143C13.4998 21.2613 10.8878 21.2643 8.27979 21.2093C6.96079 21.1823 6.13779 20.3783 5.99079 19.0473C5.67379 16.1853 5.13379 9.46826 5.13379 9.46826" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                          <path d="M20.708 6.23975H3.75" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                          <path d="M17.4406 6.23973C16.6556 6.23973 15.9796 5.68473 15.8256 4.91573L15.5826 3.69973C15.4326 3.13873 14.9246 2.75073 14.3456 2.75073H10.1126C9.53358 2.75073 9.02558 3.13873 8.87558 3.69973L8.63258 4.91573C8.47858 5.68473 7.80258 6.23973 7.01758 6.23973" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                       </svg>
                                    </span>
                                 </a>
                                 </span>
      </template>
    </KTDatatable>
          <!-- <div class="table-responsive">
            <table id="user-list-table" class="table table-striped" role="grid" data-toggle="data-table">
              <thead>
                <tr class="ligth">
                  <th>Name</th>
                  <th>Contact</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th style="min-width: 100px">Action</th>
                </tr>
              </thead>
              <tbody>
                <TableWidget :list="userList" />
              </tbody>
            </table>
          </div> -->
        </div>
      </div>
    </b-col>
  </b-row>

</template>
<script>
import KTDatatable from '@/components/kt-datatable/KTDatatable.vue';
import { userLists } from '@/service';
import { ref } from 'vue';
import { removeUser } from '@/service';
import { toast } from 'vue3-toastify';
// import BootstrapModalVue/ from '@/components/bootstrap/BootstrapModal.vue';
export default {
  components: {
    // TableWidget
    KTDatatable,
    // BootstrapModalVue
  },
  setup() {
    const currentPage = ref(1);
    const rowsPerPage = ref(10);
    const users = ref('')
    const total = ref('')
    const loading = ref(false)
    async function userslist () {
      try{
        loading.value = true
        await userLists().then(data=>{
          users.value = data.results
          total.value = data.total_pages
        loading.value = false
        })
      }
      catch (error){
        loading.value = false
        console.log(error)
      }
    }
    userslist()
    const headerConfig = ref([
      {
        name: "ID",
        key: "id",
        sortable: true,
      },
      {
        name: "Email",
        key: "email",
        sortable: false,
      },
      {
        name: "Name",
        key: "name",
        sortable: false,
      },
      {
        name: "Role",
        key: "role",
        sortable: false,
      },
      {
        name: "Phone Number",
        key: "phone_number",
        sortable: false,
      },
      {
        name: "Actions",
        key: "actions",
        sortable: false,
      },
    ]);

      async function deleteUser(value){
      try{
        await removeUser(value).then(data => users.value = data)
      } 
      catch(err){
        toast.error('Failed To Delete User',{
          autoClose: 2000
        })
      }
     }
    async function Callusers (value){
    loading.value = true
   try{
    await fetch(`${process.env.VUE_APP_LOGIN_API_URL}users/?page=${value}`,{method:'GET'}).then(response => response.json()).then(data=>{
    users.value = data.results
    total.value = data.total_pages 
    loading.value = false
    })
   }
   
   catch(error){
    console.log(error)
   }

    }
    const current_change = (page_number) => {
      currentPage.value = page_number;
      Callusers(page_number)
      
    };

    const items_per_page_change = (items_per_page) => {
      rowsPerPage.value = items_per_page;
    };
   
    return {
      deleteUser,
      users,
      current_change,
      loading,
      items_per_page_change,
      rowsPerPage,
      currentPage,
      headerConfig,
      total
    }

  },

}
</script>
