<template>
  <div>
<!-- Modal -->
<div class="modal fade" id="generic" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
<div class="modal-dialog modal-dialog-centered">
  <div class="modal-content">
    <div class="modal-header">
      <h5 class="modal-title" id="staticBackdropLabel">Disclaimer</h5>
      <button  type="button" ref="closebutton" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
    </div>
    <div class="modal-body">
    <p class="m-0 text-dark">Are you Sure you want to Delete "{{ title }}"</p>
    </div>
    <div class="modal-footer">
      <!-- <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button> -->
      <button type="button" @click="proceeding" class="btn text-light btn-danger">Proceed</button>
    </div>
  </div>
</div>
</div>
  </div>
</template>
<script>
import { ref } from 'vue';
export default {
  props:{
    title : String,
    data : Array,
    function : Function
   
  },
  setup(props){
const closebutton = ref(null)
    function proceeding (){
    props.function[0](props.data[1])
    closebutton.value.click()
   }

    return{
    proceeding,
    closebutton
    }
  }
}
</script>