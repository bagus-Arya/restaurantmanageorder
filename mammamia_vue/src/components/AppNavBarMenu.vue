<template>
  <nav class="level">
    <p class="level-item has-text-centered">
      <router-link to="/pizza" class="navbar-item">PIZZA</router-link>
    </p>
    <p class="level-item has-text-centered">
      <router-link to="/starters" class="navbar-item">STARTERS</router-link>
    </p>
    <p class="level-item has-text-centered">
      <router-link to="/most-ordered" class="navbar-item is-size-4">MOST ORDERED</router-link>
    </p>
    <p class="level-item has-text-centered">
      <router-link to="/main" class="navbar-item">MAIN</router-link>
    </p>
    <p class="level-item has-text-centered">
      <router-link to="/salad" class="navbar-item">SALAD</router-link>
    </p>
  </nav>
</template>

<script>
  export default {
    name: 'AppNavBarMenu',
    data: () => ({})
  }
</script>



