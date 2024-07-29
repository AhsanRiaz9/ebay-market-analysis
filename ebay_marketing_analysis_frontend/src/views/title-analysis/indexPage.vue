<template>

<div>
    <b-card>
    <div class="px-5 d-flex justify-content-between"><input type="text" placeholder="Search for title placement" class="title-search"><button class="btn-apply">Apply</button></div>
    </b-card>
<b-card>
    <h5 class="mb-4 fw-bold">Top 10 Selling Titles <ExclamationCircleIcon/></h5>
<div class="d-flex flex-column gap-3">
    <div v-for="(item,index) in response" :key="index"  class="title-text">
        <p>Shockproof Case Magnetic Cover</p>
    </div>
</div>    
</b-card>        
</div> 
   
</template>




<script>



import ExclamationCircleIcon from '@/components/icons/outlined/svg-icons/ExclamationCircleIcon.vue';
import { ref } from 'vue';


export default {
    components:{ExclamationCircleIcon},
setup () {
    const response = ref([])

    return{
        response
    }
}
}


</script>
<style scoped>

.title-search{
    border: 2px solid black;
    border-radius: 24px;
    padding: 10px 20px;
    width: 90%;
}
.title-text{
    border: 1px solid #dddfe2;
    padding: 15px;
    border-radius: 25px;
}
.title-text > p{
    color: black;
    font-weight: 600;
    margin: 0;
}
.btn-apply{
    border: 2px solid black;
    border-radius: 18px;
    transition: .5s;
    padding: 0px 20px;
    color: black;
    font-weight: 600;
}
.btn-apply:hover{
    background-color: black;
    color: white;
}

</style>