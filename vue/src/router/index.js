import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/client/Home.vue';
import Login from '../components/Login.vue';
import Recharge from '../components/client/Recharge.vue';

Recharge
import ChangePassword from '../components/client/ChangePassword.vue';
import History from '../components/client/History.vue';
import Histories from '../components/client/Histories.vue';
import HistoryTransactions from '../components/client/HistoryTransactions.vue';
import HistoryTransaction from '../components/client/HistoryTransaction.vue';
import PageNotFound from '../components/PageNotFound.vue';
import CheckLive from '../components/client/CheckLive.vue';

import Dashboard from '../components/admin/Dashboard.vue';

import Accounts from '../components/admin/Account/Accounts.vue';
import Account from '../components/admin/Account/Account.vue';
import AccountDetail from '../components/admin/Account/AccountDetail.vue';
import AddAccount from '../components/admin/Account/AddAccount.vue';
import AccountSearch from '../components/admin/Account/AccountSearch.vue';


import Categories from '../components/admin/Category/Categories.vue';
import Category from '../components/admin/Category/Category.vue';
import AddCategory from '../components/admin/Category/AddCategory.vue';
import CategoryDetail from '../components/admin/Category/CategoryDetail.vue';
import CategorySearch from '../components/admin/Category/CategorySearch.vue';


import Users from '../components/admin/Users/Users.vue';
import User from '../components/admin/Users/User.vue';
import UserDetail from '../components/admin/Users/UserDetail.vue';
import CreateUser from '../components/admin/Users/CreateUser.vue';
import UserSearch from '../components/admin/Users/UserSearch.vue';


import Transaction from '../components/admin/Transaction/Transaction.vue';
import Transactions from '../components/admin/Transaction/Transactions.vue';
import TransactionSearch from '../components/admin/Transaction/TransactionSearch.vue';


import Order from '../components/admin/Order/Order.vue';
import Orders from '../components/admin/Order/Orders.vue';
import OrderDetail from '../components/admin/Order/OrderDetail.vue';
import OrderSearch from '../components/admin/Order/OrderSearch.vue';


import store from "../store/index"



import { ACCESS_TOKEN, REFRESH_TOKEN } from '../services/api/auth';

const PUBLIC_PATHS = ['/', '/login',"/register",'/account/checklive'];

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    props: true,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/recharge',
    name: 'Recharge',
    component: Recharge,
  },
  {
    path: '/user/change-password',
    name: 'ChangePassword',
    component: ChangePassword,
    props: true 
  },
  {
    path: '/user/history/:page_slug',
    name: 'Histories',
    component: Histories,
    props: true 
  },
  {
    path: '/user/history/',
    name: 'History',
    component: History,
    props: true 
  },
  {
    path: '/account/checklive',
    name: 'CheckLive',
    component: CheckLive,
    props: true 
  }
  ,
  {
    path: '/user/history-transaction',
    name: 'HistoryTransaction',
    component: HistoryTransaction,
    props: true 
  },
  {
    path: '/user/history-transaction/:page_slug',
    name: 'HistoryTransactions',
    component: HistoryTransactions,
    props: true 
  },
  {
    path: '/:pathMatch(.*)*',
    name: "PageNotFound",
    component: PageNotFound,
  },
  {
    path: '/admin',
    name: 'Dashboard',
    component: Dashboard,
    props: true,
    meta:{
      is_admin : true
    }
  },
  ,
  {
    path: '/admin/accounts',
    name: 'Account',
    component: Account,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/accounts/:page_slug',
    name: 'Accounts',
    component: Accounts,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/account/add-account',
    name: 'AddAccount',
    component: AddAccount,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/categories',
    name: 'Category',
    component: Category,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/categories/:page_slug',
    name: 'Categories',
    component: Categories,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/category/add-category',
    name: 'AddCategory',
    component: AddCategory,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/account/account-detail/:id_slug',
    name: 'AccountDetail',
    component: AccountDetail,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/category/category-detail/:id_slug',
    name: 'CategoryDetail',
    component: CategoryDetail,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/users',
    name: 'User',
    component: User,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/users/:page_slug',
    name: 'Users',
    component: Users,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/user/add-user',
    name: 'CreateUser',
    component: CreateUser,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/user/user-detail/:id_slug',
    name: 'UserDetail',
    component: UserDetail,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/transactions',
    name: 'Transaction',
    component: Transaction,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/transactions/:page_slug',
    name: 'Transactions',
    component: Transactions,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/orders',
    name: 'Order',
    component: Order,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/orders/:page_slug',
    name: 'Orders',
    component: Orders,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/order-detail/:id/:page',
    name: 'OrderDetail',
    component: OrderDetail,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/account/search/:query/:page',
    name: 'AccountSearch',
    component: AccountSearch,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/order/search/:query/:page',
    name: 'OrderSearch',
    component: OrderSearch,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/transaction/search/:query/:page',
    name: 'TransactionSearch',
    component: TransactionSearch,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/category/search/:query/:page',
    name: 'CategorySearch',
    component: CategorySearch,
    props: true,
    meta:{
      is_admin : true
    }
  },
  {
    path: '/admin/users/search/:query/:page',
    name: 'UserSearch',
    component: UserSearch,
    props: true,
    meta:{
      is_admin : true
    }
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})     
const unAuthenticatedAndPrivatePage = (path) => (!PUBLIC_PATHS.includes(path)
    && !(ACCESS_TOKEN in window.localStorage)
    && !(REFRESH_TOKEN in window.localStorage));

router.beforeEach((to, from, next) => {
  if (unAuthenticatedAndPrivatePage(to.path)) {
    next(`/login?next=${to.path}`);
  } 
  else {
    if(to.matched.some(record => record.meta.is_admin)) {
      if(store.state.isAdmin == true){
          next()
        }
      else{
          next({ name: 'PageNotFound'})
        }
    }
    next()
}});

export default router;
