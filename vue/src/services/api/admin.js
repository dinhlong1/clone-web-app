import { authRequest } from './auth';

// Dashboard
const getDataDashboard = () =>{
  return authRequest.post('/api/v1/dashboard/')
    .then((response) => Promise.resolve(response.data))
    .catch((error) => Promise.reject(error));
}

// Account
const getAccounts = () => {
  return authRequest.get('/api/v1/accounts/')
    .then((response) => Promise.resolve(response.data))
    .catch((error) => Promise.reject(error));
}

const addAccount = (category,data,params) =>{
    const formData = new FormData();
    formData.append("category", category);
    formData.append("data", data);
    formData.append("params", params);

    return authRequest.post('/api/v1/account/',formData)
    .then((response) => Promise.resolve(response.data))
    .catch((error) => Promise.reject(error));
}

const changePage = (url) => {
  return authRequest.get(url)
  .then((response) =>Promise.resolve(response.data))
  .catch((error) => Promise.reject(error))
}

const deleteAccount = (id) => {
    const formData = new FormData();
    formData.append("id", id);
    console.log(formData["id"])
    return authRequest.post('/api/v1/account/delete/',formData)
    .then((response) => Promise.resolve(response.data))
    .catch((error) => Promise.reject(error));
}
const changeAccount = (id,password,auth,email,password_email,token,cookie,statusUser,sold) =>{
  const formData = new FormData();
    formData.append("id", id);
    formData.append("password", password);
    formData.append("auth", auth);
    formData.append("email", email);
    formData.append("password_email", password_email);
    formData.append("token", token);
    formData.append("cookie", cookie);
    formData.append("status", statusUser);
    formData.append("sold", sold);
    console.log(formData);
    return authRequest.put('/api/v1/account/',formData)
    .then((response) => Promise.resolve(response.data))
    .catch((error) => Promise.reject(error));
}


// Category
const getCategories = () => {
  return authRequest.get('/api/v1/categories/')
    .then((response) => Promise.resolve(response.data))
    .catch((error) => Promise.reject(error));
};
const addCategory = (name,price,discount) =>{
  const formData = new FormData();
  formData.append("name", name);
  formData.append("price", price);
  formData.append("discount", discount);

  return authRequest.post('/api/v1/category/',formData)
  .then((response) => Promise.resolve(response.data))
  .catch((error) => Promise.reject(error));
}

const deleteCategory = (id) => {
const formData = new FormData();
formData.append("id", id);
return authRequest.post("/api/v1/category/delete/",formData)
.then((response) =>Promise.resolve(response.data))
.catch((error) => Promise.reject(error))
}
const changeCategory = (id,name,price,discount) =>{
const formData = new FormData();
  formData.append("id", id);
  formData.append("name", name);
  formData.append("price", price);
  formData.append("discount", discount);

  return authRequest.put('/api/v1/category/',formData)
  .then((response) => Promise.resolve(response.data))
  .catch((error) => Promise.reject(error));
}


// Users
const getUsers = () => {
  return authRequest.get('/api/v1/user/list/')
    .then((response) => Promise.resolve(response.data))
    .catch((error) => Promise.reject(error));
};
const addUser = (email,password) =>{
  const formData = new FormData();
  formData.append("email", email);
  formData.append("password", password);
  return authRequest.post('/api/v1/user/',formData)
  .then((response) => Promise.resolve(response.data))
  .catch((error) => Promise.reject(error));
}

const deleteUser = (id) => {
const formData = new FormData();
formData.append("id", id);
return authRequest.post("/api/v1/user/delete/",formData)
.then((response) =>Promise.resolve(response.data))
.catch((error) => Promise.reject(error))
}
const changeUser = (id,email,coin) =>{
const formData = new FormData();
  formData.append("id", id);
  formData.append("email",email);
  formData.append("coin", coin);

  return authRequest.put('/api/v1/user/',formData)
  .then((response) => Promise.resolve(response.data))
  .catch((error) => Promise.reject(error));
}


// Transaction
const getTransactions = () => {
  return authRequest.get('/api/v1/transactions/')
    .then((response) => Promise.resolve(response.data))
    .catch((error) => Promise.reject(error));
};


// Order 
const getOrders = () => {
  return authRequest.get('/api/v1/orders/')
    .then((response) => Promise.resolve(response.data))
    .catch((error) => Promise.reject(error));
};

export { getDataDashboard,getOrders,getTransactions,getUsers,addUser,deleteUser,changeUser,getAccounts,addAccount,changePage,deleteAccount,changeAccount,getCategories,addCategory,deleteCategory,changeCategory }; // 