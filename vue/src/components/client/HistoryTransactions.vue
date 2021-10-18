<template>
  <div>
    <PageNotFound v-show="hasPage == false"></PageNotFound>
    <SideBar v-show="hasPage == true"></SideBar>
    <section class="home-section" v-show="hasPage == true">
        <Navbar></Navbar>

      <div class="home-content">
        <div class="header">
          <h1>Lịch Sử Giao Dịch</h1>
          <div class="breadcrumb">
            <li class="breadcrumb-item">Trang chủ</li>
            <li class="breadcrumb-item">Lịch Sử Giao Dịch</li>
          </div>
        </div>
        <div class="table-responsive">
          <table>
            <caption>
              Lịch Sử Giao Dịch
            </caption>
            <thead>
              <tr>
                <th class="time" scope="col">Thời Gian</th>
                <th class="description" scope="col">Chi tiết</th>
                <th class="custom" scope="col">Hình thức</th>
                <th class="custom" scope="col">Giá Tiền</th>
                <th class="confirm" scope="col">Trạng Thái</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in listTransaction" :key="item.created_at">
                <td class="time" scope="col">
                  {{ convertTime(item.created_at) }}
                </td>
                <th class="description" scope="col">{{ item.description }}</th>
                <th class="custom" scope="col">
                  {{ convertOption(item.option) }}
                </th>
                <th class="custom" scope="col">{{ item.money }}</th>
                <th class="confirm" scope="col">
                  {{ item.confirm ? "Thành Công" : "Thất Bại" }}
                </th>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="mx-auto">
          <div class="pagination">
            <ul></ul>
          </div>
        </div>
      </div>
    </section>
    <Footer v-show="hasPage == true"></Footer>
  </div>
</template>
<script>
import moment from "moment";

import { changPage } from "../../services/api/history";
import { mapState } from "vuex";
import PageNotFound from "../PageNotFound.vue";
import SideBar from "./SideBar.vue";
import Footer from "./Footer.vue";

export default {
  name: "HistoryTransactions",
  data() {
    return {
      listTransaction: {},
      currentPage: null,
      totalPages: null,
      linkNext: null,
      linkPrev: null,
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

    document.title = "Lịch sử giao dịch";
  },
  methods: {
    async getHistory() {
      this.errors = [];
      this.$store.commit("setIsLoading", true);
      if (this.$route.params.page_slug) {
        var url = `/api/v1/history-transaction/?${this.$route.params.page_slug}`;
        await changPage(url)
          .then((response) => {
            this.listTransaction = response.results;
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
      }
      this.$store.commit("setIsLoading", false);
    },
    convertOption(option) {
      if (option == "4") {
        return "Trừ Tiền";
      } else if (option == 3) {
        return "Khuyến mãi";
      } else if (option == 2) {
        return "Cộng Tiền";
      }
      return "Nạp Tiền";
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
          liTag += `<a href="/user/history-transaction/page=${page -
            1}/"><li class="btn prev"><span><i class="fas fa-angle-left"></i> Prev</span></li></a>`;
        }
        if (page > 1 && page == 2) {
          //show the next button if the page value is greater than 1
          liTag += `<a href="/user/history-transaction/page=1"><li class="btn prev"><span><i class="fas fa-angle-left"></i> Prev</span></li></a>`;
        }

        if (page > 2 && totalPage > 4) {
          //if page value is less than 2 then add 1 after the previous button
          liTag += `<a href="/user/history-transaction/page-1"><li class="first numb"><span>1</span></li></a>`;
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
          liTag += `<a href="/user/history-transaction/page=${plength}"><li class="numb ${active}"><span>${plength}</span></li></a>`;
        }

        if (page < totalPage - 1 && totalPage > 4) {
          //if page value is less than totalPage value by -1 then show the last li or page
          if (page < totalPage - 2 && totalPage > 5) {
            //if page value is less than totalPage value by -2 then add this (...) before the last li or page
            liTag += `<li class="dots"><span>...</span></li>`;
          }
          liTag += `<a href="/user/history-transaction/page=${totalPage}"><li class="last numb" ><span>${totalPage}</span></li></a>`;
        }

        if (page < totalPage) {
          //show the next button if the page value is less than totalPage(20)
          liTag += `<a href="/user/history-transaction/page=${page +
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
</style>
