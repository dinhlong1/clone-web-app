<template>
  <div class="body">
      <div class="container">
    <input type="checkbox" id="flip" />
    <div class="cover">
      <div class="front">
        <img
          src="http://joombig.com/v/tem/images/tech_1/image959350.jpg"
          alt=""
        />
        <div class="text">
          <span class="text-1"
            >Hãy đăng nhập để trải nghiệm các tính năng của chúng tôi</span
          >
          <span class="text-2">Bắt đầu thôi nào</span>
        </div>
      </div>
      <div class="back">
        <img
          class="backImg"
          src="http://joombig.com/v/tem/images/tech_1/image875336.jpg"
          alt=""
        />
        <div class="text">
          <span class="text-1"
            >Nếu chưa có tài khoản vui lòng tạo tài khoản để trải nghiệm</span
          >
          <span class="text-2">
            Tạo tài khoản ở mục bên
          </span>
        </div>
      </div>
    </div>
    <div class="forms">
      <div class="form-content">
        <div class="login-form">
          <div class="title">Login</div>
          <form action="#" v-on:submit.prevent="handleLogin">
            <div class="input-boxes">
              <div class="input-box">
                <i class="bx bx-user"></i>
                <input
                  type="email"
                  v-model="email"
                  placeholder="Enter your email"
                  required
                />
              </div>
              <div class="input-box">
                <i class="bx bx-lock-alt"></i>
                <input
                  type="password"
                  v-model="password"
                  placeholder="Enter your password"
                  required
                  pattern="[0-9a-zA-Z_.-@#]*"
                  oninput="this.setCustomValidity('')"
                  oninvalid="this.setCustomValidity('Vui lòng không nhập ký tự đặc biệt')"
                />
              </div>
              <vue-recaptcha
                class="captcha"
                v-if="showRecaptcha"
               siteKey="6Ldl-swbAAAAAByMTR5yFlyzQgv6pDDXZXku9e67"
                size="normal"
                theme="light"
                :tabindex="0"
                @verify="recaptchaVerified"
                @expire="recaptchaExpired"
                @fail="recaptchaFailed"
                ref="vueRecaptcha"
              >
              </vue-recaptcha>
              <div class="text"><a href="#">Forgot password?</a></div>
              <div class="button input-box">
                <input type="submit" value="Đăng Nhập" />
              </div>
              <div class="text sign-up-text">
                Don't have an account?
                <label for="flip" @click="isLogging()">Sigup now</label>
              </div>
            </div>
          </form>
        </div>
        <div class="signup-form">
          <div class="title">Signup</div>
          <form action="#" @submit.prevent="submitForm">
            <div class="input-boxes">
              <div class="input-box">
                <i class="bx bx-user"></i>
                <input
                  type="email"
                  v-model="email"
                  placeholder="Enter your email"
                  required
                />
              </div>
              <div class="input-box">
                <i class="bx bx-lock-alt"></i>
                <input
                  type="password"
                  v-model="password"
                  placeholder="Enter your password"
                  required
                  pattern="[0-9a-zA-Z_.-@#]*"
                  oninput="this.setCustomValidity('')"
                  oninvalid="this.setCustomValidity('Vui lòng không nhập ký tự đặc biệt')"
                />
              </div>
              <div class="input-box">
                <i class="bx bx-lock-alt"></i>
                <input
                  type="password"
                  v-model="confirm_password"
                  placeholder="Enter your confirm password"
                  required
                  pattern="[0-9a-zA-Z_.-@#]*"
                  oninput="this.setCustomValidity('')"
                  oninvalid="this.setCustomValidity('Vui lòng nhập không nhập ký tự đặc biệt')"
                />
              </div>
              <vue-recaptcha
                class="captcha"
                v-if="!showRecaptcha"
                siteKey="6Ldl-swbAAAAAByMTR5yFlyzQgv6pDDXZXku9e67"
                size="normal"
                theme="light"
                :tabindex="0"
                @verify="recaptchaVerified"
                @expire="recaptchaExpired"
                @fail="recaptchaFailed"
                ref="vueRecaptcha"
              >
              </vue-recaptcha>
              <div class="button input-box">
                <input type="submit" value="Tạo Tài Khoản" />
              </div>
              <div class="text sign-up-text">
                Already have an account?
                <label for="flip" @click="isLogging()">Login now</label>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
  </div>
  

</template>
<script>
import { createUser } from "../services/api/auth";
import { mapActions, mapState } from "vuex";
import { defineComponent } from "vue";
import { createToast } from "mosha-vue-toastify";
import "mosha-vue-toastify/dist/style.css";
import vueRecaptcha from "vue3-recaptcha2";

