<template>
  <div>
    <PageNotFound v-show="hasPage == false"></PageNotFound>
    <SideBar v-show="hasPage == true"></SideBar>
    <section class="home-section" v-show="hasPage == true">
      <Navbar></Navbar>
      <div class="home-content">
        <div class="header">
          <h1>Lịch Sử Mua Hàng</h1>
          <div class="breadcrumb">
            <li class="breadcrumb-item">Trang chủ</li>
            <li class="breadcrumb-item">Lịch Sử Mua Hàng</li>
          </div>
        </div>
        <div class="table-responsive">
          <table>
            <caption>
              Lịch Sử Mua Hàng
            </caption>
            <thead>
              <tr>
                <th class="time" scope="col">Thời Gian</th>
                <th class="category-history" scope="col">Loại Tài Khoản</th>
                <th class="custom" scope="col">Đơn Giá</th>
                <th class="custom" scope="col">Số Lượng</th>
                <th class="custom" scope="col">Tổng Tiền</th>
                <th class="get-account" scope="col"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in listOrders" :key="item.created_at">
                <td class="time" scope="col">
                  {{ convertTime(item.created_at) }}
                </td>
                <td data-label="Category">
                  {{ item.category.name }}
                </td>
                <td class="custom" data-label="Due Date">
                  {{ item.category.price }}
                </td>
                <td class="custom" data-label="Amount">{{ item.quantity }}</td>
                <td class="custom" data-label="Period">
                  {{ item.paid_amount }}
                </td>
                <th class="get-account" scope="col">
                  <button
                    data-bs-toggle="modal"
                    data-bs-target="#exampleModal"
                    @click="getFile(item.id)"
                  >
                    Lấy Dữ Liệu
                  </button>
                </th>
                <div
                  class="modal fade"
                  id="exampleModal"
                  tabindex="-1"
                  aria-labelledby="exampleModalLabel"
                  aria-hidden="true"
                >
                  <div class="modal-dialog modal-dialog-centered modal-xl">
                    <div class="modal-content">
                      <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">
                          Lấy Dữ Liệu
                        </h5>
                        <button
                          type="button"
                          class="btn-close"
                          data-bs-dismiss="modal"
                          aria-label="Close"
                        ></button>
                      </div>
                      <div class="modal-body">
                        <form>
                          <div class="mb-3">
                            <label for="message-text" class="col-form-label"
                              >Message:</label
                            >
                            <textarea
                              class="form-control"
                              id="message-text"
                              rows="10"
                              v-model="details"
                            ></textarea>
                          </div>
                        </form>
                      </div>
                      <div class="modal-footer">
                        <button
                          type="button"
                          class="btn btn-secondary"
                          data-bs-dismiss="modal"
                        >
                          Đóng
                        </button>
                        <button
                          type="button"
                          class="btn btn-primary"
                          @click="download(details)"
                        >
                          Tải Dữ Liệu
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="pagination">
          <ul></ul>
        </div>
      </div>
    </section>
    <Footer v-show="hasPage == true"></Footer>
  </div>
</template>
<script>
import moment from "moment";
import { changPage, getDetail } from "../../services/api/history";
import { mapState } from "vuex";
import PageNotFound from "../PageNotFound.vue";
import SideBar from "./SideBar.vue";
import Footer from "./Footer.vue";
import { createToast } from "mosha-vue-toastify";
import "mosha-vue-toastify/dist/style.css";

export default {
  name: "Histories",
  data() {
    return {
      listOrders: {},
      currentPage: 1,
      totalPages: 8,
      linkNext: null,
      linkPrev: null,
      details: null,
      hasPage: true,
    };
  },
  components: {
    PageNotFound,
    SideBar,
    Footer,
  },
  computed: {
    ...mapState(["isLoggedIn"]),
  },
  mounted() {
    this.getHistory();

    document.title = "Lịch sử mua";
  },
  methods: {
    download( text) {
      var currentdate = new Date();
      var filename =  currentdate.getFullYear().toString() +currentdate.getFullDate().toString() +(currentdate.getMonth()+1).toString()+currentdate.getHours().toString()+currentdate.getMinutes().toString()+currentdate.getSeconds().toString()+".txt"
      var element = document.createElement("a");
      element.setAttribute(
        "href",
        "data:text/plain;charset=utf-8," + encodeURIComponent(text)
      );
      element.setAttribute("download", filename);

      element.style.display = "none";
      document.body.appendChild(element);

      element.click();

      document.body.removeChild(element);
    },
    async getHistory() {
      this.errors = [];
      this.$store.commit("setIsLoading", true);
      var url = `/api/v1/history/?${this.$route.params.page_slug}`;
      await changPage(url)
        .then((response) => {
          this.listOrders = response.results;
          this.totalPages = response.total_pages;
          this.currentPage = response.current_page;
          this.linkNext = response.links.next;
          this.linkPrev = response.links.previous;
          if (this.currentPage != null && this.totalPages != null) {
            this.createPgn();
          }
          this.hasPage = true;
        })
        .catch((error) => {
          console.log(error);
          this.hasPage = false;
        });
      this.$store.commit("setIsLoading", false);
    },
    convertTime(time) {
      var t = moment(time);
      return t.format("L") + "\n" + t.format("LTS");
    },
    getFile(id) {
      getDetail(id)
        .then((res) => {
          this.details = res;
          console.log(res);
        })
        .catch((error) => {
          createToast(
            {
              title: "Lỗi",
              description: "Xem thông tin thất bại vui lòng thử lại",
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
          liTag += `<a href="/user/history/page=${page -
            1}/"><li class="btn prev"><span><i class="fas fa-angle-left"></i> Prev</span></li></a>`;
        }
        if (page > 1 && page == 2) {
          //show the next button if the page value is greater than 1
          liTag += `<a href="/user/history/"><li class="btn prev"><span><i class="fas fa-angle-left"></i> Prev</span></li></a>`;
        }

        if (page > 2 && totalPage > 4) {
          //if page value is less than 2 then add 1 after the previous button
          liTag += `<a href="/user/history/"><li class="first numb"><span>1</span></li></a>`;
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
          ``;
          liTag += `<a href="/user/history/page=${plength}"><li class="numb ${active}"><span>${plength}</span></li></a>`;
        }

        if (page < totalPage - 1 && totalPage > 4) {
          //if page value is less than totalPage value by -1 then show the last li or page
          if (page < totalPage - 2 && totalPage > 5) {
            //if page value is less than totalPage value by -2 then add this (...) before the last li or page
            liTag += `<li class="dots"><span>...</span></li>`;
          }
          liTag += `<a href="/user/history/page=${totalPage}"><li class="last numb" ><span>${totalPage}</span></li></a>`;
        }

        if (page < totalPage) {
          //show the next button if the page value is less than totalPage(20)
          liTag += `<a href="/user/history/page=${page +
            1}"><li class="btn next" ><span>Next <i class="fas fa-angle-right"></i></span></li></a>`;
        }
        element.innerHTML = liTag; //add li tag inside ul

        return liTag; //reurn the li tag
      }
    },
  },
};
</script>
<style>
a {
  text-decoration: none;
}
.table-time {
  width: 100px;
}
</style>
