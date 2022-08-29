<template>
  <div class="hero">
    <div class="hero is-fullheight is-dark has-background">
      <img alt="burger background" class="hero-background is-transparent" src="@/assets/images/bghome.jpeg" />
      <div class="hero-body">
        <div class="container has-text-centered">
          <h1 v-if="($store.state.IS_OPEN === false) && ($store.state.isAuthenticated === true)" class="title">Maaf Restauran Sedang Tutup</h1>
          <h1 class="title">
            WELCOME TO <br>MAMMAMIA 
          </h1>
          <h3 class="subtitle">
            PIZZA & PASTA
          </h3>
          <a class="button is-danger is-rounded p*-4" href="#latestProduct" >ORDER PICK-UP OR DELIVERY</a>
        </div>
      </div>
    </div>
  <div class="container mt-5 mb-5">
    <div v-if="this.$store.state.isAuthenticated === true" class="columns is-multiline">
      <div class="column is-12" id="latestProduct">
        <h2 class="is-size-2 has-text-centered">Latest Product</h2>
      </div>
      <ProductBox
        v-for="product in latestProducts"
        v-bind:key="product.id"
        v-bind:product="product" />
    </div>
    <div class="columns is-1-mobile is-0-tablet">
        <div class="column">
            <img alt="burger background" src="@/assets/images/bghome.jpeg" />
        </div>
        <div class="column has-text-centered">
          <br>
          <br>
          <br>
          <br>
          <br>
          <h1 class="title">Our Core Value</h1>
          <br>
          <p>
            Mamma Mia Renon is one of cozy italian restauran in Bali
          </p>
        </div>
    </div>
    <div class="columns is-1-mobile is-0-tablet">
        <div class="column has-text-centered">
          <br>
          <br>
          <br>
          <br>
          <br>
          <h1 class="title">Our Core Value</h1>
          <br>
          <p>
            Mamma Mia Renon is one of cozy italian restauran in Bali
          </p>
        </div>
        <div class="column">
            <img alt="burger background" src="@/assets/images/bghome.jpeg" />
        </div>
    </div>
  </div>
</div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios'
import ProductBox from '@/components/ProductBox.vue'
import asyncDataLogin_ready from '@/mixins/asyncDataLogin'

export default {
  name: 'Home',
  data(){
    return{
      latestProducts: []
    }
  },
  components: {
    ProductBox,
  },
  mounted(){
    document.title = 'Home'+ ' | mammamia'
  },
  created(){
    this.getLatestProducts()
  },
  beforeCreate(){
    this.$store.dispatch('storeisOpen')
  },
  methods: {
    async getLatestProducts(){
        const token = localStorage.getItem('token')
        const decodeValue = atob(token);
          const headers = { 
              'Content-Type': 'application/json',
              'Authorization':'Token '+decodeValue
          };
        this.$store.commit('setIsLoading', true)
        await axios.get('/api/v1/latest-products/', {headers})
        .then(response => {
          this.latestProducts = response.data
        }).catch(error => {console.log(error)})
        this.$store.commit('setIsLoading', false)
    },
  }
}
</script>

<style lang="scss">
@import '~bulma/css/bulma.css';

.hero.has-background {
  position: relative;
  overflow: hidden;
}
.hero-background {
  position: absolute;
  object-fit: cover;
  object-position: center center;
  width: 100%;
  height: 100%;
}
.hero-background.is-transparent {
  opacity: 0.3;
}
</style>



