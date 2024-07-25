<template>
    <div>
        <h4>Update Modules</h4>
        <b-col lg="12" class="py-3">
        <b-card no-body>

          <b-card-header class="d-flex justify-content-center">
            <div class="header-title d-flex align-items-center gap-2 ">
              <h4 class="card-title">Available Modules</h4><SquarePlusIcon style="cursor: pointer;"  type="button" data-bs-toggle="modal" data-bs-target="#staticBackdrop"/>
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
          <b-card-body v-else>
            <div v-for=" (item) in Modules" :key="item.id" class="d-flex gap-2 gap-y-3 justify-content-center align-items-center flex-wrap mb-2">
              <p class="fs-5 m-0 d-inline">{{item.name ? item.name : ''}}</p><span><SquareXIcon class="btn-inner" data-bs-toggle="modal" data-bs-target="#generic" style="cursor: pointer;" @click="Modulename = item.name , Moduleid = item.id"/></span></div>
          </b-card-body>

        </b-card>
      </b-col>
    </div>
    <DialogBox  :title="Modulename" :function="[removeModule]" :data="[Modulename,Moduleid]" />
    <BootstrapModalVue :function="[addModules,Success]"/>
</template>

<script>
import SquarePlusIcon from '@/components/icons/outlined/svg-icons/SquarePlusIcon.vue'
import SquareXIcon from '@/components/icons/outlined/svg-icons/SquareXIcon.vue';
import DialogBox from '@/components/bootstrap/DialogBox.vue';
import BootstrapModalVue from '@/components/bootstrap/BootstrapModal.vue'
import { addModules,getModules,deleteModule } from '@/service';
import { onMounted, ref } from 'vue';
import { toast } from 'vue3-toastify';
// import LoaderComponent from '@/components/custom/loader/LoaderComponent.vue';
export default {
  components:{SquareXIcon,SquarePlusIcon,BootstrapModalVue,DialogBox},
  setup (){
    const Modules = ref('')
    const Modulename = ref('')
    const Moduleid = ref('')
    const loading = ref(false)




    onMounted(async()=>{try{ 
      loading.value = true
      await getModules().then(data=> {Modules.value = data.results
        loading.value = false
        
    })}
    catch(err){
      toast.error('Network Error',{
        autoClose:2000
      })
      loading.value = false
    }
    loading.value = false
  }
  
  )

    function Success (){
      loading.value = true
      getModules().then(data=> {Modules.value = data.results
        loading.value = false
      })
      loading.value = false
    }
    async function removeModule (value) {
      await deleteModule(value).then(data => {if(data.message){
        Success()
        toast.success(data.message,{
          autoClose: 2000
        })
      }})
    }




    return {
      loading,
    Modules,
    Modulename,
    Moduleid,
    removeModule,
    addModules,
    Success
    }
  } 

}
</script>