<template>
  <b-row>
    <b-col xl="3" lg="4">
     <b-card>
        <b-card-header class="d-flex justify-content-between">
          <div class="header-title">
            <h4 class="card-title">Add New User</h4>
          </div>
        </b-card-header>
        <b-card-body>
          <form>
            <!-- <div class="form-group">
              <div class="profile-img-edit position-relative">
                <img src="@/assets/images/avatars/01.png" alt="profile-pic"
                  class="theme-color-default-img profile-pic rounded avatar-100" loading="lazy" />
                <img src="@/assets/images/avatars/avtar_1.png" alt="profile-pic"
                  class="theme-color-purple-img profile-pic rounded avatar-100" loading="lazy" />
                <img src="@/assets/images/avatars/avtar_2.png" alt="profile-pic"
                  class="theme-color-blue-img profile-pic rounded avatar-100" loading="lazy" />
                <img src="@/assets/images/avatars/avtar_4.png" alt="profile-pic"
                  class="theme-color-green-img profile-pic rounded avatar-100" loading="lazy" />
                <img src="@/assets/images/avatars/avtar_5.png" alt="profile-pic"
                  class="theme-color-yellow-img profile-pic rounded avatar-100" loading="lazy" />
                <img src="@/assets/images/avatars/avtar_3.png" alt="profile-pic"
                  class="theme-color-pink-img profile-pic rounded avatar-100" loading="lazy" />
                <div class="upload-icone bg-primary">
                  <svg class="upload-button" width="14" height="14" viewBox="0 0 24 24">
                    <path fill="#ffffff"
                      d="M14.06,9L15,9.94L5.92,19H5V18.08L14.06,9M17.66,3C17.41,3 17.15,3.1 16.96,3.29L15.13,5.12L18.88,8.87L20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18.17,3.09 17.92,3 17.66,3M14.06,6.19L3,17.25V21H6.75L17.81,9.94L14.06,6.19Z" />
                  </svg>
                  <input class="file-upload" type="file" accept="image/*" />
                </div>
              </div>
              <div class="img-extension mt-3">
                <div class="d-inline-block align-items-center">
                  <span>Only</span>
                  <a href="javascript:void(0);">.jpg</a>
                  <a href="javascript:void(0);">.png</a>
                  <a href="javascript:void(0);">.jpeg</a>
                  
                  <span> allowed</span>
                </div>
              </div>
            </div> -->
            <div class="form-group">
              <label class="form-label">User role:</label>
              <select type="text" @change="clearError('role')" class="form-control" id="city" placeholder="Select role" v-model="Formdata.role">
                <option value="">Select role</option>
                  <option v-for="(item,index) in all_roles" :value="item.name" :key="index">{{ item.name }}</option>
              </select>
              <span v-if="errors.role" class="error" style="color:red;">{{ errors.role }}</span>
            </div>
          </form>
        </b-card-body>
      </b-card>
    </b-col>
    <div class="col-xl-9 col-lg-8">
      <b-card>
        <b-card-header class="d-flex justify-content-between">
          <div class="header-title">
            <h4 class="card-title">New User Information</h4>
          </div>
        </b-card-header>
        <b-card-body>
          <div class="new-user-info">
            <form  @submit="handleSubmit">
              <b-row>
                <b-col md="6" class="form-group">
                  <label class="form-label" for="fname">Name:</label>
                  <input type="text" class="form-control" @input="clearError('name')" id="fname" placeholder="name" v-model="Formdata.name" />
                  <span v-if="errors.name" class="error" style="color:red">{{ errors.name }}</span>
                </b-col>
                <b-col md="6" class="form-group">
                  <label class="form-label" for="mobno">Phone Number:</label>
                  <input type="number" class="form-control" id="mobno" @input="clearError('phone_number')" placeholder="Phone Number" v-model="Formdata.phone_number" />
                  <span v-if="errors.phone_number" class="error" style="color:red">{{ errors.phone_number.replace('_',' ') }}</span>
                </b-col>
                <b-col md="6" class="form-group">
                  <label class="form-label" for="email">Email:</label>
                  <input type="email" class="form-control" id="email" @input="clearError('email')" placeholder="Email" v-model="Formdata.email" />
                  <span v-if="errors.email" class="error" style="color:red">{{ errors.email }}</span>
                </b-col>
                <b-col md="6" class="form-group">
                  <label class="form-label" for="city">Town/City:</label>
                  <input type="text" class="form-control" id="city" @input="clearError('city_name')" placeholder="Town/City" v-model="Formdata.city_name" />
                  <span v-if="errors.city_name" class="error" style="color:red">{{ errors.city_name.replace('_',' ') }}</span>
                </b-col>
              </b-row>
              <hr />
              <h5 class="mb-3">Security</h5>
              <div class="row">
                <b-col md="6" class="form-group">
                  <label class="form-label" for="uname">User name:</label>
                  <input type="text" class="form-control" id="uname" @input="clearError('userName')" placeholder="User name" v-model="Formdata.userName" />
                  <span v-if="errors.userName" class="error" style="color:red">{{ errors.userName.toLowerCase().replace('',' ') }}</span>
                </b-col>
                <b-col md="6" class="form-group">
                  <label class="form-label" for="pass">Password:</label>
                  <input type="password" class="form-control" id="pass" @input="clearError('password')" placeholder="Password" v-model="Formdata.password" />
                  <span v-if="errors.password" class="error" style="color:red">{{ errors.password }}</span>
                </b-col>
                <!-- <b-col md="6" class="form-group">
                  <label class="form-label" for="rpass">Repeat Password:</label>
                  <input type="password" class="form-control" id="rpass" placeholder="Repeat Password " v-model="Formdata.repeatPassword" />
                </b-col> -->
              </div>
              <!-- <div class="checkbox">
                <label class="form-label"><input class="form-check-input me-2" type="checkbox" value=""
                    id="flexchexked" />Enable Two-Factor-Authentication</label>
              </div> -->
              <button type="submit" class="btn btn-primary">Add New User</button>
            </form>
          </div>
        </b-card-body>
      </b-card>
    </div>
  </b-row>