export default {
  name: "Login",
  data() {
    return {
      showRecaptcha: true,
      email: null,
      password: null,
      confirm_password: null,
      nextPath: "/",
      errors: [],
      disableButton: false,
      captcha: false,
    };
  },
  components: {
    vueRecaptcha,
    sn: vueRecaptcha,
  },
  computed: {
    ...mapState(["isLoggedIn"]),
  },
  mounted() {
    document.title = "Login";
    this.updateAfterLoginNextPath();
    if (this.isLoggedIn) {
      this.$router.push("/");
    }
  },
  methods: {
    isLogging() {
      this.showRecaptcha = !this.showRecaptcha;
      this.email = null;
      this.password = null;
      this.confirm_password = null;
      this.$refs.vueRecaptcha.reset();
    },
    recaptchaVerified(response) {
      this.captcha = true;
    },
    recaptchaExpired() {
      this.$refs.vueRecaptcha.reset();
    },
    recaptchaFailed() {
      this.captcha = false;
    },
    async submitForm() {
      this.errors = [];
      this.$store.commit("setIsLoading", true);
      if (this.password === "") {
        this.errors.push("Vui lòng nhập mật khẩu");
      }

      if (this.captcha == false) {
        this.errors.push("Vui lòng xác nhận Captcha");
      }

      if (this.password !== this.confirm_password) {
        this.errors.push("Mật khẩu không trùng nhau vui lòng nhập lại");
      }
      if (this.password.length < 8) {
        this.errors.push("Mật khẩu phải trên 8 ký tự");
      }
      if (this.password == "12345678") {
        this.errors.push("Mật khẩu quá chung chung");
      }
      if (
        this.email.toLowerCase().indexOf(this.password.toLowerCase()) == true
      ) {
        this.errors.push("Mật khẩu không được giống với tài khoản");
      }
      if (!this.errors.length) {
        await createUser(this.email, this.password)
          .then((response) => {
            createToast(
              {
                title: "Thành công",
                description: "Bạn đã đăng ký tài khoản thành công. Vui lòng đăng nhập",
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
            window.reload();
          })
          .catch((error) => {
            if (error.response) {
              for (const property in error.response.data) {
                if (error.response.data[property] == "email is not defined") {
                  this.errors.push("Email đã tồn tại. Vui lòng nhập lại.");
                }
                if (
                  error.response.data[property] == "password is not defined"
                ) {
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
                 if (
                  error.response.data[property] ==
                  "The password is too similar to the email address."
                ) {
                  this.errors.push(
                    "Mật khẩu với email quá giống nhau"
                  );
                }
                
              }

              this.password = "";
              this.confirm_password = "";
              console.log(JSON.stringify(error.response.data));
            } else if (error.message) {
              this.errors.push("Có lỗi vui lòng thử lại");

              console.log(JSON.stringify(error));
              this.password = "";
              this.confirm_password = "";
            }
          });
      }
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
       this.$store.commit("setIsLoading",false);
    },
    async handleLogin(event ) {
       this.$store.commit("setIsLoading", true);
      this.disableButton = true;
      this.errors = [];
      if (this.password === "") {
        this.errors.push("Vui lòng nhập mật khẩu");
      }
      if (this.captcha == false) {
        this.errors.push("Vui lòng xác nhận Captcha");
      }

      if (this.email == "") {
        this.errors.push("Vui lòng nhập email");
      }
      if (this.password.length < 8 && this.password != "") {
        this.errors.push("Vui lòng nhập lại mật khẩu hợp lệ");
      }
      if (this.errors.length == 0) {
        this.$store.commit("setIsLoading", true);
        event.preventDefault();
        await this.login({ email: this.email, password: this.password })

          .then(() => {
            this.$router.push(this.nextPath);
            createToast(
              {
                title: "Thành công",
                description: "Đăng nhập thành công",
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
          })
          .catch((error) => {
            createToast(
              {
                title: "Lỗi",
                description: "Tài khoản hoặc mật khẩu không chính xác",
              },
              {
                position: "top-right",
                showCloseButton:false,
                swipeClose: true,
                hideProgressBar: false,
                showIcon: true,
                type: "danger",
              }
            );
            console.log(JSON.stringify(error.response.data));
            this.password = "";
          });
           this.$store.commit("setIsLoading", false);
      }
      this.$refs.vueRecaptcha.reset();
      this.disableButton = false;
      this.$store.commit("setIsLoading", false);
      if (this.errors.length != 0) {
        for (var i = 0; i < this.errors.length; i++) {
          createToast(
            {
              title: "Lỗi",
              description: this.errors[i],
            },
            {
              position: "top-right",
              showCloseButton: "false",
              swipeClose: "true",
              hideProgressBar: "false",
              showIcon: "true",
              type: "danger",
            }
          );
        }
      }
    },
    updateAfterLoginNextPath() {
      if ("next" in this.$route.query) {
        this.nextPath = this.$route.query.next;
      }
    },
    ...mapActions(["login"]),
  },
};
</script>
<style scoped>
/* Google Font Link */
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600;700&display=swap");
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Poppins", sans-serif;
}
.body {
  height: 100vh;
  width:100%;
  display: flex;
  align-items: center;
  justify-items: center;
}
.container {
  position: relative;
  max-width: 850px;
  width: 100%;
  background: #fff;
  padding: 40px 30px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
  perspective: 2700px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.container .cover {
  position: absolute;
  top: 0;
  left: 50%;
  height: 100%;
  width: 50%;
  z-index: 98;
  transition: all 1s ease;
  transform-origin: left;
  transform-style: preserve-3d;
}
.container .cover::before {
  content: "";
  position: absolute;
  height: 100%;
  width: 100%;
  background: #0072b5;
  opacity: 0.5;
  z-index: 100;
}
.container .cover::after {
  content: "";
  position: absolute;
  height: 100%;
  width: 100%;
  background: #0072b5;
  opacity: 0.5;
  z-index: 100;
  transform: rotateY(180deg);
}
.container #flip:checked ~ .cover {
  transform: rotateY(-180deg);
}
.container .cover img {
  position: absolute;
  height: 100%;
  width: 100%;
  object-fit: cover;
  z-index: 12;
  backface-visibility: hidden;
}
.container .cover .back .backImg {
  transform: rotateY(180deg);
  transform: rotateY(180deg);
}
.container .cover .text {
  position: absolute;
  z-index: 111;
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.cover .text .text-1,
.cover .text .text-2 {
  font-size: 26px;
  font-weight: 600;
  color: #fff;
  text-align: center;
  backface-visibility: hidden;
}
.cover .back .text .text-1,
.cover .back .text .text-2 {
  transform: rotateY(180deg);
}
.cover .text .text-2 {
  font-size: 15px;
  font-weight: 500;
}
.container .forms {
  height: 100%;
  width: 100%;
  background: #fff;
}
.container .form-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.form-content .login-form,
.form-content .signup-form {
  width: calc(100% / 2 - 25px);
}
.forms .form-content .title {
  position: relative;
  font-size: 24px;
  font-weight: 500;
  color: #333;
}
.forms .form-content .title:before {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  height: 3px;
  width: 25px;
  background: #0072b5;
}
.forms .signup-form .title:before {
  width: 20px;
}
/* .forms .form-content .input-boxes {
  margin-top: 30px;
} */
.forms .form-content .input-box {
  display: flex;
  align-items: center;
  height: 50px;
  width: 100%;
  margin: 10px 0;
  position: relative;
}
.form-content .input-box input {
  height: 100%;
  width: 100%;
  outline: none;
  border: none;
  padding: 0 30px;
  font-size: 16px;
  font-weight: 500;
  border-bottom: 2px solid rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}
.form-content .input-box input:focus,
.form-content .input-box input:valid {
  border-color: #0072b5;
}
.form-content .input-box i {
  position: absolute;
  color: #0072b5;
  font-size: 17px;
}
.forms .form-content .text {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}
.forms .form-content .text a {
  text-decoration: none;
}
.forms .form-content .text a:hover {
  text-decoration: underline;
}
.forms .form-content .button {
  color: #fff;
  margin-top: 40px;
}
.forms .form-content .button input {
  color: #fff;
  background: #0072b5;
  border-radius: 6px;
  padding: 0;
  cursor: pointer;
  transition: all 0.4s ease;
}
.forms .form-content .button input:hover {
  background: #0072b5;
}
.forms .form-content label {
  color: #0072b5;
  cursor: pointer;
}
.forms .form-content label:hover {
  text-decoration: underline;
}
.forms .form-content .login-text,
.forms .form-content .sign-up-text {
  text-align: center;
  margin-top: 25px;
}
.container #flip {
  display: none;
}
@media (max-width: 730px) {
  .container .cover {
    display: none;
  }
  .form-content .login-form,
  .form-content .signup-form {
    width: 100%;
  }
  .form-content .signup-form {
    display: none;
  }
  .container #flip:checked ~ .forms .signup-form {
    display: block;
  }
  .container #flip:checked ~ .forms .login-form {
    display: none;
  }
  .captcha {
    align-items: center;
    width: 100%;
  }
}
</style>
