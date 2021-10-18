<template>
  <div>
    <SideBarAdmin></SideBarAdmin>
    <section class="home-section">
      <NavbarAdmin></NavbarAdmin>

      <div class="home-content">
        <div class="header">
          <h1>Add Category</h1>
          <div class="breadcrumb">
            <li class="breadcrumb-item">Trang chủ</li>
            <li class="breadcrumb-item">Category</li>
            <li class="breadcrumb-item">Add Category</li>
          </div>
        </div>
        <form class="form-add">
          <h1>Add Category</h1>
          <div class="form-group">
            <label>Name</label>
            <input
              type="text"
              v-model="name"
              class="form-control"
              placeholder="Name"
            />
          </div>
          <div class="form-group">
            <label>Price</label>
            <input
              type="number"
              v-model="price"
              class="form-control"
              placeholder="Price"
            />
          </div>
          <div class="form-group">
            <label>Discount</label>
            <input
              type="number"
              v-model="discount"
              class="form-control"
              placeholder="Discount"
            />
          </div>
          <button type="button" class="btn btn-primary" @click="add()">
            Add Data
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
import { addCategory } from "../../../services/api/admin.js";
import { createToast } from "mosha-vue-toastify";
import "mosha-vue-toastify/dist/style.css";

export default {
  data() {
    return {
      name: "",
      price: 0,
      discount: 0,
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
        await addCategory(this.name, this.price, this.discount)
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
            this.$router.push("/admin/categories");
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
</style>
