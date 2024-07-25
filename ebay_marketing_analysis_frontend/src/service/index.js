import store from '@/store/index.js'
import Urls from './urls/index.js'


function getUserauth() {
  const Token = store.state.accesstoken
  return Token
}

// export const deleteUser = async(data) =>{
//   const url = Urls.
// }

export const loginUser = async (data) => {
  const url = Urls.loginUser
  return await fetch(url, { method: 'POST', headers: { 'Content-Type': 'Application/json' }, body: JSON.stringify(data) })
    .then((response) => response.json())
    .then((data) => data)
}
export const userLists = async () => {
  const url = Urls.userDetail
  const Token = getUserauth()
  return await fetch(url, { method: 'GET', headers: { Authorization: 'Bearer ' + Token } }).then((response) => response.json())
}
export const removeUser = async (value) => {
  const url = Urls.userDelete
  const Token = getUserauth()
  return await fetch(url + value + '/', { method: 'Delete', headers: { Authorization: 'Bearer ' + Token } }).then((response) => response.json())
}
export const deleteModule = async (value) => {
  const url = Urls.deleteModule
  const Token = getUserauth()
  return await fetch(url + value + '/', { method: 'Delete', headers: { 'Content-Type': 'Application/json', Authorization: 'Bearer ' + Token } }).then((response) => response.json())
}
export const userSignup = async (data) => {
  const url = Urls.userSignup
  const Token = getUserauth()
  return await fetch(url, { method: 'POST', headers: { 'Content-Type': 'Application/json', Authorization: 'Bearer ' + Token}, body: JSON.stringify(data) })
}

export const allRoles = async () => {
  const url = Urls.roles
  const Token = getUserauth()
  return await fetch(url, { method: 'GET', headers: { Authorization: 'Bearer ' + Token } }).then((response) => response.json())
}
export const addRoles = async (value) => {
  const url = Urls.addRole
  const Token = getUserauth()
  return await fetch(url, { method: 'POST', headers: { 'Content-Type': 'Application/json', Authorization: 'Bearer ' + Token }, body: JSON.stringify(value) }).then((response) => response.json())
}
export const deleteRoles = async (value) => {
  const url = Urls.deleteRole
  const Token = getUserauth()
  return await fetch(url + value + '/', { method: 'DELETE', headers: { 'Content-Type': 'Application/json', Authorization: 'Bearer ' + Token } }).then((response) => response.json())
}
export const getModules = async () => {
  const url = Urls.getModules
  const Token = getUserauth()
  return await fetch(url, { method: 'GET', headers: { Authorization: 'Bearer ' + Token } }).then((response) => response.json())
}
export const addModules = async (data) => {
  const url = Urls.addModules
  const Token = getUserauth()
  return await fetch(url, { method: 'POST', headers: { 'Content-Type': 'Application/json', Authorization: 'Bearer ' + Token }, body: JSON.stringify(data) }).then((response) => response.json())
}
export const getPermissions = async () => {
  const url = Urls.modulePermissions
  const Token = getUserauth()
  return await fetch(url, { method: 'GET', headers: { Authorization: 'Bearer ' + Token } }).then((response) => response.json())
}
export const deletePermissions = async (value) => {
  const url = Urls.deletePermissions
  const Token = getUserauth()
  return await fetch(url + value + '/', { method: 'DELETE', headers: { 'Content-Type': 'Application/json', Authorization: 'Bearer ' + Token } }).then((response) => response.json())
}
export const addPermissions = async (data) => {
  const url = Urls.addPermissions
  const Token = getUserauth()
  return await fetch(url, { method: 'POST', headers: { 'Content-Type': 'Application/json', Authorization: 'Bearer ' + Token }, body: JSON.stringify(data) }).then((response) => response.json())
}
export const updaterolepermissions = async (id, data) => {
  const url = Urls.roles
  const Token = getUserauth()
  return await fetch(url + id + '/', { method: 'PUT', headers: { 'Content-Type': 'Application/json', Authorization: 'Bearer ' + Token }, body: JSON.stringify(data) }).then((response) => response.json())
}

export const checkRoute = async (permissions, name, permission) => {
if(permissions){
  const result = permissions?.permissions[name]?.some((i) => i.name == permission)
  return await result
}
else{
  return false
}
}

export const callProducts = async(value = 1)=>{
  const url = Urls.ebay_products
  return await fetch(url+value,{method:'GET'}).then((response) => response.json())
}