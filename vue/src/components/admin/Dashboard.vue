<template>
  <div>
    <SideBarAdmin></SideBarAdmin>
    <section class="home-section">
      <NavbarAdmin></NavbarAdmin>
      <div class="home-content">
      <div class="overview-boxes">
       
        <div class="box">
          <div class="right-side">
            <div class="box-topic">Total Sales</div>
            <div class="number">{{ formatValue(sales) }}</div>
            <div class="indicator" v-if="sales > salesOld">
              <i class='bx bx-up-arrow-alt'></i>
              <span class="text">Up {{formatValue(sales - salesOld)}} ( {{formatPercent((sales - salesOld)/salesOld * 100)}} %) From Month</span>
            </div>
            <div class="indicator" v-else>
              <i class='bx bx-down-arrow-alt down'></i>
              <span class="text">Down {{formatValue(salesOld - sales)}} ( {{formatPercent((salesOld - sales)/salesOld * 100)}} %) From Month</span>
            </div>
          </div>
         
            <i class='bx bxs-cart-download cart one' ></i>
        </div>
        <div class="box">
          <div class="right-side">
            <div class="box-topic">Total Profit</div>
            <div class="number">{{ formatValue(profit) }}</div>
            <div class="indicator" v-if="profit > profitOld">
              <i class='bx bx-up-arrow-alt'></i>
              <span class="text">Up {{formatValue(profit - profitOld)}}( {{formatPercent((profit - profitOld)/profitOld * 100)}} %) From Month</span>
            </div>
            <div class="indicator" v-else>
             <i class='bx bx-down-arrow-alt down'></i>
              <span class="text">Down {{formatValue(profitOld - profit)}}( {{formatPercent((profitOld - profit)/profitOld * 100)}} %)  From Month</span>
            </div>
          </div>
          <i class='bx bx-money cart two' ></i>
        </div>
        <div class="box">
          <div class="right-side">
            <div class="box-topic">Total User</div>
            <div class="number">{{formatValue(totalUser)}}</div>
            <div class="indicator" v-if="totalUser > totalUserOld">
              <i class='bx bx-up-arrow-alt'></i>
              <span class="text">Up {{formatValue(totalUser - totalUserOld)}} ( {{formatPercent((totalUser - totalUserOld)/totalUserOld * 100)}} %)From Month </span>
            </div>
            <div class="indicator" v-else>
              <i class='bx bx-down-arrow-alt down'></i>
              <span class="text">Down {{ formatValue(totalUserOld - totalUser) }} ( {{formatPercent((totalUserOld - totalUser)/totalUserOld * 100)}} %) From Month </span>
            </div>
          </div>
          <i class='bx bx-user cart three' ></i>
        </div>
         <div class="box">
          <div class="right-side">
            <div class="box-topic">Total Deposited</div>
            <div class="number">{{formatValue(coinRecharge)}}</div>
            <div class="indicator" v-if="coinRecharge > coinRechargeOld">
              <i class='bx bx-up-arrow-alt'></i>
              <span class="text">Up {{ formatValue(coinRecharge - coinRechargeOld) }} ( {{formatPercent((coinRecharge - coinRechargeOld)/coinRechargeOld * 100)}} %) From Month </span>
            </div>
             <div class="indicator" v-else>
              <i class='bx bx-down-arrow-alt down'></i>
              <span class="text">Down {{ formatValue(coinRechargeOld - coinRecharge) }} ( {{formatPercent((coinRechargeOld - coinRecharge)/coinRechargeOld * 100)}} %) From Month</span>
            </div>
          </div>
          <i class='bx bxs-cart-add cart four' ></i>
        </div>
      </div>
      <div class="middle-box">
        <div class="table-responsive table-left">
          
          <table>
          <caption>Top 5 User Deposited In Month</caption>
            <thead class="thead-light">
              <tr>
                <th>User ID</th>
                <th>Email</th>
                <!-- <th>IP</th> -->
                <th>Money</th>
              
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in topUserRecharge" :key="user">
                <td>{{user[0].users.id }}</td>
                <td>{{ user[0].users.email}}</td>
                <td>{{ user[1].money }}</td>
              </tr>
            </tbody>
          </table>
      </div>
      <div class="table-responsive table-left">
          
          <table>
          <caption>Top 5 Bills In Month</caption>
            <thead class="thead-light">
              <tr>
                <th>Email</th>
                <th>Category</th>
                <th>Quantity</th>
                <th>Amount</th>
              
              </tr>
            </thead>
            <tbody>
              <tr v-for="bill in topBills" :key="bill">
                <td>{{ bill.user.email  }}</td>
                <td>{{ bill.category.name}}</td>
                <td>{{ bill.quantity }}</td>
                <td>{{ bill.paid_amount }}</td>
              </tr>
            </tbody>
          </table>
      </div>
  
      </div>
      
       <div class="table-responsive table-bottom">
          <table>
            <caption>Most recent purchase history</caption>
            <thead class="thead-light">
              <tr>
                <th>Time</th>
                <th>User</th>
                <th>Category</th>
                <th>Price</th>
                <th>Quantity</th>
                <th>Total</th>  
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in historyOrders" :key="order">
                <td>{{ convertTime(order.created_at) }}</td>
                <td>{{ order.user.email }}</td>
                <td>{{ order.category.name }}</td>
                <td>{{ order.category.price }}</td>
                <td>{{ order.quantity }}</td>
                <td>{{ order.paid_amount }}</td>
              </tr>
              
            </tbody>
          </table>
        </div>
         <div class="button-more">
           <router-link to="/admin/orders">
            <a href="#"><p class="button-custom">See All</p></a>
           </router-link>
          </div>
       
    </div>
    </section>
    <FooterAdmin></FooterAdmin>
  </div>
