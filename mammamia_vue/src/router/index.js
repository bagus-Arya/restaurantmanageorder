import {createRouter, createWebHistory} from 'vue-router'
import Home from '../views/Home.vue'
import Product from '../views/Product.vue'
import Category from '../views/Category.vue'
import Search from '../views/Search.vue'
import Cart from '../views/Cart.vue'
import Signup from '../views/Signup.vue'
import Login from '../views/Login.vue'
import MyAccount from '../views/MyAccount.vue'
import ReviewCart from '../views/ReviewCart.vue'
import PesananSaya from '../views/MyOrder.vue'
import RiwayatBelanja from '../views/HistoryOrder.vue'
import MostOrdered from '../views/MostOrdered.vue'
import CheckOut from '../views/CheckOut.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/most-ordered',
    name: 'MostOrdered',
    component: MostOrdered
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    },
    {
    path: '/:category_slug/:product_slug',
    name: 'Product',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component:Product
    },
    {
    path: '/:category_slug',
    name: 'Category',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component:Category
    },
    {
    path: '/search',
    name: 'Search',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component:Search
    },
    {
    path: '/cart',
    name: 'Cart',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component:Cart
    },
    {
    path: '/review-cart',
    name: 'ReviewCart',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component:ReviewCart
    },
    {
    path: '/check-out',
    name: 'CheckOut',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component:CheckOut
    },
    {
    path: '/sign-up',
    name: 'Signup',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component:Signup
    },
    {
    path: '/log-in',
    name: 'Login',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component:Login
    },
    {
    path: '/my-account',
    name: 'MyAccount',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: MyAccount,
    meta: {
        requireLogin:true
      }
    },
    {
    path: '/pesanan-saya',
    name: 'PesananSaya',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: PesananSaya,
    meta: {
        requireLogin:true
      }
    },
    {
    path: '/riwayat-belanja',
    name: 'RiwayatBelanja',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: RiwayatBelanja,
    meta: {
        requireLogin:true
      }
    },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// router.beforeEach((to, from, next) => {
//     if (to.name !== 'Login' && !store.state.isAuthenticated) next({ name: 'Login', query: {to: to.path}})
//     else next()
// })

export default router
