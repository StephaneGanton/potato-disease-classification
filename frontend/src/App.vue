<template>

<nav class="container-fluid bg-success">
  <div class=" cnt">
    <h3 class="navbar-brand">POTATOES's LEAF DISEASE CLASSIFIER: <span> (select an image to classify)</span></h3>
  </div>
</nav>

 
  <router-view/>
</template>

<style scoped>
#app {
  
}
.container-fluid{
  opacity: .8;
  height: 10vh;
  color: white;
}
.cnt{
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  padding-top: 30px;
  padding-bottom: 20px;
  font-size: larger;
}

span{
  color: yellow;
}

/*nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}*/
</style>