</template>

<script>

import moment from "moment";
import { getDataDashboard } from '../../services/api/admin';
export default {
  name:"Dashboard",
  data() {
    return {
      topUserRecharge:[],
      salesOld:null,
      sales:null,
      profitOld:null,
      profit:null,
      totalUserOld:null,
      totalUser:null,
      coinRechargeOld:null,
      coinRecharge:null,
      historyOrders:[],
      data :null,
      direction: null,
      margin:null,
      topBills:null,
    };
  },
  mounted() {
    this.getData();
    document.title = "DashBoard | Admin Page";
  }
  ,
  methods: {
     formatValue(value) {
      let val = (value / 1).toFixed(0).replace(".", ",");
      return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    },
    formatPercent(value) {
      let val = (value / 1).toFixed(2).replace(".", ",");
      return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    },
     convertTime(time) {
      var t = moment(time);
      return t.format("L") + "\n" + t.format("LTS");
    },
    async getData(){
      this.$store.commit("setIsLoading", true);
      await getDataDashboard()
      .then((response) =>{
        console.log(response)
        this.salesOld = response[1]['salesOld'] 
        this.sales = response[2]['sales'] 
        this.profitOld = response[3]['profitOld'] 
        this.profit = response[4]['profit'] 
        this.totalUserOld = response[5]['totalUserOld'] 
        this.totalUser = response[6]['totalUser'] 
        this.coinRechargeOld = response[7]['coinRechargeOld'] 
        this.coinRecharge = response[8]['coinRecharge'] 
        this.historyOrders = response[9]   
        this.topBills = response[10]   
        this.topUserRecharge = response[0]['topUserRecharge']
      })
      .catch((error)=>{
        console.log(error);
      })
      this.$store.commit("setIsLoading", false);

  }}
}
</script>
<style scoped>
a {
  text-decoration: none;
}
.modal-title {
  color: red;
}
.row > * {
  margin-top: 10px;
}
.card {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-evenly;
  border-radius: 6px;
  padding: 5px 0px;
  /* border-left-color: #0a2558; */
  border-left: 5px;
}
.card-left .bx {
  color: #0a2558;
  font-weight: 600;
  font-size: 50px;
  margin: 0px;
}
.card-right {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.card-right h6,
.card-right p {
  margin: 0px;
}
.card-right p {
  color: #0a2558;
}
</style>
