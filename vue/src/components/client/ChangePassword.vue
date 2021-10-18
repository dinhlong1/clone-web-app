<template>
  <div>
    <SideBar></SideBar>
    <section class="home-section">
        <Navbar></Navbar>
      <div class="home-content">
        <div class="header">
          <h1>Đổi mật khẩu</h1>
          <div class="breadcrumb">
            <li class="breadcrumb-item">Trang chủ</li>
            <li class="breadcrumb-item">Tài Khoản</li>
            <li class="breadcrumb-item">Đổi mật khẩu</li>
          </div>
        </div>
        <div class="mainDiv">
          <div class="cardStyle">
            <form class="forms-sample" @submit.prevent="submitForm">
              <img src="" />

              <h2 class="formTitle">
                Đổi mật khẩu
              </h2>
              <div class="inputDiv">
                <label class="inputLabel">Mật khẩu cũ</label>
                <input
                  type="password"
                  id="currentPassword"
                  v-model="currentPassword"
                  required
                  pattern="[0-9a-zA-Z_.-@#]*"
                />
              </div>
              <div class="inputDiv">
                <label class="inputLabel">Mật khẩu mới</label>
                <input
                  type="password"
                  id="password"
                  v-model="password"
                  required
                  pattern="[0-9a-zA-Z_.-@#]*"
                />
              </div>

              <div class="inputDiv">
                <label class="inputLabel">Xác nhận mật Khẩu</label>
                <input
                  type="password"
                  id="confirmPassword"
                  pattern="[0-9a-zA-Z_.-@#]*"
                />
              </div>

              <div class="buttonWrapper">
                <button
                  type="submit"
                  id="submitButton"
                  class="submitButton pure-button pure-button-primary"
                >
                  <span>Thay đổi</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </section>
    <Footer></Footer>
  </div>
</template>
<script>
import SideBar from "./SideBar.vue";
import Footer from "./Footer.vue";
import { SetPassword } from "../../services/api/user";
import { mapState } from "vuex";
import { createToast } from "mosha-vue-toastify";
import "mosha-vue-toastify/dist/style.css";

export default {
  name: "SetPassword",
  data() {
    return {
      currentPassword: "",
      password: "",
      confirmPassword: "",
      errors: [],
    };
  },
  components: {
    Footer,
    SideBar,
  },
  computed: {
    ...mapState(["isLoggedIn"]),
  },
  mounted() {
    document.title = "Đổi Mật Khẩu ";
  },
  methods: {
    submitForm() {
      this.errors = [];
      if (
        this.currentPassword == "" ||
        this.password == "" ||
        this.confirmPassword == ""
      ) {
        this.errors.push("Vui lòng nhập đầy đủ mật khẩu.");
      }
      if (this.currentPassword.length < 8 && this.currentPassword != "") {
        this.errors.push("Vui lòng nhập chính xác mật khẩu cũ");
      }
      if (this.password.length < 8 && this.password != "") {
        this.errors.push("Vui lòng nhập mật khẩu mới trên 8 ký tự");
      }
      if (this.password !== this.confirmPassword) {
        this.errors.push("Mật khẩu mới không trùng nhau vui lòng nhập lại");
      }
      if (this.errors.length == 0) {
        SetPassword(this.password, this.currentPassword)
          .then((response) => {
            createToast(
              {
                title: "Thành công",
                description: "Sửa Mật Khẩu Thành Công",
              },
              {
                position: "top-right",
                showCloseButton: false,
                swipeClose: true,
                hideProgressBar: false,
                showIcon: true,
                type: "success",
              }
            );
            this.$router.push("/");
          })
          .catch((error) => {
            for (const property in error.response.data) {
              if (error.response.data[property] == "email is not defined") {
                this.errors.push("Email đã tồn tại. Vui lòng nhập lại.");
              }
              if (error.response.data[property] == "password is not defined") {
                this.errors.push(
                  "Mật khẩu không được xác định. Vui lòng nhập lại."
                );
              }
              if (
                error.response.data[property] ==
                "user with this email address already exists."
              ) {
                this.errors.push(
                  "Email đã tồn tại. Vui lòng nhập lại email mới."
                );
              }
            }
            this.errors.push("Có lỗi vui lòng thử lại");
            this.currentPassword = "";
            this.password = "";
            this.confirmPassword = "";
            console.log(JSON.stringify(error.response.data));
          });
      }
      this.currentPassword = "";
      this.password = "";
      this.confirmPassword = "";
      if (this.errors.length != 0) {
        for (var i = 0; i < this.errors.length; i++) {
          createToast(
            {
              title: "Lỗi",
              description: this.errors[i],
            },
            {
              position: "top-right",
              showCloseButton: false,
              swipeClose: true,
              hideProgressBar: false,
              showIcon: true,
              type: "danger",
            }
          );
        }
      }
    },
  },
};
</script>
<style scoped>
.mainDiv {
  display: flex;
  min-height: 100%;
  align-items: center;
  justify-content: center;
  background-color: #f9f9f9;
  font-family: "Open Sans", sans-serif;
}
.cardStyle {
  width: 500px;
  border-color: white;
  background: #fff;
  padding: 36px 0;
  border-radius: 4px;
  margin: 30px 0;
  box-shadow: 0px 0 2px 0 rgba(0, 0, 0, 0.25);
}
#signupLogo {
  max-height: 100px;
  margin: auto;
  display: flex;
  flex-direction: column;
}
.formTitle {
  font-weight: 600;
  margin-top: 20px;
  color: #2f2d3b;
  text-align: center;
}
.inputLabel {
  font-size: 12px;
  color: #555;
  margin-bottom: 6px;
  margin-top: 24px;
}
.inputDiv {
  width: 70%;
  display: flex;
  flex-direction: column;
  margin: auto;
}
input {
  height: 40px;
  font-size: 16px;
  border-radius: 4px;
  border: none;
  border: solid 1px #ccc;
  padding: 0 11px;
}
input:disabled {
  cursor: not-allowed;
  border: solid 1px #eee;
}
.buttonWrapper {
  margin-top: 40px;
}
.submitButton {
  width: 70%;
  height: 40px;
  margin: auto;
  display: block;
  color: #fff;
  background-color: #0a2558;
  border-color: #0a2558;
  text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.12);
  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.035);
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}
.submitButton:disabled,
button[disabled] {
  border: 1px solid #cccccc;
  background-color: #cccccc;
  color: #666666;
}

#loader {
  position: absolute;
  z-index: 1;
  margin: -2px 0 0 10px;
  border: 4px solid #f3f3f3;
  border-radius: 50%;
  border-top: 4px solid #666666;
  width: 14px;
  height: 14px;
  -webkit-animation: spin 2s linear infinite;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
/* .btn-fw {
  display: flex;
  align-items: center;
  justify-self: center;
  justify-content: flex-end;
} */
</style>
