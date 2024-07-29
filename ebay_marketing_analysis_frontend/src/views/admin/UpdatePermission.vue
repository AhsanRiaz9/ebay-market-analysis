<template>
    <div class="row">
      <h4 class="mb-4">Update Permissions</h4>
    <div v-if="loading" style="background-color: white">
        <img
          class="mx-auto d-block"
            height="300"
            width="300"
            src="/img/Evitare loader.gif"
            alt=""
          />
    </div>
      <b-col v-else lg='3' v-for="(items,index) in results" :key="index">
        <b-card>
          <div class="d-flex align-items-center">
            <div class="d-flex flex-column  justify-content-center w-100">
              <div class="fs-italic">
                <div class="d-flex justify-content-between align-items-center"><h5>{{ items.name }}</h5> <SquarePlusIcon  style="cursor: pointer;"  type="button" data-bs-target="#staticBackdrop" data-bs-toggle="modal" @click="checkModule(items)"/></div>
                <div class="text-muted-50 py-3">
                  <!-- {{items.id}} -->
                  <ul v-for="(item,index) in permissions" :key="index" class="list-group ">
          <li v-if="items.id == item.module" class="list-group-item d-flex justify-content-between align-items-center my-1">
              {{ item.name }}
          <span @click=" permissionsName = item.name , permissionsId = item.id " class="btn-inner" data-bs-toggle="modal" data-bs-target="#generic" style="cursor: pointer">
          <icon-component  type="outlined" icon-name="trash"/> 
          </span>
  </li> 
</ul>
</div>  

</div>
</div>
</div>
</b-card>
</b-col>
</div>
<BootstrapModal  :content= "moduleName" :addpermission="Addpermission" /> 
<DialogBox :title="permissionsName" :data="[permissionsName,permissionsId]"  :function="[Deletepermission,Success]"/>
</template>

<script>
import { getModules,getPermissions,deletePermissions,addPermissions, loginUser } from '@/service';
import SquarePlusIcon from '@/components/icons/outlined/svg-icons/SquarePlusIcon.vue';
import BootstrapModal from '@/components/bootstrap/BootstrapModal.vue';
import { onMounted } from 'vue';
import DialogBox from '@/components/bootstrap/DialogBox.vue';
import { ref } from 'vue';
import { toast } from 'vue3-toastify';
import { useStore } from 'vuex';
export default {
  components:{
SquarePlusIcon,
BootstrapModal,
DialogBox
  },
    setup(){
      const store = useStore()
      const moduleName = ref(null)
      const permissionsName = ref(null)
      const permissionsId = ref(null)
      const results = ref([])
      const proceed = ref(false)
      const moduleNumber = ref('')
      const permissions = ref([])
      const modalstatic = ref(false)
      const loading = ref(false)

      onMounted(async()=>{try{
        loading.value = true
        await getPermissions().then(data => {permissions.value = data
        })}catch(err){console.log(err)}
         try{
          await getModules().then(data=> {results.value = data.results 
          })
         }catch(err){
          console.log(err)
         }
         loading.value = false 
        }
      )
      
      function checkModule(value){
        moduleName.value = `Add ${value.name} Permission`
        moduleNumber.value = value.id
      }
    async function Success (){
      const response = await loginUser(store?.getters?.accesstoken)
    if(response.access){
     await store.dispatch('handleAccesstoken',response.access)}
     await getPermissions().then(data=> permissions.value = data)
    }
   
    
     async function Deletepermission(id) {
     try{
      await deletePermissions(id).then(data =>{ 
        if(data.message){
          toast.success(data.message,{autoClose:2000})
         getPermissions().then(data => {permissions.value = data})
        } 
        else{
          toast.info(data.message,{autoClose:2000}) 
        }
     })
     }catch (err){
      toast.error('Failed to delete',{autoClose:2000})
     }
      }


      async function Addpermission (value) {
         let data = {}
         data.module = moduleNumber.value
         const valueLowercase = value.name.toLowerCase().trim().replace(' ','_')
          data.name = value.name.trim()
          data.code = valueLowercase+'_'
          if(data){
              await addPermissions(data).then(data =>{ if(data){Success()
                if(data.message){
                  toast.success(data.message,{
          autoClose: 2000
        })
                }
              }})
          }
        }
        return {
          loading,
          results,
          proceed,
          Success,
          Deletepermission,
          Addpermission,
          modalstatic,
          checkModule,
          moduleName,
          permissions,
          permissionsName,
          permissionsId,

        }
    },

}
</script>