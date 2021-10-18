<template>
  <div>
    <SideBar></SideBar>
    <section class="home-section">
      <Navbar></Navbar>
      <div class="home-content">
        <div class="header">
          <h1>Nạp tiền</h1>
          <div class="breadcrumb">
            <li class="breadcrumb-item">Trang chủ</li>
            <li class="breadcrumb-item">Nạp tiền</li>
          </div>
        </div>
        <div class="form-rechange">
            <div class="form-title">
              Nạp tiền từ ví Momo
            </div>
            <div class="form-icon">
              <img src="https://upload.wikimedia.org/wikipedia/vi/archive/f/fe/20201011055543%21MoMo_Logo.png"/>
            </div>
            <div class="input-money">
              <h4>Nhập số tiền muốn nạp</h4>
              <div class="input-group ">
                <input type="number" v-model="money" class="form-control" placeholder="Nhập số tiền" aria-label="Recipient's username" aria-describedby="basic-addon2">
                <span class="input-group-text" id="basic-addon2">Nghìn VNĐ</span>
              </div>
                   
              <button data-bs-toggle="modal" @click="createQrCode()" data-bs-target="#momoModal" >Tạo QR Code</button>
            </div>
            <div class="modal fade" id="momoModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title" id="exampleModalLabel">Thanh toán Momo qua QR Code</h5>
                  <button type="button" @click="c" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  <div class="modal-recharge">
                    <div id="qrcode"></div>
                    <h4><b>Số tiền thanh toán là: </b> {{money}}.000 VNĐ</h4>
                    <h5><b>Nội dung chuyển khoản: </b> Nạp tiền vào id số {{$store.state.user.id}}</h5>
                    <span>Lưu ý: <i>Vui lòng nhập đúng nội dung chuyển khoản</i></span>
                  </div>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <Footer></Footer>
  </div>
</template>

<script>
import "mosha-vue-toastify/dist/style.css";


export default {
  name: "Recharge",
  data() {
    return {
        money:null,
    };
  },
  mounted() {
    document.title = "Nạp Tiền";
  },
  computed: {
  },
  methods: {
    createQrCode() {
      const target = document.getElementById('qrcode')
      // target = ""
      const url = `https://test-payment.momo.vn/pay/store/MOMOIQA420180417-storeid01?a=${this.money}&b=B001221&extra=454SKDJ124&s=601a7280711dd72bfae8c365801f5e257311a1ebd8779cf3bc4as474a8`;
      const qrcode = new QRCode(target, {
      text: url,
      width: 200,
      height: 200,
      colorDark : '#000',
      colorLight : '#fff',
      correctLevel : QRCode.CorrectLevel.H
    });
    }
  },
};
</script>
<style scoped>
.form-rechange{
  background-color:white;
  margin:15px 5%;
  widows: 90%;
  border: 2px solid #0a2558;
  border-radius:7px 7px 0px 0px;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
}
.form-rechange .form-title{
  height:40px;
  width:100%;
  display: flex;
  justify-content: center;
  color:white;
  align-items: center;
  background-color: #0a2558;

}
.form-rechange .form-icon{
    padding:20px 0;
}
.form-rechange .form-icon img{
  width:180px;
  height:180px
}
.form-rechange .input-money{
    padding:20px 0px;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.form-rechange .input-money .input-group{
    padding:10px;
}
.form-rechange .input-money .input-group .input-group-text {
  color: white;
  background-color: #0a2558;
  border: 1px solid #0a2558;
}
.form-rechange .input-money button{
  padding:5px 10px;
  border: 2px solid #0a2558;
  border-radius:5px;
  color:#0a2558;
  font-weight:600;
}
.form-rechange .input-money button:hover{
  color:white;
  background-color:#0a2558;
}
.modal-title{
  width:100%;
  text-align:center;
}
.modal-recharge{
  display:flex;
  flex-direction:column;
  align-items: center;
  justify-content:center;
}
.modal-recharge #qrcode{
  padding: 5px 5px;
  border: 5px solid #af1a70;
  border-radius:7px;
}
.modal-recharge span{
  font-size:18px;
  padding: 10px;
  color: #E33367;
  font-weight:600;
}
</style>
