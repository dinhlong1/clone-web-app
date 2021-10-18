<template>
  <div class="sidebar color-sidebar">
    <div class="logo-details">
      <i class="bx bxl-facebook"></i>
      <span class="logo_name">Admin Site</span>
    </div>
    <ul class="nav-links">
      <li>
        <router-link to="/admin">
          <a href="#">
            <i class="bx bx-store"></i>
            <span class="links_name">DashBoard</span>
          </a>
        </router-link>
      </li>
      <!-- <li>
        <hr>
        <div class="side-title">
          <h5>Account</h5>
        </div>
      </li> -->
      <li>
        <router-link to="/admin/accounts">
          <a href="#">
            <i class="bx bx-user"></i>
            <span class="links_name">Account List</span>
          </a>
        </router-link>
      </li>
      <li>
        <router-link to="/admin/account/add-account">
          <a href="#">
            <i class="bx bx-user-plus"></i>
            <span class="links_name">Add Account</span>
          </a>
        </router-link>
      </li>
      <li>
        <router-link to="/admin/categories">
          <a href="#">
            <i class="bx bx-book-alt"></i>
            <span class="links_name">Category List</span>
          </a>
        </router-link>
      </li>
      <li>
        <router-link to="/admin/category/add-category">
          <a href="#">
            <i class="bx bx-book-add"></i>
            <span class="links_name">Add Category</span>
          </a>
        </router-link>
      </li>
      <li>
        <router-link to="/admin/users">
          <a href="#">
            <i class="bx bxs-user"></i>
            <span class="links_name">User List</span>
          </a>
        </router-link>
      </li>
      <li>
        <router-link to="/admin/user/add-user">
          <a href="#">
            <i class="bx bxs-user-plus"></i>
            <span class="links_name">Create User</span>
          </a>
        </router-link>
      </li>
      <li>
        <router-link to="/admin/transactions">
          <a href="#">
            <i class="bx bx-transfer"></i>
            <span class="links_name">Transaction</span>
          </a>
        </router-link>
      </li>
      <li>
        <router-link to="/admin/orders">
          <a href="#">
            <i class="bx bx-detail"></i>
            <span class="links_name">Order</span>
          </a>
        </router-link>
      </li>

      <li class="log_in">
      
        <a href="#" @click="goBack()">
          <i class="bx bx-log-out"></i>
          <span class="links_name">Trở về</span>
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "SideBarAdmin",
  methods: {
    goBack(){
      this.$router.push("/")
    }
  }
};
</script>
<style scoped>
#menu {
  background-color: white;
  text-align: center;
}
ol,
ul {
  padding: 0px;
}
.nav-item-head {
  text-align: center;
}
.profile-details {
  text-align: center;
  font-size: 18px;
  color: aliceblue;
  border: 5px solid white;
}
.side-title {
  display: flex;
  align-items: center;
  margin: 0;
  padding: 5px 0px;
  justify-content: center;
}
.side-title h5 {
  color: #f0ebea;
}
hr {
  color: white;
  margin: 0;
}
</style>
