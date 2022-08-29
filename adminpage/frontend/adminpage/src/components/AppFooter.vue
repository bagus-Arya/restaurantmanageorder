<template>
  <footer class="footer mt-5">
    <div class="columns is-1-mobile is-0-tablet is-3-desktop">
      <div class="column is-1"></div>
      <div class="column has-text-centered-mobile is-one-quarter">
        <h1 class="is-size-4">MAMMA MIA</h1>
        <p>Cabang Renon</p>
        <p>Jalan Tukad Jinah No.5 Renon</p>
      </div>
      <div class="column has-text-centered">
        <div class="columns">
          <div class="column">
            <img src="@/assets/logo_mammamia.png" alt="logo-mammamia" style="width:125px;"/>
            <div class="columns is-mobile mt-5">
              <div class="column is-size-4">
                <span class="icon has-text-danger">
                  <a href="https://www.facebook.com/mammamia.renon/"><i class="fa fa-facebook-f"></i></a>
                </span>
                <span class="icon has-text-danger pl-5 pr-5">
                  <a href="https://www.instagram.com/mammamiarenon/"><i class="fa fa-instagram"></i></a>
                </span>
                <span class="icon has-text-danger">
                  <a href="https://api.whatsapp.com/send/?phone=628113980918"><i class="fa fa-phone"></i></a>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="column has-text-centered is-size-5">
        AUTHENTIC WOOD FIRED PIZZA <br> TRADITIONAL ITALIAN 
        <br> HOME COOKING
      </div>
      <div class="column is-1"></div>
    </div>
  </footer>
</template>

<script>
  export default {
    name: 'AppFooter',
    data: () => ({})
  }
</script>

<style lang="scss">
@import '~bulma/css/bulma.css';

</style>