</template>

<script>
import { onMounted, ref } from 'vue'
// import { useStore } from 'vuex'
// import {userDetails} from '@/service/index.js'
// import store from '@/store';
import { userSignup } from '@/service';
import { useStore } from 'vuex';
import { allRoles } from '@/service';
import { toast } from 'vue3-toastify';

// import { Form } from 'vee-validate';
// import * as Yup from 'yup';

export default {
  setup() {
//     const Schema= Yup.object({
//   name: Yup.string().required('name is required'),
//   email: Yup.string().email('Invalid email address').required('Email is required'),
//   password: Yup.string().min(8, 'Password must be at least 8 characters long').required('Password is required'),
// });
    // const errors = ref({});
    // const store = useStore()
async function fetchRoles () {
  try{
    await allRoles().then(data=> all_roles.value = data)
  }
  catch(err){
    console.log(err)
    toast.error('Server down',{
      autoClose:4000
    })}

}

  const all_roles = ref([])

    onMounted(()=>{
      fetchRoles()
    })
    const errors = ref({})
    const store = useStore()
    // const result = ref(null)
    const Formdata = ref({
      name: '',
      role: '',
      phone_number: '',
      email: '',
      city_name: '',
      userName: '',
      password: '',
    })
    
    // const validateForm = async () => {



    //   try {
    //     await Schema.validate(Formdata, { abortEarly: false });
    //     Object.keys(errors).forEach((key) => {
    //       errors[key] = undefined;
    //     });
    //     return true; // Form is valid
    //   } catch (validationErrors) {
    //     validationErrors.inner.forEach((error) => {
    //       errors[error.path] = error.message;
    //     });
    //     return false; // Form is invalid
    //   }
    // };


       function SubmitUser (payload) {
        userSignup(payload).then(response => response.json()).then(data =>
        {
          if(data.message){
            toast.info(data.message,{
              autoClose:1500
            })
          }
        }
        )
        store.dispatch('handleuserList',payload)
       } 


    const clearError = (key) =>{
      errors.value[key] = ''
    }
    const handleSubmit = async(e) =>
    {
      errors.value = {}
      e.preventDefault()
      const userlist = {...Formdata.value}
      for (let x in userlist) { 
        if(!userlist[x]){
          errors.value[x] = `${x} cannot be empty`
        }
      }
      if (Object.keys(errors.value).length < 1) {
          SubmitUser(userlist)
        }   
    }
    return {
      Formdata,
      handleSubmit,
      clearError,
      errors,
      all_roles  
    }
  }
}
</script>
