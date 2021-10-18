import {
  createStore
} from 'vuex'
import {
  authRequest,
  loginUser,
  ACCESS_TOKEN,
  logoutUser,
} from '../services/api/auth';
import {myUser} from '../services/api/user.js'
import jwt_decode from 'jwt-decode';

export default createStore({
  state: {
    user: JSON.parse(localStorage.getItem('currentUser')),
    isLoggedIn: false,
    isLoading: false,
    pageNotFound:false,
    isAdmin:false,
  },
  mutations: {
    checkAdmin(state){
      if (localStorage.getItem("access_token")) {
        const decodeUser = jwt_decode(localStorage.getItem("access_token"));
        if (decodeUser.is_superuser == true){
          state.isAdmin = true
        }else{
          state.isAdmin = false
        }
      }else{
        state.isAdmin = false
      }
    },
    checkAuth(state) {
      if (localStorage.getItem("access_token")) {
        state.isLoggedIn = true
        authRequest.defaults.headers.Authorization = `Bearer ${window.localStorage.getItem(ACCESS_TOKEN)}`;
        myUser()
        .then((response) =>{
        state.user = response
        localStorage.setItem('currentUser', JSON.stringify(response));
        })
        .catch((error)=>{
          console.log(error)
       
      })
      } else {
        state.isLoggedIn = false
        authRequest.defaults.headers.Authorization = ''
      }
    },
    async getUser(state){
      await myUser()
        .then((response) =>{
        state.user = response
        localStorage.setItem('currentUser', JSON.stringify(response));
        })
        .catch((error)=>{
          console.log(error)
       
      })
    },
    loginSuccess(state, userId) {
      state.isLoggedIn = true;
    },
    logout(state) {
      state.user = null;
      state.isLoggedIn = false;
      localStorage.removeItem('currentUser')
    },
    setIsLoading(state, status) {
      state.isLoading = status
    },
  },
  actions: {
    reloadPage({commit}){
      commit({
        type: 'checkAdmin'
      });
      commit({
        type: 'checkAuth'
      });
    }
    ,
    checkAdmin({commit}){
      commit('check_admin');
    },
    async login({commit}, {email,password}) {
      commit('setIsLoading',true);
      await loginUser(email, password)
        .then((response) => {
          console.log(response)
          window.localStorage.setItem('access_token', response.access);
          window.localStorage.setItem('refresh_token', response.refresh);
          commit({
            type: 'getUser'
          });
          commit({
            type: 'loginSuccess',
            email
          });
          commit({
            type: 'checkAdmin'
          });
      
          return Promise.resolve();
        })
        .catch((error) => {
          commit({
            type: 'logout'
          });
          
          return Promise.reject(error);
        });
      commit('setIsLoading',false);
    },
    logout({commit}) {
      commit('logout');
      logoutUser();
    },
  },
  modules: {},
});