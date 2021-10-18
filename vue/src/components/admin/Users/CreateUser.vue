<template>
  <div>
    <SideBarAdmin></SideBarAdmin>
    <section class="home-section">
      <NavbarAdmin></NavbarAdmin>

      <div class="home-content">
        <div class="header">
          <h1>Create User</h1>
          <div class="breadcrumb">
            <li class="breadcrumb-item">Trang chủ</li>
            <li class="breadcrumb-item">User</li>
            <li class="breadcrumb-item">Create User</li>
          </div>
        </div>
        <form class="form-add">
          <h1>Create User</h1>
          <div class="form-group">
            <label>Email</label>
            <input
              type="email"
              v-model="email"
              class="form-control"
              placeholder="Email"
              required
            />
          </div>
          <div class="form-group">
            <label>Password</label>
            <input
              type="password"
              v-model="password"
              class="form-control"
              placeholder="Password"
              required
              pattern="[0-9a-zA-Z_.-@#]*"
              oninput="this.setCustomValidity('')"
              oninvalid="this.setCustomValidity('Vui lòng nhập không nhập ký tự đặc biệt')"
            />
          </div>
          <div class="form-group">
            <label>Confirm Password</label>
            <input
              type="password"
              v-model="confirm_password"
              class="form-control"
              placeholder="Confirm Password"
              required
              pattern="[0-9a-zA-Z_.-@#]*"
              oninput="this.setCustomValidity('')"
              oninvalid="this.setCustomValidity('Vui lòng nhập không nhập ký tự đặc biệt')"
            />
          </div>
          <button type="button" class="btn btn-primary" @click="add()">
            Create User
          </button>
        </form>
      </div>
    </section>
    <FooterAdmin></FooterAdmin>
  </div>
</template>

<script>
import FooterAdmin from "../FooterAdmin.vue";
import NavbarAdmin from "../NavbarAdmin.vue";
import SideBarAdmin from "../SideBarAdmin.vue";
import { addUser } from "../../../services/api/admin.js";
import { createToast } from "mosha-vue-toastify";
import "mosha-vue-toastify/dist/style.css";

export default {
  data() {
    return {
      email: null,
      password: null,
      confirm_password: null,
      errors: [],
    };
  },
  components: {
    FooterAdmin,
    NavbarAdmin,
    SideBarAdmin,
  },
  mounted() {
    document.title = "Add Category | Admin Page";
  },
  methods: {
    async add() {
      this.errors = [];
      this.$store.commit("setIsLoading", true);
      if (this.password == null) {
        this.errors.push("Vui lòng nhập mật khẩu");
      } else if (this.password == "") {
        this.errors.push("Vui lòng nhập mật khẩu");
      } else if (this.password.length < 8) {
        this.errors.push("Vui lòng nhập mật khẩu trên 8 ký tự");
      } else if (this.password !== this.confirm_password) {
        this.errors.push("Mật khẩu không trùng nhau.Vui lòng nhập lại");
      }

      if (this.email == null || this.email == "") {
        this.errors.push("Vui lòng nhập email");
      } else if (!this.ValidateEmail(this.email)) {
        this.errors.push("Vui lòng nhập email đúng định dạng");
      }
      if (!this.errors.length) {
        await addUser(this.email, this.password)
          .then((response) => {
            createToast(
              {
                title: "Thành Công",
                description: response,
              },
              {
                position: "top-right",
                showCloseButton: false,
                swipeClose: true,
                hideProgressBar: true,
                showIcon: true,
                type: "success",
              }
            );
            this.$router.push("/admin/users");
          })
          .catch((error) => {
            createToast(
              {
                title: "Thất Bại",
                description: "Thêm Tài Khoản Thất Bại",
              },
              {
                position: "top-right",
                showCloseButton: false,
                swipeClose: true,
                hideProgressBar: true,
                showIcon: true,
                type: "danger",
              }
            );
          });
      }
      for (var i = 0; i < this.errors.length; i++) {
        createToast(
          {
            title: "Lỗi",
            description: this.errors[i],
          },
          {
            position: "top-right",
            showCloseButton: true,
            swipeClose: true,
            hideProgressBar: true,
            showIcon: true,
            type: "danger",
          }
        );
      }
      this.$store.commit("setIsLoading", false);
    },
    ValidateEmail(inputText) {
      var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
      if (inputText.match(mailformat)) {
        return true;
      } else {
        return false;
      }
    },
  },
};
</script>
<style scoped>
.btn-primary {
  background-color: #0a2558;
  margin: 10px;
}
.form-add {
  margin: 0px 5% 0px 5%;
  width: 90%;
  /* border: 2px solid #0a2558; */
  /* border-radius: 25px; */
  display: flex;
  flex-direction: column;
}
.form-add h1 {
  text-align: center;
}
.form-add button {
  align-self: center;
}
.form-group {
  margin-top: 10px;
  padding: 10px;
}
</style>
