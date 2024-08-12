const baseUrl = process.env.VUE_APP_LOGIN_API_URL

const loginUser =  baseUrl + 'api/token/'
const userDelete = baseUrl + 'users/'
const userDetail = baseUrl + 'users/'
const userSignup = baseUrl + 'users/'
const addModules = baseUrl + 'modules/'
const getModules = baseUrl + 'modules/'
const deleteModule = baseUrl + 'modules/'
const deleteRole = baseUrl + 'roles/'
const addRole = baseUrl + 'roles/'
const roles = baseUrl + 'roles/'
const addPermissions = baseUrl + 'permissions/'
const deletePermissions = baseUrl + 'permissions/'
const modulePermissions = baseUrl + 'permissions/'
const ebay_products = baseUrl + 'ebay_products/mobile_phones/?page='
const conditions = baseUrl + 'product_configuration/conditions/'
const tokenValidate = baseUrl + 'api/token/validate/'
const productFilters = baseUrl + 'product_configuration/product_filters/'


const URLS = {
    loginUser,
    addModules,
    addPermissions,
    deletePermissions,
    modulePermissions,
    deleteModule,
    userDelete,
    deleteRole,
    addRole,
    userDetail,
    userSignup,
    getModules,
    roles,
    ebay_products,
    conditions,
    tokenValidate,
    productFilters
}

export default URLS