const UsersPermission = [{
  id: 1,
  name: 'Create Users',
  allowed: false  
},{
    id: 2,
    name: 'View Users',
    allowed: false    
  },{
    id: 3,
    name: 'Update Users',
    allowed: false   
  },{
    id: 4,
    name: 'Delete Users',
    allowed: false    
  }]
const RolePermission = [{
    id: 1,
    name: 'Create Roles',
    allowed: false  
  },{
      id: 2,
      name: 'View Roles',
      allowed: false    
    },{
      id: 3,
      name: 'Update Roles',
      allowed: false    
    },{
      id: 4,
      name: 'Delete Roles',
      allowed: false    
    }]
 const ProductPermission = [{
  id: 1,
  name : 'Edit Product'
 },{
  id: 2,
  name: 'Create Product'},{
  id: 3,
  name: 'Delete Product'
  }
]   
const roles = ['User','Admin','SuperAdmin','Owner','Vendor']
const Modules = ['User','Product','Roles']
export default {UsersPermission,RolePermission,roles,Modules,ProductPermission}  