<template>
  <div>
    <SideBarAdmin></SideBarAdmin>
    <section class="home-section">
      <NavbarAdmin></NavbarAdmin>

      <div class="home-content">
        <div class="header">
          <h1>Account Detail</h1>
          <div class="breadcrumb">
            <li class="breadcrumb-item">Trang chủ</li>
            <li class="breadcrumb-item">Account</li>
            <li class="breadcrumb-item">Detail</li>
          </div>
        </div>
        <form class="form-add">
          <h1>Account Detail</h1>
          <div class="form-group">
            <label for="">Uid</label>
            <input type="text" v-model="uid" class="form-control" disabled />
          </div>
          <div class="form-group">
            <label for="">Password</label>
            <input type="text" v-model="password" class="form-control" />
          </div>
          <div class="form-group">
            <label for="">Auth</label>
            <input type="text" v-model="auth" class="form-control" />
          </div>
          <div class="form-group">
            <label for="">Email</label>
            <input type="email" v-model="email" class="form-control" />
          </div>
          <div class="form-group">
            <label for="">Email Password</label>
            <input type="email" v-model="password_email" class="form-control" />
          </div>
          <div class="form-group">
            <label for="">Cookie</label>
            <input type="text" v-model="cookie" class="form-control" />
          </div>
          <div class="form-group">
            <label for="">Token</label>
            <input type="text" v-model="token" class="form-control" />
          </div>
          <div class="form-check form-switch">
            <label class="form-check-label">Live</label>
            <input class="form-check-input" v-model="status" type="checkbox" />
          </div>
          <div class="form-check form-switch">
            <label class="form-check-label">Sold</label>
            <input class="form-check-input" type="checkbox" v-model="sold" />
          </div>
          <div class="form-group">
            <router-link to="/admin/accounts">
              <button type="button" class="btn btn-info">
                Back
              </button>
            </router-link>

            <button
              type="button"
              class="btn btn-primary"
              data-bs-toggle="modal"
              data-bs-target="#staticBackdrop"
            >
              Save
            </button>
          </div>
        </form>
        <div
          class="modal fade"
          id="staticBackdrop"
          data-bs-backdrop="static"
          data-bs-keyboard="false"
          tabindex="-1"
          aria-labelledby="staticBackdropLabel"
          aria-hidden="true"
        >
          <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="staticBackdropLabel">
                  Change Account
                </h5>
                <button
                  type="button"
                  class="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>
              <div class="modal-body">
                Would you like to change Account information?
              </div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  data-bs-dismiss="modal"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  class="btn btn-success"
                  @click="changeAccountDetail()"
                >
                  OK
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <FooterAdmin></FooterAdmin>
  </div>
</template>

<script>
import FooterAdmin from "../FooterAdmin.vue";
import NavbarAdmin from "../NavbarAdmin.vue";
import SideBarAdmin from "../SideBarAdmin.vue";
import { changeAccount, changePage } from "../../../services/api/admin.js";
import { createToast } from "mosha-vue-toastify";
import "mosha-vue-toastify/dist/style.css";

export default {
  data() {
    return {
      uid: "",
      password: "",
      auth: "",
      email: "",
      password_email: "",
      token: "",
      cookie: "",
      status: "",
      sold: "",
      errors: [],
    };
  },
  components: {
    FooterAdmin,
    NavbarAdmin,
    SideBarAdmin,
  },
  mounted() {
    this.getDetail();
    document.title = "Account Detail | Admin Page";
  },
  methods: {
    goBack() {
      this.$router.back();
    },
    async changeAccountDetail() {
      this.errors = [];
      this.$store.commit("setIsLoading", true);
      if (this.password.trim.length < 8) {
        this.errors.push = "Vui lòng điền lại mật khẩu hợp lệ";
      }
      if (this.status == true) {
        this.status = 1;
      } else {
        this.status = 0;
      }
      if (this.sold == true) {
        this.sold = 1;
      } else {
        this.sold = 0;
      }
      if (!this.errors.length) {
        await changeAccount(
          this.$route.params.id_slug,
          this.password,
          this.auth,
          this.email,
          this.password_email,
          this.token,
          this.cookie,
          this.status,
          this.sold
        )
          .then((response) => {
            createToast(
              {
                title: "Thành công",
                description: response,
              },
              {
                position: "top-right",
                showCloseButton: true,
                swipeClose: true,
                hideProgressBar: true,
                showIcon: true,
                type: "success",
              }
            );
            this.$router.go(this.$router.currentRoute);
          })
          .catch((error) => {
            createToast(
              {
                title: "Thất Bại",
                description: "Sửa đổi thông tin Account thất bại",
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
      this.$store.commit("setIsLoading", false);
    },
    getDetail() {
      this.$store.commit("setIsLoading", true);
      const url = `/api/v1/account/id=${this.$route.params.id_slug}`;
      changePage(url)
        .then((response) => {
          this.uid = response[0].uid;
          this.password = response[0].password;
          this.auth = response[0].auth;
          this.email = response[0].email;
          this.password_email = response[0].password_email;
          this.token = response[0].token;
          this.cookie = response[0].cookie;
          this.status = response[0].status;
          this.sold = response[0].sold;
        })
        .catch((error) => {
          console.log(error);
        });
      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>
<style scoped>
.btn-primary {
  background-color: #0a2558;
  margin: 5px;
}

</style>
