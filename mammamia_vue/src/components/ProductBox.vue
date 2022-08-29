<template>
    <div class="column is-3">
        <div class="box">
            <figure class="image mb-4">
                <img :src="product.get_thumbnail" alt="thumbnail">
            </figure>
            <router-link v-bind:to="product.get_absolute_url" class="navbar-item">
                <h3 class="is-size-4">{{product.name}}</h3>
            </router-link>
                <p class="is-size-6">Size: {{product.size}}</p>
                <p class="is-size-6 has-text-grey">Rp. {{formatPrices(product.price)}}</p>
                <p >{{product.description}}</p>
            <router-link v-if="($store.state.IS_OPEN === true) && ($store.state.isAuthenticated === true)" v-bind:to="product.get_absolute_url" class="button is-primary mt-4 is-fullwidth">Pesan</router-link>
            <router-link v-else to="#" class="button is-primary mt-4 is-fullwidth">Pesan</router-link>
        </div>
    </div>
</template>

<script>
import { formatPrice } from '@/utils/function'

export default {
    name: 'ProductBox',
    props:{
        product:Object,
    },
    methods:{
        formatPrices(harga) {
            var hargas = parseInt(harga)
            var hargat = formatPrice(hargas);
            return hargat;
        },
    }
}
</script>

<style scoped>
    .image{
        margin-top: -1.25 rem;
        margin-left:-1.25 rem;
        margin-bottom:-1.25 rem;
    }

</style>

