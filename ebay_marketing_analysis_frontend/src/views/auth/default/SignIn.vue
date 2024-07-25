<template>
  <section class="login-content">
    <b-row class="m-0 align-items-center bg-white h-100">
      <b-col md="6">
        <b-row class="justify-content-center">
          <b-col md="10">
            <b-card class="card-transparent shadow-none d-flex justify-content-center mb-0 auth-card iq-auth-form">
              <h2 class="mb-2 text-center">Welcome to Pricing Tool</h2>
              <p class="text-center">Sign In </p>
              <form
              @submit="handlesubmit"
              >
                <div class="row">
                  <div class="col-lg-12">
                    <div class="form-group">
                      <label for="email" class="form-label">Email</label>
                      <input type="email" class="form-control" id="email" @input="()=>{
                        errors.email = ''
                      }" v-model="data.email" aria-describedby="email" placeholder=" " />
                      <span style="color: red">{{ errors.email }}</span>
                    </div>
                  </div>
                  <div class="col-lg-12">
                    <div class="form-group">
                      <label for="password" class="form-label">Password</label>
                      <input type="password" class="form-control" @input="()=>{errors.password=''}" v-model="data.password" id="password" aria-describedby="password" placeholder=" " />
                      <span style="color: red;">{{ errors.password }}</span>
                    </div>
                  </div>
                  <!-- <div class="col-lg-12 d-flex justify-content-between">
                    <div class="form-check mb-3">
                      <input type="checkbox" class="form-check-input" id="customCheck1" />
                      <label class="form-check-label" for="customCheck1">Remember Me</label>
                    </div>
                  </div> -->
                </div>
                <div class="d-flex justify-content-center">
                <button :disabled="loading" type="submit" class="btn btn-primary">Sign In</button>
                </div>
              </form>
            </b-card>
          </b-col>
        </b-row>
      </b-col>
      <div class="col-md-6 d-md-block d-none bg-primary p-0 vh-100 overflow-hidden">
        <img src="@/assets/images/auth/01.png" class="img-fluid gradient-main animated-scaleX" alt="images" loading="lazy" />
      </div>
    </b-row>
  </section>
</template>

<script>
import { useStore } from 'vuex';
import {loginUser} from '@/service/index.js'
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { toast } from 'vue3-toastify';
export default {
  setup () {
const store = useStore()
const router = useRouter()
const loading = ref(false)
const errors = ref({
  email:'',
  password:''
})
const data = ref({
  email :'',
  password : ''
})
async function handlesubmit(e){
  e.preventDefault()
  loading.value = true
  if(data.value.email == '' && data.value.password == ''){
    errors.value.email = 'email cannot be empty'
  errors.value.password = 'password cannot be empty'
  loading.value = false
  }
  else if(data.value.email == ''){
    errors.value.email = 'email cannot be empty'
    loading.value = false
  }
  else if(data.value.password == ''){
    errors.value.password = 'password cannot be empty'
  loading.value = false
  }
  else{
    try{
    const response = await loginUser(data.value)
    if(response.access){
     await store.dispatch('handleAccesstoken',response.access)
      toast.success('login Successful',{autoClose:1700})
    if(store.getters.accesstoken){
      setTimeout(() => {
        router.push('/')
      }, 1200);
    }
}
if(!response.access){
  toast.error(response.detail,{
    autoClose:1700
  })
}
loading.value = false
}
catch(error){
  toast.error('Login Failed',{
    autoClose:1700
  })
  loading.value = false
} 
}
}
return {
    errors,
    loading,
    data,
    handlesubmit
  }  
}
}
</script>

<style lang="scss" scoped></style>
