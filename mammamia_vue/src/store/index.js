import { createStore, createLogger } from 'vuex'
import axios from 'axios'
import {toast} from 'bulma-toast'

const debug = process.env.NODE_ENV !== 'production'

export default createStore({
    state: {
        items:[],
        dataIdHistoryCart:[],
        isLoading: false,
        isAuthenticated: false,
        IS_CLICKED: false,
        IS_CEKONGKIR: false,
        IS_OPEN: false,
        token: '',
        uid: '',
    },
    getters: {
        isCartCount (state) {
            return state.items.reduce((acc, curVal) =>{
                return acc += parseInt(curVal.quantity)
            },0)
        },
        isIdCartHistory (state) {
            return state.dataIdHistoryCart
        }
    },
    actions:{
        async storeisOpen(context) {
            const token = localStorage.getItem('token')
            const decodeValueTkn = atob(token);
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValueTkn
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
        async getAllCartLists(context){
            const token = localStorage.getItem('token')
            const uIds = localStorage.getItem('uid')
            const decodeValueTkn = atob(token);
            const decodeValueId = atob(uIds);
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValueTkn
            };
                context.commit("setIsLoading", true)
            await axios.get(`/api/v1/usr/cart-lists/${decodeValueId}/`, {headers})
                .then(response => {
                    context.commit("setCartData", response.data)
                    
                })
                .catch(error => {
                    toast({
                        message: 'Login Dulu Ya',
                        type: 'is-danger',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 5000,
                        position: 'center',
                      })
                })
                context.commit("setIsLoading", false)
        },
        async getAllCartHistoryIdLists(context){
            const token = localStorage.getItem('token')
            const decodeValueTkn = atob(token);
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValueTkn
            };
                context.commit("setIsLoading", true)
            await axios.get('/api/v1/usr/cart-lists-id', {headers})
                .then(response => {
                    context.commit("setHistoryIdData", response.data)
                    
                })
                .catch(error => {
                    if (error) {
                        toast({
                            message: 'Login Dulu Ya',
                            type: 'is-danger',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 5000,
                            position: 'center',
                        })
                    }
                })
                context.commit("setIsLoading", false)
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
        setCartData(state, dataC) {
            state.items = dataC
        },
        setHistoryIdData(state, dataId) {
            state.dataIdHistoryCart = dataId
        },
        setToken(state, token) {
            state.token = token.tokens
            state.uid = token.uIds
            state.isAuthenticated = true
        },
        setButtonCartClick(state) {
            state.IS_CLICKED = true
        },
        setButtonCekOngkir(state, status) {
            state.IS_CEKONGKIR = status
        },
        setButtonCartFalse(state) {
            state.IS_CLICKED = false
        },
        removeToken(state) {
            state.token = ''
            state.uid = ''
            state.isAuthenticated = false
        }
    },
    modules: {
   
    },
    strict: debug,
    plugins: debug ? [createLogger()] : []
})