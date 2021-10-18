<template>
  <div>
    <SideBar></SideBar>
    <section class="home-section">
        <Navbar></Navbar>

      <div class="home-content">
        <h1>Check Live Theo Uid</h1>
        <p>
          <textarea
            v-model="listUid"
            id="textExample"
            style="border-radius: 5 px solid black;margin-left:2.5%;margin-right:2.5%; max-width:95%"
            rows="10"
            cols="60"
          ></textarea>
        </p>
        <div class="d-flex justify-content-center">
          <button
            class="btn btn-primary"
            style="margin :center"
            id="type"
            @click="check"
          >
            Kiểm Tra
          </button>
        </div>
        <div class="containers">
          <div class="container container-left container container--init">
            <h4>Danh sách Live</h4>
            <span>{{ countLive + "/" + countUid }}</span>
            <textarea
              name="init"
              v-model="listLive"
              id="init"
              spellcheck="false"
            ></textarea>
          </div>

          <div class="container container-right container container--result">
            <h4>Danh sách Die</h4>
            <span>{{ countDie + "/" + countUid }}</span>
            <textarea
              name="result"
              v-model="listDie"
              id="result"
              spellcheck="false"
            ></textarea>
          </div>
        </div>
      </div>
    </section>
    <Footer></Footer>
  </div>
</template>
<script>
import SideBar from "./SideBar.vue";
import Footer from "./Footer.vue";

export default {
  name: "CheckLive",
  data() {
    return {
      listUid: "",
      listLive: "",
      listDie: "",
      count: null,
      countUid: 0,
      countDie: 0,
      countLive: 0,
    };
  },
  components: {
    SideBar,
    Footer,
  },
  mounted() {
    document.title = "Check Live/Die";
  },
  methods: {
    check() {
      this.$store.commit("setIsLoading", true);
      this.countUid = 0;
      this.countLive = 0;
      this.countDie = 0;
      var die = [];
      var live = [];
      var arrayUid = this.listUid.split("\n");
      if (arrayUid != []) {
        this.countUid = arrayUid.length;
        for (var i = 0; i < arrayUid.length; i++) {
          if (this.checkUid(arrayUid[i])) {
            live.push(arrayUid[i]);
            this.countLive++;
          } else {
            die.push(arrayUid[i]);
            this.countDie++;
          }
        }
        if (live != []) {
          this.listLive = live.join("\n");
        }

        if (die != []) {
          this.listDie = die.join("\n");
        }
      }
      this.$store.commit("setIsLoading", false);
    },
    checkUid(uid) {
      var url = "https://graph.facebook.com/" + uid + "/picture?type=normal";

      var xmlHttp = new XMLHttpRequest();
      xmlHttp.open("GET", url, false); // false for synchronous request
      xmlHttp.send(null);
      if (xmlHttp.responseURL.includes("//static")) {
        return false;
      }
      return true;
      // xhr.send(null);
    },
    httpGetAsync(theUrl, callback) {
      var xmlHttp = new XMLHttpRequest();
      xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
          callback(xmlHttp.responseText);
      };
      xmlHttp.open("GET", theUrl, true); // true for asynchronous
      xmlHttp.send(null);
    },
  },
};
</script>

<style scoped>
p {
  margin: 1.2rem 0;
}

textarea {
  width: 100%;
  height: 150px;
  margin: 0;
  border: 1px solid #ccc;
  border-radius: 10px;
  font-size: 13px;
  font-family: monospace;
}

.wrapper {
  width: 100%;
  margin: 1.5rem auto 4rem;
}

.panel {
  position: relative;
  z-index: 1;
  margin-bottom: 2.5rem;
  display: flex;
  justify-content: space-between;
}

.options {
  position: relative;
}

.options__middle-word {
  vertical-align: middle;
  color: #aaa;
}

.options__text {
  display: inline-block;
  border-bottom: 1px dashed;
  color: steelblue;
  cursor: pointer;
}
.options__input:checked + .options__text {
  border: 0;
  color: inherit;
  cursor: default;
}

.expander {
  position: relative;
  z-index: 2;
}

.expanded {
  position: absolute;
  top: -15px;
  right: -15px;
  left: -15px;
  padding: 2rem 1.5rem 1rem;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 0 5px rgba(0, 0, 0, 0.1);
}

.button-example {
  padding: 0;
  border: 0;
  border-bottom: 1px dashed;
  line-height: 1;
  align-self: center;
  font: inherit;
  font-size: 14px;
  color: steelblue;
  cursor: pointer;
}

.containers {
  margin-bottom: 32px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.container {
  position: relative;
  width: 48%;
  margin-bottom: 1em;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}
.container-left {
  color: green;
}
.container-right {
  color: red;
}
</style>
