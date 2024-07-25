<template>
    <div>
<!-- Modal -->
<div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="staticBackdropLabel">{{ content ? content : "Untitled" }}</h5>
        <button type="button" ref="closebutton" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
      <input placeholder="Please enter valid content here." v-model="data.name" type="text" class="border-0 border-bottom w-100">
      </div>
      <div class="modal-footer">
        <!-- <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button> -->
        <button type="button" class="btn btn-primary" @click="handleSubmit(data)">Submit</button>
      </div>
    </div>
  </div>
</div>
    </div>
</template>
  

<script>
import { ref } from 'vue';
import { toast } from 'vue3-toastify';

export default {
  props:{
    content :String,
    function : Function,
    addpermission : Function
  },
  setup(props){
    const data = ref({name:''})
    const closebutton = ref(null)
   async  function handleSubmit(value){
 if(props.function){
  try{
    await props.function[0](value).then(data=>{
      if(data.message){
        toast.success(data.message,{
          autoClose: 2000
        })
        if(props.function[1]){
        props.function[1]()
      }
        closebutton.value.click()
         data.value = ref({name:''})
      }
      if(data.error){
        toast.error(data.error,{
          autoClose:2000
        })
      }
    }
    )
  }catch(err){
    toast.error('Operation Failed',{
      autoClose: 2000
    })
  }
 }
 else{
    props.addpermission(value)
    closebutton.value.click()
     data.value = ref({name:''})
 }
   }
   return{
    handleSubmit,
    closebutton,
    data
   }
  }
  
}
</script>