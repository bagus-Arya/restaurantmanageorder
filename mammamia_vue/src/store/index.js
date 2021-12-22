import { createStore } from 'vuex'

export default createStore({
    state: {
        cart: {
            items: [],
        },
        isAuthenticated: false,
        token: '',
        isLoading: false,
  },
    mutations: {
        initializeStore(state) {
            if (localStorage.getItem('cart')) {
                state.cart = JSON.parse(localStorage.getItem('cart'))
            }
            else {
                // If cart blm dibuat, maka buat baru 
                localStorage.setItem('cart', JSON.stringify(state.cart))
            }
            if (localStorage.getItem('token')) {
                state.token = localStorage.getItem('token')
                state.isAuthenticated = true
            } else {
                state.token = ''
                state.isAuthenticated = false
            }

        },
        addToCart(state, item) {
            // variabel exist untuk mengecek jika item yg ingin ditambahkan ke cart sudah ada di cart
            const exist = state.cart.items.filter(i => i.product.id == item.product.id)
            
            if (exist.length) {
                exist[0].quantity = parseInt(exist[0].quantity) + parseInt(item.quantity)
            } else {
                // jika tidak ada dalam cart, tambahkan ke object cart (atribut items)
                state.cart.items.push(item)
            }
            localStorage.setItem('cart', JSON.stringify(state.cart))
        },
        setIsLoading(state, status) {
            state.isLoading = status
            
        }
  },
  actions: {
  },
  modules: {
  }
})
