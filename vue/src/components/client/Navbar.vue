<template>
  <nav>
    <div class="sidebar-button">
      <i class="bx bx-menu sidebarBtn" @click="activeSidebar()"></i>
    </div>
    <div
      class="profile-details"
      id="dropdownMenuButton2"
      data-bs-toggle="dropdown"
      aria-expanded="false"
       v-if="isLoggedIn != false"
    >
      <img
        src="https://scontent.fsgn8-2.fna.fbcdn.net/v/t1.30497-1/143086968_2856368904622192_1959732218791162458_n.png?_nc_cat=1&ccb=1-5&_nc_sid=7206a8&_nc_ohc=8fru4cWA3v4AX8zmwQg&_nc_ht=scontent.fsgn8-2.fna&oh=bee9d33a8bbba06fe5451674eda94f15&oe=614AD378"
        alt=""
      />
      <div class="admin_name">
        <span>ID: {{id}}</span>
        <span>Coin: {{formatPrice(coins)}}</span>
      </div>
      <button type="button"
        class="btn btn-lg dropdown-toggle dropdown-toggle-split"
        data-bs-toggle="dropdown"
        aria-expanded="false">
        <span class="visually-hidden">Toggle Dropdown</span>
      </button>
      <ul
        class="dropdown-menu dro  pdown-menu-dark"
        aria-labelledby="dropdownMenuButton2"
      >
        <li>
          
          <a class="dropdown-item active" @click="goRecharge()" href="#">Nạp tiền</a>
          
        </li>
        <li>
        
          <a class="dropdown-item" @click="goHistory()" href="#">Lịch sử mua hàng</a>
         
        </li>
        <li>
         
          <a class="dropdown-item" @click="goChangePass()" href="#">Đổi mật khẩu</a>
         
        </li>
        <li>
          <hr class="dropdown-divider"/>
        </li>
        <li>
          <a class="dropdown-item" v-on:click="handleLogout" href="#">Đăng xuất</a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
import { mapState, mapActions } from "vuex";
export default {
  name: "Navbar",
  data() {
    return{
      coins: null,
      id: null,
      }
  },
  mounted(){
  if (this.isLoggedIn != false) {
      this.getProfile();
    }
  },
  computed: {
    ...mapState(["isLoggedIn", "user"]),
  },
  methods:{
    ...mapActions(["logout"]),
    activeSidebar() {
      let sidebar = document.querySelector(".sidebar");
      let sidebarBtn = document.querySelector(".sidebarBtn");
      if (sidebarBtn) {
        sidebarBtn.onclick = function() {
          sidebar.classList.toggle("active");
          if (sidebar.classList.contains("active")) {
            sidebarBtn.classList.replace("bx-menu", "bx-menu-alt-right");
          } else sidebarBtn.classList.replace("bx-menu-alt-right", "bx-menu");
        };
      }
    }, 
    getProfile() {
      if (this.user != null){
        this.coins = this.user.coin;
        this.id = this.user.id;
      }

    },
    goRecharge(){
      this.$router.push("/recharge")
    },
    goHistory(){
      this.$router.push("/user/history")
    },
    goChangePass(){
      this.$router.push("/user/change-password")
    },
   formatPrice(value) {
      let val = (value / 1).toFixed(0).replace(".", ",");
      return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    },
    handleLogout(event) {
      event.preventDefault();
      this.logout();
      this.$router.push("/login");
    },
}
}
</script>
