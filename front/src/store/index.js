import { createStore } from 'vuex'

export default createStore({
  state: {
    userName: ''
  },
  getters: {
    getUserName: state => {
      return state.userName
    }
  },
  mutations: {
    SET_USERNAME: (state, userName) => {
      state.userName = userName
    },
  },
  actions: {
  },
  modules: {
  }
})
