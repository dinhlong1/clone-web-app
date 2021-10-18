<template>
  <div>
    <SideBarAdmin></SideBarAdmin>
    <section class="home-section">
      <NavbarAdmin></NavbarAdmin>
      <div class="home-content">
        <div class="header">
          <h1>OrderDetail</h1>
          <div class="breadcrumb">
            <li class="breadcrumb-item">Trang chủ</li>
            <li class="breadcrumb-item">Account</li>
          </div>
        </div>
        <div class="table-responsive">
          <table>
            <caption>
              Account
            </caption>
            <thead class="thead-light">
              <tr>
                <th>Order ID</th>
                <th>Uid</th>
                <th>Password</th>
                <th>Auth</th>
                <th>Email</th>
                <th>Password Email</th>
                <th>Status</th>

                <th></th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in orders" :key="item">
                <td>{{ item.order.id }}</td>
                <td>{{ item.account.uid }}</td>
                <td>{{ item.account.password }}</td>
                <td>{{ item.account.auth }}</td>
                <td>{{ item.account.email }}</td>
                <td>{{ item.account.password_email }}</td>
                <td>
                  <span
                    :class="
                      item.account.status
                        ? 'badge bg-success'
                        : 'badge bg-danger'
                    "
                    >{{ item.account.status ? "Live" : "Die" }}</span
                  >
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="pagination">
          <ul></ul>
        </div>
      </div>
    </section>

    <!-- Modal -->

    <FooterAdmin></FooterAdmin>
  </div>
</template>

<script>
import FooterAdmin from "../FooterAdmin.vue";
import NavbarAdmin from "../NavbarAdmin.vue";
import SideBarAdmin from "../SideBarAdmin.vue";
import { getAccounts, changePage } from "../../../services/api/admin.js";
import "mosha-vue-toastify/dist/style.css";
import { createToast } from "mosha-vue-toastify";

export default {
  data() {
    return {
      orders: [],
      currentPage: null,
      totalPages: null,
      id: null,
    };
  },
  components: {
    FooterAdmin,
    SideBarAdmin,
    NavbarAdmin,
  },
  mounted() {
    this.getData();
    document.title = "Accounts | Admin Page";
  },
  methods: {
    async getData() {
      this.$store.commit("setIsLoading", true);
      // path: '/admin/order-detail/:id/:page',
      var url = `/api/v1/order/order-detail/?${this.$route.params.id}&${this.$route.params.page}`;
      console.log(url);
      await changePage(url)
        .then((response) => {
          this.orders = response.results;
          this.totalPages = response.total_pages;
          this.currentPage = response.current_page;
          if (this.currentPage != null && this.totalPages != null) {
            this.createPgn();
          }
        })
        .catch((error) => {
          createToast(
            {
              title: "Thất Bại",
              description: "Lỗi dữ liệu",
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
      this.$store.commit("setIsLoading", false);
    },
    createPgn() {
      this.id = this.$route.params.id;
      // selecting required element
      const element = document.querySelector(".pagination ul");
      //calling function with passing parameters and adding inside element which is ul tag
      element.innerHTML = createPagination(
        this.totalPages,
        this.currentPage,
        this.id
      );
      function createPagination(totalPage, page, id) {
        let liTag = "";
        let active;
        let beforePage = page - 1;
        let afterPage = page + 1;
        if (page > 1 && page > 2) {
          //show the next button if the page value is greater than 1
          liTag += `<a href="/admin/order-detail/${id}/page=${page -
            1}/"><li class="btn prev"><span><i class="fas fa-angle-left"></i> Prev</span></li></a>`;
        }
        if (page > 1 && page == 2) {
          //show the next button if the page value is greater than 1
          liTag += `<a href="/admin/order-detail/${id}/"><li class="btn prev"><span><i class="fas fa-angle-left"></i> Prev</span></li></a>`;
        }

        if (page > 2 && totalPage > 4) {
          //if page value is less than 2 then add 1 after the previous button
          liTag += `<a href="/admin/order-detail/${id}/"><li class="first numb"><span>1</span></li></a>`;
          if (page > 3 && totalPage > 5) {
            //if page value is greater than 3 then add this (...) after the first li or page
            liTag += `<li class="dots"><span>...</span></li>`;
          }
        }

        // how many pages or li show before the current li
        if (page == totalPage) {
          beforePage = beforePage - 2;
        } else if (page == totalPage - 1) {
          beforePage = beforePage - 1;
        }
        // how many pages or li show after the current li
        if (page == 1) {
          afterPage = afterPage + 2;
        } else if (page == 2) {
          afterPage = afterPage + 1;
        }

        for (var plength = beforePage; plength <= afterPage; plength++) {
          if (plength > totalPage) {
            //if plength is greater than totalPage length then continue
            continue;
          }
          if (plength == 0) {
            //if plength is 0 than add +1 in plength value
            plength = plength + 1;
          }
          if (page == plength) {
            //if page is equal to plength than assign active string in the active variable
            active = "active";
          } else {
            //else leave empty to the active variable
            active = "";
          }
          if (plength < 0) {
            continue;
          }
          liTag += `<a href="/admin/order-detail/${id}/page=${plength}"><li class="numb ${active}"><span>${plength}</span></li></a>`;
        }

        if (page < totalPage - 1 && totalPage > 4) {
          //if page value is less than totalPage value by -1 then show the last li or page
          if (page < totalPage - 2 && totalPage > 5) {
            //if page value is less than totalPage value by -2 then add this (...) before the last li or page
            liTag += `<li class="dots"><span>...</span></li>`;
          }
          liTag += `<a href="/admin/order-detail/${id}/page=${totalPage}"><li class="last numb" ><span>${totalPage}</span></li></a>`;
        }

        if (page < totalPage) {
          //show the next button if the page value is less than totalPage(20)
          liTag += `<a href="/admin/order-detail/${
            this.$route.params.id
          }/page=${page +
            1}"><li class="btn next" ><span>Next <i class="fas fa-angle-right"></i></span></li></a>`;
        }
        element.innerHTML = liTag; //add li tag inside ul

        return liTag; //reurn the li tag
      }
    },
  },
};
</script>
<style scoped>
a {
  text-decoration: none;
}
.modal-title {
  color: red;
}
</style>
