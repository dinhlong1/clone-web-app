<template>
  <div>
    <SideBarAdmin></SideBarAdmin>
    <section class="home-section">
      <NavbarAdmin></NavbarAdmin>

      <div class="home-content">
        <div class="header">
          <h1>Category Detail</h1>
          <div class="breadcrumb">
            <li class="breadcrumb-item">Trang chủ</li>
            <li class="breadcrumb-item">Category</li>
            <li class="breadcrumb-item">Detail</li>
          </div>
        </div>
        <form class="form-add">
          <h1>Category Detail</h1>
          <div class="form-group">
            <label for="">Id</label>
            <input type="text" v-model="id" class="form-control" disabled />
          </div>
          <div class="form-group">
            <label for="">Name</label>
            <input type="text" v-model="name" class="form-control" />
          </div>
          <div class="form-group">
            <label for="">Price</label>
            <input type="number" v-model="price" min="0" class="form-control" />
          </div>
          <div class="form-group">
            <label for="">Discount</label>
            <input
              type="number"
              v-model="discount"
              min="0"
              max="100"
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label for="">Quantity</label>
            <input
              type="int"
              v-model="quantity"
              class="form-control"
              disabled
            />
          </div>
          <div class="form-group">
            <router-link to="/admin/categories">
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
                  Change Category
                </h5>
                <button
                  type="button"
                  class="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>
              <div class="modal-body">
                Would you like to change Category information?
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
                  data-bs-dismiss="modal"
                  @click="changeCategoryDetail()"
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
import { changeCategory, changePage } from "../../../services/api/admin.js";
import { createToast } from "mosha-vue-toastify";

export default {
  data() {
    return {
      id: "",
      name: "",
      price: "",
      discount: "",
      quantity: "",
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
    async changeCategoryDetail() {
      this.$store.commit("setIsLoading", true);
      if (this.name.trim() == "") {
        this.errors.push("Vui Lòng Nhập Tên Cho Category");
      }
      if (this.price <= 0) {
        this.errors.push("Vui lòng nhập lại giá tiền hợp lệ");
      }
      if (this.discount < 0 || this.discount >= 100) {
        this.errors.push("Vui lòng nhập tỉ lệ giảm giá hợp lệ");
      }
      if (!this.errors.length) {
        await changeCategory(
          this.$route.params.id_slug,
          this.name,
          this.price,
          this.discount
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
                description: "Sửa đổi thông tin thất bại",
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
    async getDetail() {
      this.$store.commit("setIsLoading", true);
      const url = `/api/v1/category/id=${this.$route.params.id_slug}`;
      await changePage(url)
        .then((response) => {
          this.id = response[0].id;
          this.name = response[0].name;
          this.price = response[0].price;
          this.discount = response[0].discount;
          this.quantity = response[0].get_quantity;
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
