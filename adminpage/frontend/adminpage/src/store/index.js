import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    isLoading: false,
    token: '',
    itemCounts: '',
    IS_OPEN: false,
    page: {active:[]},
    editBtn: false,
    productId: '',
  },
  getters: {
  },
  actions:{
    async storeisOpen(context) {
        const token = localStorage.getItem('token')
        const headers = { 
            'Content-Type': 'application/json',
            'Authorization':'Token '+token
        };
        await axios.get('/api/v1/usr/store-status', {headers})
            .then(response => {
                const a = response.data[0].isOpen;
                if (a == 1) {
                    context.commit("setStoreStatus", true);
                } else {
                    context.commit("setStoreStatus", false);
                }
            })
            .catch(error => {console.log(error)})
    },
    async getAllCartNotif(context){
      const token = localStorage.getItem('token')
      const headers = { 
          'Content-Type': 'application/json',
          'Authorization':'Token '+token
      };
      await axios.get('/api/v1/usr/history-user-cart-lists/', {headers})
          .then(response => {
            const itemCount = parseInt(JSON.stringify(response.data.length))
            context.commit("setCartLists", itemCount);
          })
          .catch(error => {console.log(error)})
    },
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem('token')) {
          state.token = localStorage.getItem('token')
          state.isAuthenticated = true
      } else {
          state.token = ''
          state.isAuthenticated = false
      }
    },
    setIsLoading(state, status) {
      state.isLoading = status
    },
    setStoreStatus(state, status) {
      state.IS_OPEN = status
    },
    setIndex(state, item) {
      state.page.active.push(item)
      localStorage.setItem('pageIsActive', JSON.stringify(state.page)) 
    },
    setEditClickeds(state, dt) {
      state.editBtn = true
      state.productId = dt
    },
    setToken(state, token) {
      state.token = token
      state.isAuthenticated = true
    },
    setCartLists(state, data) {
      state.itemCounts = data
    },
    removeToken(state) {
        state.token = ''
        state.isAuthenticated = false
    },
  },
  modules: {
  }
})
