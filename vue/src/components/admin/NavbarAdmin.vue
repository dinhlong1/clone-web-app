<template>
  <nav>
    <div class="sidebar-button">
      <i class="bx bx-menu sidebarBtn" @click="activeSidebar()"></i>
    </div>
    <!-- <div class="search-box">
      <input type="text" placeholder="Search..." />
      <i class="bx bx-search"></i>
    </div> -->
    <div class="profile-details">
      <img
        src="https://scontent.fsgn8-2.fna.fbcdn.net/v/t1.30497-1/143086968_2856368904622192_1959732218791162458_n.png?_nc_cat=1&ccb=1-5&_nc_sid=7206a8&_nc_ohc=8fru4cWA3v4AX8zmwQg&_nc_ht=scontent.fsgn8-2.fna&oh=bee9d33a8bbba06fe5451674eda94f15&oe=614AD378"
        alt=""
      />
      <span class="admin_name">
        Admin
      </span>
      <i class="bx bx-chevron-down"></i>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavbarAdmin",
  data() {
    return {};
  },
  methods: {
    activeSidebar() {
      let sidebar = document.querySelector(".sidebar");
      let sidebarBtn = document.querySelector(".sidebarBtn");
      if (sidebarBtn) {
        sidebarBtn.onclick = function() {
          sidebar.classList.toggle("active");
          if (sidebar.classList.contains("active")) {
            sidebarBtn.classList.replace("bx-menu", "bx-menu-alt-right");
          } else sidebarBtn.classList.replace("bx-menu-alt-right", "bx-menu");
          console.log("1");
        };
      }
    },
  },
};
</script>
