<template>
  <div>
    <SideBarAdmin></SideBarAdmin>
    <section class="home-section">
      <NavbarAdmin></NavbarAdmin>

      <div class="home-content">
        <div class="header">
          <h1>Thông Tin User</h1>
          <div class="breadcrumb">
            <li class="breadcrumb-item">Trang chủ</li>
            <li class="breadcrumb-item">User</li>
            <li class="breadcrumb-item">Thông Tin</li>
          </div>
        </div>
        <form class="form-add">
          <h1>Thông Tin User</h1>
          <div class="form-group">
            <label for="">ID</label>
            <input type="text" v-model="id" class="form-control" disabled />
          </div>
          <div class="form-group">
            <label for="">Email</label>
            <input type="email" v-model="email" class="form-control" />
          </div>
          <div class="form-group">
            <label for="">Password</label>
            <input
              type="text"
              v-model="password"
              class="form-control"
              disabled
            />
          </div>
          <div class="form-group">
            <label for="">Coin</label>
            <input type="number" v-model="coin" class="form-control" />
          </div>

          <div class="form-group">
            <router-link to="/admin/users">
              <button type="button" class="btn btn-info">
                Trở về
              </button>
            </router-link>

            <button
              type="button"
              class="btn btn-primary"
              data-bs-toggle="modal"
              data-bs-target="#staticBackdrop"
            >
              Lưu Dữ Liệu
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
                  Sửa thông tin User
                </h5>
                <button
                  type="button"
                  class="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>
              <div class="modal-body">
                Bạn có muốn sửa thông tin User này
              </div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  data-bs-dismiss="modal"
                >
                  Hủy
                </button>
                <button
                  type="button"
                  class="btn btn-success"
                  @click="changeUserDetail()"
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
import { changeUser, changePage } from "../../../services/api/admin.js";
import { createToast } from "mosha-vue-toastify";
import "mosha-vue-toastify/dist/style.css";

export default {
  data() {
    return {
      id: "",
      email: "",
      password: "",
      coin: "",
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
    async changeUserDetail() {
      this.errors = [];
      this.$store.commit("setIsLoading", true);
      if (this.coin < 0) {
        this.errors.push = "Vui lòng điền lại mật khẩu hợp lệ";
      }

      if (!this.errors.length) {
        await changeUser(this.$route.params.id_slug, this.email, this.coin)
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
                description: "Sửa đổi thông tin tài khoản thất bại",
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
      const url = `/api/v1/user/id=${this.$route.params.id_slug}`;
      changePage(url)
        .then((response) => {
          this.id = response[0].id;
          this.email = response[0].email;
          this.password = response[0].password;
          this.coin = response[0].coin;
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
.form-add {
  margin: 0px 5% 0px 5%;
  width: 90%;
  border: 2px solid #0a2558;
  border-radius: 25px;
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
.form-check {
  margin: 10px;
}
</style>
