<template>
    <div>
        <h4>Update Roles</h4>
        <b-col lg="12" class="py-3">
        <b-card no-body>

          <b-card-header class="d-flex justify-content-center">
            <div class="header-title d-flex align-items-center gap-2 ">
              <h4 class="card-title">Available Roles</h4><SquarePlusIcon style="cursor: pointer;"  type="button" data-bs-toggle="modal" data-bs-target="#staticBackdrop"/>
            </div>
          </b-card-header>
          <img
          v-if="loading"
          class="mx-auto"
            height="300"
            width="300"
            src="/img/Evitare loader.gif"
            alt=""
          />
          <b-card-body>
            <div v-for=" (item,index) in all_roles" :key="index" class="d-flex gap-2 justify-content-center align-items-center flex-wrap mb-2">
              <p class="fs-5 m-0">{{ item.name }}</p><SquareXIcon class="btn-inner" data-bs-toggle="modal" data-bs-target="#generic" style="cursor: pointer;" @click="Roleid = item.id , Rolename = item.name"/></div>
          </b-card-body>

        </b-card>
      </b-col>
    </div>
    <DialogBox  :title="Rolename" :data="[Rolename,Roleid]" :function="[removeRole]" />
    <BootstrapModalVue content="Update Roles" :function="[addRoles,Success]" />
</template>

<script>
  import {allRoles, deleteRoles, addRoles} from '@/service';
import SquarePlusIcon from '@/components/icons/outlined/svg-icons/SquarePlusIcon.vue'
import { onMounted, ref } from 'vue';
import DialogBox from '@/components/bootstrap/DialogBox.vue';
import BootstrapModalVue from '@/components/bootstrap/BootstrapModal.vue';
import SquareXIcon from '@/components/icons/outlined/svg-icons/SquareXIcon.vue';
import { toast } from 'vue3-toastify';
export default {
  components:{SquarePlusIcon,BootstrapModalVue,SquareXIcon,DialogBox},
  setup (){
    const all_roles = ref([])
    const Rolename = ref('')
    const Roleid = ref('')
    const loading = ref(false)
    onMounted(async()=>{try{
      loading.value = true
      await allRoles().then(data=> {all_roles.value = data
        loading.value = false
      } )}catch(err){console.log(err)
        loading.value = false
      }
    loading.value = false
    })
    function Success (){
      loading.value = true
      allRoles().then(data=> {all_roles.value = data
        loading.value = false
      })
      loading.value = false
    }
    async function removeRole (value) {
      try{
        await deleteRoles(value).then(data => {if(data.message)
        {toast.success(data.message,{
          autoClose: 2000
        })
         Success() }
        if(data.error){
          toast.error(data.message,{
          autoClose: 2000
        })
        }
        })
      }
      catch (err){
        toast.error('Error while deleting',{
            autoClose : 2000
        })
      }
    }
    return {
      loading,
      all_roles,
      Rolename,
      Roleid,
      Success,
      removeRole,
      addRoles

    }
  } 

}
</script>