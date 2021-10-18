<template>
  <div>
    <SideBarAdmin></SideBarAdmin>
    <section class="home-section">
      <NavbarAdmin></NavbarAdmin>
      <div class="home-content">
        <div class="header">
          <h1>Category List</h1>
          <div class="breadcrumb">
            <li class="breadcrumb-item">Trang chủ</li>
            <li class="breadcrumb-item">Category</li>
          </div>
        </div>
        <div class="table-top">
          <p>
            From {{ currentPage == 1 ? 1 : (currentPage - 1) * 20 }} to
            {{ currentPage * 20 > count ? count : currentPage * 20 }} (Total :
            {{ count }})
          </p>
          <caption>
            Account
          </caption>
          <form class="table-search">
            <input
              type="text"
              v-model="query"
              required
              pattern="[0-9a-zA-Z_.-@# ]*"
              oninput="this.setCustomValidity('')"
              oninvalid="this.setCustomValidity('Vui lòng không nhập ký tự đặc biệt')"
            />
            <button @click="search(query)">Search</button>
          </form>
        </div>
        <div class="table-responsive">
          <table>
            <thead class="thead-light">
              <tr>
                <th>ID</th>
                <th class="category-history">Name</th>
                <th>Price</th>
                <th>Discount</th>
                <th>Total</th>
                <th>Exists</th>
                <th>Sold</th>
                <th class="time">Created At</th>
                <th class="time">Updated At</th>
                <th></th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="category in categories" :key="category">
                <td>{{ category.id }}</td>
                <td class="category-history">{{ category.name }}</td>
                <td>{{ category.price }}</td>
                <td>{{ category.discount }}</td>
                <td>{{ category.total_quantity }}</td>
                <td>{{ category.get_quantity }}</td>
                <td>{{ category.sale_figure }}</td>
                <td>{{ convertTime(category.created_at) }}</td>
                <td>{{ convertTime(category.updated_at) }}</td>
                <td>
                  <a
                    href="#"
                    class="btn btn-sm btn-primary"
                    @click="getDetail(category.id)"
                    >Detail</a
                  >
                </td>
                <td>
                  <a
                    href="#"
                    class="btn btn-sm btn-danger"
                    data-bs-toggle="modal"
                    data-bs-target="#staticBackdrop"
                    @click="beforeDelete(account.id)"
                    >Delete</a
                  >
                </td>
              </tr>
            </tbody>
          </table>
        </div>
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
                  Delete Category
                </h5>
                <button
                  type="button"
                  class="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>
              <div class="modal-body">
                Would you like to detele Category?
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
                  class="btn btn-danger"
                  @click="dltCategory()"
                  data-bs-dismiss="modal"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="pagination">
          <ul></ul>
        </div>
      </div>
    </section>
    <FooterAdmin></FooterAdmin>
  </div>
</template>

<script>
import moment from "moment";
import FooterAdmin from "../FooterAdmin.vue";
import NavbarAdmin from "../NavbarAdmin.vue";
import SideBarAdmin from "../SideBarAdmin.vue";
import { changePage } from "../../../services/api/admin";
import "mosha-vue-toastify/dist/style.css";
import { createToast } from "mosha-vue-toastify";

export default {
  data() {
    return {
      categories: [],
      totalPages: null,
      currentPage: null,
      count: null,
      query: null,
    };
  },
  components: {
    FooterAdmin,
    SideBarAdmin,
    NavbarAdmin,
  },
  mounted() {
    this.getData();
    document.title = "Category | Admin Page";
  },
  methods: {
    async getData() {
      this.$store.commit("setIsLoading", true);
      var url = `/api/v1/categories/?${this.$route.params.page_slug}`;
      await changePage(url)
        .then((response) => {
          this.categories = response.results;
          this.totalPages = response.total_pages;
          this.currentPage = response.current_page;
          this.count = response.count;
          this.createPgn();
        })
        .catch((error) => {
          createToast(
            {
              title: "Thất Bại",
              description: "Lấy thông tin không thành công",
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
    getDetail(id) {
      this.$router.push(`/admin/category/category-detail/${id}`);
    },
    search(query) {
      this.$router.push(`/admin/category/search/query=${query}/page=1`);
    },
    beforeDelete(id) {
      this.id = id;
    },
    async dltCategory() {
      this.$store.commit("setIsLoading", true);
      
      await deleteCategory(this.id)
        .then((response) => {
          createToast(
            {
              title: "Thành công",
              description: "Bạn đã xóa thành công",
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
          console.log(error);
          createToast(
            {
              title: "Thành công",
              description: "Bạn đã xóa thất bại",
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
        });
      this.$store.commit("setIsLoading", false);
      this.$router.go(this.$router.currentRoute);
    },
    convertTime(time) {
      var t = moment(time);
      return t.format("L") + "\n" + t.format("LTS");
    },
    createPgn() {
      // selecting required element
      const element = document.querySelector(".pagination ul");
      //calling function with passing parameters and adding inside element which is ul tag
      element.innerHTML = createPagination(this.totalPages, this.currentPage);
      function createPagination(totalPage, page) {
        let liTag = "";
        let active;
        let beforePage = page - 1;
        let afterPage = page + 1;
        if (page > 1 && page > 2) {
          //show the next button if the page value is greater than 1
          liTag += `<a href="/admin/categories/page=${page -
            1}/"><li class="btn prev"><span><i class="fas fa-angle-left"></i> Prev</span></li></a>`;
        }
        if (page > 1 && page == 2) {
          //show the next button if the page value is greater than 1
          liTag += `<a href="/admin/categories/"><li class="btn prev"><span><i class="fas fa-angle-left"></i> Prev</span></li></a>`;
        }

        if (page > 2 && totalPage > 4) {
          //if page value is less than 2 then add 1 after the previous button
          liTag += `<a href="/admin/categories/"><li class="first numb"><span>1</span></li></a>`;
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
          liTag += `<a href="/admin/categories/page=${plength}"><li class="numb ${active}"><span>${plength}</span></li></a>`;
        }

        if (page < totalPage - 1 && totalPage > 4) {
          //if page value is less than totalPage value by -1 then show the last li or page
          if (page < totalPage - 2 && totalPage > 5) {
            //if page value is less than totalPage value by -2 then add this (...) before the last li or page
            liTag += `<li class="dots"><span>...</span></li>`;
          }
          liTag += `<a href="/admin/categories/page=${totalPage}"><li class="last numb" ><span>${totalPage}</span></li></a>`;
        }

        if (page < totalPage) {
          //show the next button if the page value is less than totalPage(20)
          liTag += `<a href="/admin/categories/page=${page +
            1}"><li class="btn next" ><span>Next <i class="fas fa-angle-right"></i></span></li></a>`;
        }
        element.innerHTML = liTag; //add li tag inside ul

        return liTag; //reurn the li tag
      }
    },
  },
};
</script>
