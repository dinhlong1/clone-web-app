<template>
  <div>
    <SideBar></SideBar>
    <section class="home-section">
      <Navbar></Navbar>
      <div class="home-content">
        <div class="header">
          <h1>Trang chủ</h1>
          <div class="breadcrumb">
            <li class="breadcrumb-item">Trang chủ</li>
          </div>
        </div>
        <div class="table-responsive">
          <table>
            <caption>
              Danh Sách Sản Phẩm
            </caption>
            <thead>
              <tr>
                <th class="category" scope="col">Loại Tài Khoản</th>
                <th class="custom" scope="col">Đơn Giá</th>
                <th class="custom" scope="col">Còn Lại</th>
                <th class="custom" scope="col">Số Lượng</th>
                <th class="btn-buy" scope="col"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="category in categoryList" :key="category.name">
                <td data-label="Category">
                  {{ category.name }}
                </td>
                <td class="custom" data-label="Due Date">
                  {{ category.price }}
                </td>
                <td class="custom" data-label="Amount">
                  {{ category.get_quantity }}
                </td>
                <td class="custom" data-label="Period">
                  <input
                    type="number"
                    :id="category.id"
                    min="1"
                    :max="category.get_quantity"
                    value="1"
                    :disabled="category.get_quantity == 0 ? true : false"
                  />
                </td>
                <th class="btn-buy" scope="col">
                  <button
                    class="btn-disable"
                    v-show="category.get_quantity == 0"
                    disabled
                  >
                    Mua hàng
                  </button>

                  <template v-if="isLoggedIn != false">
                    <button
                      v-if="category.get_quantity > 0"
                      :disabled="disableButton"
                      @click="buyAccount(category.id)"
                    >
                      {{ disableButton ? "Đang mua" : "Mua hàng" }}
                    </button>
                  </template>
                  <template v-else>
                    <a href="/login">
                      <button v-if="category.get_quantity > 0">
                        Mua hàng
                      </button>
                    </a>
                  </template>
                </th>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>
    <Footer></Footer>
  </div>
</template>

<script>
import { createToast } from "mosha-vue-toastify";
import "mosha-vue-toastify/dist/style.css";
import { store } from "../../services/api/store";
import { myUser } from "../../services/api/user";
import { payment } from "../../services/api/payment";
import { mapState, mapActions } from "vuex";

export default {
  name: "Home",
  data() {
    return {
      categoryList: [],
      quantity: 0,
      coins: null,
      id: null,
      email: null,
      isLoading: false,
      errors: [],
      disableButton: false,
    };
  },
  mounted() {
    this.getCategory();
    if (this.isLoggedIn != false) {
      this.getProfile();
    }
    document.title = "Home";
  },
  computed: {
    ...mapState(["isLoggedIn", "user"]),
  },
  methods: {
    ...mapActions(["resetUser"]),
    getProfile() {
      if (this.user != null) {
        this.coins = this.user.coin;
        this.id = this.user.id;
        this.email = this.user.email;
      }
    },
    async buyAccount(index) {
      this.disableButton = true;
      this.errors = [];
      this.successs = [];
      this.quantity = parseInt(document.getElementById(index).value);
      if (this.quantity < 0 || this.quantity == null) {
        this.errors.push("Vui lòng nhập lại giá trị hợp lệ");
      }
      if (this.coins == 0) {
        this.errors.push("Không đủ tiền để mua hàng");
      }
      for (var i = 0; i < this.categoryList.length; i++) {
        if (this.categoryList[i].id == index) {
          if (this.quantity > this.categoryList[i].get_quantity) {
            this.errors.push(
              "Số lượng nhập vào đang nhiều hơn số lượng hiện có"
            );
          }
        }
      }
      if (this.errors.length == 0) {
        await this.paymentOrder(index, this.id, this.quantity);
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
      this.disableButton = false;
    },
    async paymentOrder(category, user, quantity) {
      await payment(category, user, quantity)
        .then((response) => {
          for (var i = 0; i < this.categoryList.length; i++) {
            if (this.categoryList[i].id == category) {
              this.categoryList[i].get_quantity -= quantity;
            }
            createToast(
              {
                title: "Thành công",
                description: "Mua hàng thành công",
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
            this.resetUser();
            this.$router.push("/user/history/");
          }
        })
        .catch((error) => {
          setTimeout(() => {
            this.errors.push("Có lỗi vui lòng thử lại");
            console.log(error);
          }, 3000);
        });

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
    async getCategory() {
      this.$store.commit("setIsLoading", true);
      await store()
        .then((data) => {
          this.categoryList = data;
        })
        .catch((error) => {
          console.log(error);
          this.$router.push("/");
        });
      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>
<style scoped>
.col-1 {
  width: 50%;
}
.col-2 {
  width: 10%;
}
.col-3 {
  width: 20;
}
</style>
