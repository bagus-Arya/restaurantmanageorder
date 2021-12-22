<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
        <div class="navbar-brand">
            <router-link to="/" class="navbar-item"><strong>Mammamia</strong></router-link>
            <!-- Hamburger Menu -->
            <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu" @click="showMobileMenu = !showMobileMenu">
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
            </a>
        </div>
        <div class="navbar-menu" id="navbar-menu" v-bind:class="{'is-active': showMobileMenu }">
            <div class="navbar-start">
                <div class="navbar-item">
                    <form method="get" action="/search">
                        <div class="field has-addons">
                            <div class="control">
                                <input type="text" class="input" placeholder="Search something" name="query">
                            </div>
                            <div class="control"><button class="button is-sucess"><span class="icon"><i class="fas fa-search"></i></span></button></div> 
                        </div>
                    </form>
                </div>
            </div>
            <div class="navbar-end">
                <router-link to="/pasta" class="navbar-item">Pasta</router-link>
                <router-link to="/salad" class="navbar-item">Salad</router-link>
                <div class="navbar-item">
                    <div class="buttons">
                        <router-link to="/log-in" class="button is-white">Log In</router-link>
                        <router-link to="/cart" class="button is-success">
                            <span class="icon"><i class="fas fa-shopping-cart"></i></span>
                            <span>Cart ({{ cartTotalLength }})</span>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    </nav>

    <!-- Loading Bar -->
    <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading}">
        <div class="lds-dual-ring">
        </div>
    </div>
    
    <section class="section">
        <router-view/>
    </section>
    <footer class="footer">
        <p class="has-text-centered">Copyright (c) 2021</p>
    </footer>
  </div>
</template>

<script>
export default {
    data() {
        return{
            showMobileMenu: false,
            // simpan cart untuk dibawa ke state
            cart: {
                items: [],
            }
        }
        
    },
    mounted(){
        this.cart = this.$store.state.cart
    },
    beforeCreate(){
        this.$store.commit('initializeStore')

    },
    computed:{
        cartTotalLength(){
            let totalLength = 0
            for(let i = 0; i < this.cart.items.length; i++){
                totalLength += this.cart.items[i].quantity
            }
            return totalLength
        }
    }
}
</script>

<style lang="scss">
@import '../node_modules/bulma';


/* loading bar styling */
.lds-dual-ring{
    display:inline-block;
    width: 80px;
    height: 80px;
}

.lds-dual-ring:after{
    content: "";
    display: block;
    width: 64px;
    height: 64px;
    margin: 8px;
    border-radius: 50%;
    border: 6px solid #ccc;
    border-color: #ccc transparent #ccc transparent;
    animation: lds-dual-ring 1.2s linear infinite;
}
@keyframes lds-dual-ring{
    0%{
        transform: rotate(0 deg);
    }
    100%{
        transform: rotate(360 deg);
    }
}

.is-loading-bar{
    height: 0;
    overflow: hidden;
    -webkit-transition: all 0.3s;
    transition: all 0.3s;
    &.is-loading{
        height: 80px;
    }
}



/* end of loading bar styling */
</style>
