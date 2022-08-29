import {createRouter, createWebHistory} from 'vue-router'
import LoginPage from '../views/LoginPage.vue'
import IndexPage from '../views/IndexPage.vue'
import StatistikPage from '../views/StatistikPage.vue'
import TransaksiPage from '../views/TransaksiPage.vue'
import PickUpPage from '../views/PickUpPage.vue'
import DeliveryPage from '../views/DeliveryPage.vue'
import RiwayatPage from '../views/RiwayatPage.vue'

const routes = [
    {
      path: '/',
      name: 'LoginPage',
      component: LoginPage
    },
    {
      path: '/index',
      name: 'Index',
      component: IndexPage
    },
    {
      path: '/statistik',
      name: 'statistik',
      component: StatistikPage
    },
    {
      path: '/transaksi',
      name: 'transaksi',
      component: TransaksiPage
    },
    {
      path: '/pick-up',
      name: 'pick-up',
      component: PickUpPage
    },
    {
      path: '/delivery',
      name: 'delivery',
      component: DeliveryPage
    },
    {
      path: '/riwayat',
      name: 'riwayat',
      component: RiwayatPage
    }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
