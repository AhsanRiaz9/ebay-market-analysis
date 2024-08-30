import { createStore, createLogger } from 'vuex'
import setting from './setting'
import createPersistedState from 'vuex-persistedstate';
const debug = process.env.NODE_ENV !== 'production'
export default createStore({
  state: {
    shareOffcanvas: false,
    userlogin : false,
    accesstoken : '',
    formData : [],
    permissions : null,
    role: null,
    username: null,
    productlink : ''
  },
  getters: {
    shareOffcanvas: (state) => state.shareOffcanvas,
    userlogindetail : (state) => state.userlogin,
    userlist : (state) => state.formData,
    accesstoken : (state) =>  state.accesstoken,
    permissions : (state) => state.permissions,
    role : (state) => state.role,
    username: (state)=> state.username,
    productlink : (state)=> state.productlink
  },
  mutations: {
    openBottomCanvasCommit(state, payload) {
      state[payload.name] = payload.value
    },
    handleuserLogin: (state,payload)=>{
      state.userlogin = payload
      localStorage.setItem('userlogin',payload)
    },
    handleuserList : (state,payload) =>{
      state.formData.push(payload)
    },
    handleAccesstoken : (state,payload) => {
      state.accesstoken = payload
    },
    handleuserpermissions: (state,payload)=>{
      state.permissions = payload
    },
    handlerole : (state,payload)=>{
      state.role = payload
    },
    handleusername: (state,payload)=>{
      state.username = payload
    },
    handleproductLink : (state,payload) =>{
      state.productlink = payload
    }
  },
  actions: {
    openBottomCanvasAction({ commit }, payload) {
      commit('openBottomCanvasCommit', payload)
    },
    handleuserLogin({commit},payload){
      commit('handleuserLogin',payload)
    },
    handleuserList({commit},payload){
      commit('handleuserList',payload)
    },
    handleAccesstoken({commit},payload){
      commit('handleAccesstoken',payload)
    },
    handleuserpermissions({commit},payload){
      commit('handleuserpermissions',payload)
    },
    handlerole({commit},payload){
      commit('handlerole',payload)
    },
    handleusername({commit},payload){
      commit('handleusername',payload)
    },
    handleproductLink({commit},payload){
      commit('handleproductLink',payload)
    },
  },
  modules: {
    setting: setting
  },
  strict: debug,
  plugins: debug ? [createLogger(), createPersistedState({
    key: 'info', 
    paths: ['accesstoken'],
    storage: window.localStorage,
  }),] : []
})
