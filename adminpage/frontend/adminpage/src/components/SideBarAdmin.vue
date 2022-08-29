<template>
  <aside class="column has-background-warning-light is-3 is-narrow-mobile is-fullheight section is-hidden-mobile menu">
    <ul class="menu-list">
      <li>
        <div class="columns is-mobile">
          <div class="column">
            <img src="@/assets/logo_mammamia.png" alt="logo-mammamia" style="width:125px;"/>
          </div>
          <div class="column is-size-5 mt-5">
            <h1>MAMMA MIA Renon</h1>
          </div>
        </div>
      </li>
      <li>
        <a href="/index" @click='setIndex()' :class="{'is-active' : isActivateIndex}">
          <span class=""><i class=""></i></span> Input Produk
        </a>
      </li>
      <li>
        <a href="/statistik" @click='setStatistik()' :class="{'is-active' : isActivateStatistik}">
          <span class=""><i class=""></i></span> Statistik Penjualan
        </a>
      </li>
      <li>
        <a href="/transaksi" @click='setTransaksi()' :class="{'is-active' : isActivateTransaksi}">
          <span class=""><i class=""></i></span> Transaksi ({{$store.state.itemCounts?$store.state.itemCounts:'0'}})
        </a>
        <ul>
          <li>
            <a href="/pick-up">
              <span class=""><i class=""></i></span> Pick-Up
            </a>
          </li>
          <li>
            <a href="/delivery">
              <span class=""><i class=""></i></span> Delivery
            </a>
          </li>
        </ul>
      </li>
      <li>
        <a href="/riwayat" @click='setRiwayat()' :class="{'is-active' : isActivateRiwayat}">
          <span class=""><i class=""></i></span> Riwayat
        </a>
      </li>
      <li>
        <button @click='logout()' class="button is-danger">Keluar</button>
        <button v-if="$store.state.IS_OPEN === true" @click='updateStatus()' class="button is-primary mt-3">Tutup Restauran Sekarang</button>
        <button v-else @click='updateStatus()' class="button is-primary mb-5">Buka Restauran</button>
      </li>
    </ul>
  </aside>
</template>

<script>
import axios from 'axios'
import {toast} from 'bulma-toast'

export default {
    name: 'SideBarAdmins',
    data: () => ({
      isActivateIndex : '',
      isActivateStatistik : '',
      isActivateTransaksi : '',
      isActivateRiwayat : '',
    }),
    beforeCreate(){
      this.$store.dispatch('storeisOpen')
      this.$store.dispatch('getAllCartNotif')
    },
    created(){
      const data = JSON.parse(localStorage.getItem('pageIsActive'))
      this.isActivateIndex = data.active[0].isActivateIndex,
      this.isActivateStatistik = data.active[0].isActivateStatistik,
      this.isActivateTransaksi = data.active[0].isActivateTransaksi,
      this.isActivateRiwayat = data.active[0].isActivateRiwayat
    },
    methods:{
      logout(){
        axios.defaults.headers.common['Authorization'] = ''
        localStorage.removeItem('token')
        localStorage.removeItem('username')
        localStorage.removeItem('password')
        localStorage.removeItem('userid')
        localStorage.removeItem('pageIsActive')
        this.$store.commit('removeToken')
        this.$router.push({name:'LoginPage'})
      },
      setIndex(){
        const dataActive = {
          isActivateIndex : true,
          isActivateStatistik : false,
          isActivateTransaksi : false,
          isActivateRiwayat : false
        }
        this.$store.commit('setIndex', dataActive)
      },
      setStatistik(){
        const dataActive = {
          isActivateIndex : false,
          isActivateStatistik : true,
          isActivateTransaksi : false,
          isActivateRiwayat : false
        }
        this.$store.commit('setIndex', dataActive)
      },
      setTransaksi(){
        const dataActive = {
          isActivateIndex : false,
          isActivateStatistik : false,
          isActivateTransaksi : true,
          isActivateRiwayat : false
        }
        this.$store.commit('setIndex', dataActive)
      },
      setRiwayat(){
        const dataActive = {
          isActivateIndex : false,
          isActivateStatistik : false,
          isActivateTransaksi : false,
          isActivateRiwayat : true
        }
        this.$store.commit('setIndex', dataActive)
      },
      async updateStatus(){
          if (this.$store.state.IS_OPEN === true) {
             const token = localStorage.getItem('token')
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            const updateStatuss = JSON.stringify({
              isOpen: 0
            });
            await axios
                  .put('/api/v1/usr/store-status-update/', updateStatuss, {headers})
                  .then(response=>{
                      if (!response) {
                          toast({
                              message: 'Data Sudah Ada',
                              type: 'is-danger',
                              dismissible: true,
                              pauseOnHover: true,
                              duration: 5000,
                              position: 'top-right',
                          })
                          this.$router.go()
                          return response
                      } else {
                          toast({
                              message: 'Restauran Berhasil Ditutup',
                              type: 'is-success',
                              dismissible: true,
                              pauseOnHover: true,
                              duration: 10000,
                              position: 'top-right',
                          })
                          this.$router.go()
                          return response
                      }
                  })
                  .catch(error => {
                      if (error.response){
                          for (const property in error.response.data){
                              this.errors.push(`${property}: ${error.response.data[property]}`)
                          }
                          console.log(JSON.stringify(error.response.data))
                      }else if(error.message){
                          this.errors.push('Something went wrong, please try again')
                          console.log(JSON.stringify(error))
                      }
                  });
          } else {
            const token = localStorage.getItem('token')
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            const updateStatuss = JSON.stringify({
              isOpen: 1
            });
            await axios
                  .put('/api/v1/usr/store-status-update/', updateStatuss, {headers})
                  .then(response=>{
                      if (!response) {
                          toast({
                              message: 'Data Sudah Ada',
                              type: 'is-danger',
                              dismissible: true,
                              pauseOnHover: true,
                              duration: 5000,
                              position: 'top-right',
                          })
                          this.$router.go()
                          return response
                      } else {
                          toast({
                              message: 'Restauran Berhasil Ditutup',
                              type: 'is-success',
                              dismissible: true,
                              pauseOnHover: true,
                              duration: 10000,
                              position: 'top-right',
                          })
                          this.$router.go()
                          return response
                      }
                  })
                  .catch(error => {
                      if (error.response){
                          for (const property in error.response.data){
                              this.errors.push(`${property}: ${error.response.data[property]}`)
                          }
                          console.log(JSON.stringify(error.response.data))
                      }else if(error.message){
                          this.errors.push('Something went wrong, please try again')
                          console.log(JSON.stringify(error))
                      }
                  });
          }  
      }
    }
  }
</script>

<style lang="scss">
@import '~bulma/css/bulma.css';

  .menu {
    position: sticky;
    display: inline-block;
    vertical-align: top;
    max-height: 100vh;
    overflow-y: auto;
    width: 200px;
    top: 0;
    bottom: 0;
    padding: 30px;
  }
</style>