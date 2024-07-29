<template>
  <tr v-for="(item, index) in list" :key="index">
    <!-- <td class="text-center"><img class="bg-soft-primary rounded img-fluid avatar-40 me-3" :src="item.image" alt="profile" loading="lazy" /></td> -->
    <td>{{ item.name }}</td>
    <td>{{ item.phone_number }}</td>
    <td>{{ item.email }}</td>
    <td>{{ item.role }}</td>
    <td>
      <div class="flex align-items-center list-user-action">
        <!-- <a class="btn btn-sm btn-icon btn-success mx-1" data-bs-toggle="tooltip" data-bs-placement="top" title="Add" href="#">
          <span class="btn-inner">
            <icon-component type="outlined" icon-name="user-add" />
          </span>
        </a> -->
        <a class="btn btn-sm btn-icon btn-warning mx-1" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="Edit" href="#">
          <span class="btn-inner">
            <icon-component type="outlined" icon-name="pencil-alt" />
          </span>
        </a>
        <a @click="deleteuser(index)" class="btn btn-sm btn-icon btn-danger mx-1" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="Delete" href="#">
          <span class="btn-inner">
            <icon-component type="outlined" icon-name="trash" />
          </span>
        </a>
      </div>
    </td>
  </tr>
</template>
<script>
export default {
  props: {
    list:Array
  },
  setup(){  
    function deleteuser(index){
      const userlist = JSON.parse(localStorage.getItem('user-list'))
      userlist.formData.splice(index,1)
      console.log(userlist)
      localStorage.setItem('user-list',JSON.stringify(userlist))
    }
    return{
      deleteuser
    }
  }

}
</script>
