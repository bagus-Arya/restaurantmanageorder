<template>
    <nav class="level">
        <p class="level-item has-text-centered">
            <router-link to="/my-account" class="navbar-item">Profile Saya</router-link>
        </p>
        <p class="level-item has-text-centered">
            <router-link to="/pesanan-saya" class="navbar-item">Riwayat Pick-Up</router-link>
        </p>
        <p class="level-item has-text-centered">
            <router-link to="/riwayat-belanja" class="navbar-item">Riwayat Delivery</router-link>
        </p>
    </nav>
</template>

<script>
  export default {
    name: 'AppNavAkun',
    data: () => ({})
  }
</script>



