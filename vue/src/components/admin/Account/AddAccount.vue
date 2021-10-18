<template>
  <div>
    <SideBarAdmin></SideBarAdmin>
    <section class="home-section">
      <NavbarAdmin></NavbarAdmin>

      <div class="home-content">
        <div class="header">
          <h1>Add Account</h1>
          <div class="breadcrumb">
            <li class="breadcrumb-item">Trang chủ</li>
            <li class="breadcrumb-item">Account</li>
            <li class="breadcrumb-item">Add Account</li>
          </div>
        </div>
        <form class="form-add">
          <h1>Add Account</h1>
          <div class="form-group">
            <label class="col-md-4 control-label" style="text-align: left;"
              >Choose Category</label
            >
            <div class="col-md-12">
              <VueformMultiselect
                v-model="categorySelect"
                :options="categoryOption"
                :searchable="true"
              ></VueformMultiselect>
              <div class="output">Data: {{ categorySelect }}</div>
            </div>
          </div>
          <div class="form-group">
            <label class="col-md-4 control-label" style="text-align: left;"
              >Choose type to import Account</label
            >
            <div class="col-md-12">
              <VueformMultiselect
                v-model="accountValue"
                :options="accountOptions"
                mode="tags"
                :searchable="true"
                :createTag="true"
              ></VueformMultiselect>
              <div>Data: {{ accountValue }}</div>
            </div>
          </div>
          <div class="form-group">
            <label class="col-md-4 control-label" style="text-align: left;"
              >Input Data</label
            >
            <textarea
              class="form-control"
              style="min-height:200px"
              v-model="dataInput"
            ></textarea>
          </div>
          <button type="button" class="btn btn-primary" @click="addDataAccount()">
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
import { addAccount } from "../../../services/api/admin.js";
import { store } from "../../../services/api/store.js";
import { createToast } from "mosha-vue-toastify";
import VueformMultiselect from "@vueform/multiselect";
import "mosha-vue-toastify/dist/style.css";

export default {
  data() {
    return {
      accountValue: [],
      categorySelect: "",
      dataInput: "",
      accountOptions: [
        "uid",
        "password",
        "auth",
        "email",
        "password_email",
        "cookie",
        "token",
      ],
      categoryOption: [],
      errors: [],
    };
  },
  components: {
    FooterAdmin,
    NavbarAdmin,
    SideBarAdmin,
    VueformMultiselect,
  },
  mounted() {
    this.getCategory();
    document.title = "Add Account | Admin Page";
  },
  methods: {
    async getCategory() {
      this.$store.commit("setIsLoading", true);
      await store()
        .then((response) => {
          
          // Get Category Array
          for (var i = 0; i < response.length; i++) { 
            var item = {
              value: response[i].id,
              label: response[i].name,
            };
            this.categoryOption.push(item);
          }
        })
        .catch((error) => {
          createToast(
            {
              title: "Lỗi",
              description: "Không nhận được dữ liệu các Category",
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
        });
      this.$store.commit("setIsLoading", false);
    },
    async addDataAccount() {
      this.errors = [];

      if (this.dataInput == "") {
        this.errors.push("Vui lòng nhập dữ liệu Account");
      } else {
        if (this.dataInput.includes("\n")) {
          
          // Check Value in a line in textarea
          const accounts = this.dataInput.split("\n");
          for (var i = 0; i < accounts.length; i++) {
            const account = accounts[i].split("|");
            if (account.length < this.accountValue.length) {
              this.errors.push("Giá trị nhập vào không đúng định dạng đã chọn");
            }
          }
        }
      }
      if (this.categorySelect.length == 0 || this.categorySelect == "") {
        this.errors.push("Vui lòng chọn Category");
      }

      if (this.accountValue.length == 0) {
        this.errors.push("Vui lòng nhập kiểu Account");
      }
      if (
        this.accountValue.includes("uid") == false &&
        this.accountValue.length != 0
      ) {
        this.errors.push("Vui lòng thêm định dạng uid vào kiểu dữ liệu");
      }
      if (
        this.accountValue.includes("password") == false &&
        this.accountValue.length != 0
      ) {
        this.errors.push("Vui lòng thêm định dạng password vào kiểu dữ liệu");
      }

      if (!this.errors.length) {
        this.$store.commit("setIsLoading", true);
        await addAccount(this.categorySelect, this.dataInput, this.accountValue)
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
            // this.$router.push('/admin/accounts');
          })
          .catch((error) => {
            createToast(
              {
                title: "Lỗi",
                description: error,
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
            hideProgressBar: false,
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
<style src="@vueform/multiselect/themes/default.css"></style>

<style scoped>
.btn-primary {
  background-color: #0a2558;
  margin: 10px;
}
.form-add {
  margin: 0px 5% 0px 5%;
  width: 90%;
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
