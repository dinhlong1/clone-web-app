<template>
  <div class="sidebar">
    <div class="logo-details">
      <i class="fab fa-facebook-f"></i>
      <span class="logo_name">KD37</span>
    </div>
    <!-- <div class="profile-details" v-if="isLoggedIn == true">
      <div class="name-job">
        <div class="profile_name">{{ email }}</div>
        <div class="job">{{ formatPrice(coins) }} Coin</div>
      </div>
    </div> -->
    <ul class="nav-links">
      <li>
        <router-link to="/">
          <a href="#">
            <i class="bx bx-store"></i>
            <span class="links_name">Trang Chủ</span>
          </a>
        </router-link>
      </li>
      <li v-if="isLoggedIn == true">
        <router-link to="/recharge">
          <a href="#">
            <i class="bx bx-coin-stack"></i>
            <span class="links_name">Nạp Tiền</span>
          </a>
        </router-link>
      </li>
      <li v-if="isLoggedIn == true">
        <router-link to="/user/history">
          <a href="#">
            <i class="bx bx-history"></i>
            <span class="links_name">Lịch Sử Mua Hàng</span>
          </a>
        </router-link>
      </li>
      <li v-if="isLoggedIn == true">
        <router-link to="/user/history-transaction/">
          <a href="#">
            <i class="bx bx-bar-chart-alt-2"></i>
            <span class="links_name">Lịch Sử Giao Dịch</span>
          </a>
        </router-link>
      </li>
      <li>
        <router-link to="/account/checklive">
          <a href="#">
            <i class="fas fa-user-check"></i>
            <span class="links_name">Kiểm Tra Live/Die</span>
          </a>
        </router-link>
      </li>
      <li v-if="isLoggedIn == true">
        <router-link to="/user/change-password">
          <a href="#">
            <i class="fas fa-user-cog"></i> 
            <span class="links_name">Đổi Mật Khẩu</span>
          </a>
        </router-link>
      </li>
      <li v-if="isLoggedIn == true && isAdmin== true">
        <router-link to="/admin">
          <a href="#">
            <i class="bx bx-desktop"></i>
            <span class="links_name">Admin Site</span>
          </a>
        </router-link>
      </li>
      <li class="log_in" v-if="isLoggedIn == false">
        <router-link to="/login">
        <a href="#" >
          <i class="bx bx-log-out"></i>
          <span class="links_name">Đăng Nhập</span>
        </a>
        </router-link>
      </li>
      
       <li class="log_out" v-if="isLoggedIn == true">
          <a href="#" v-on:click="handleLogout" >
            <i class="bx bx-log-out"></i>
        </a>
        <div class="profile-user" >
         
          <span>ID : {{ id }}</span>
          <span>Coin : {{ formatPrice(coins) }} coin</span>
        </div>
       </li>
    </ul>
  </div>
</template>

<script>
import { mapState, mapActions,mapGetters } from "vuex";


export default {
  name: "SliderBar",
  data() {
    return {
      coins: null,
      id: null,
    };
  },
  mounted() {
    if (this.isLoggedIn != false) {
      this.getProfile();
    }
  },
  computed: { 
    ...mapState(["isLoggedIn","user","isAdmin"]),
  },
  methods: {
    ...mapActions(["logout"]),
    handleLogout(event) {
      event.preventDefault();
      this.logout();
      this.$router.push("/login");
    },
    getProfile() {
      if (this.user !== null){
        this.coins = this.user.coin;
        this.id = this.user.id;
      }
    },
    formatPrice(value) {
      let val = (value / 1).toFixed(0).replace(".", ",");
      return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    },
    
  },
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
</style>
