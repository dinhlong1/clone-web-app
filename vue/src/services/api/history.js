import { authRequest } from './auth';

const changPage = (url) => {
  return authRequest.get(url)
  .then((response) =>Promise.resolve(response.data))
  .catch((error) => Promise.reject(error))
}

const historyOrders = () => {
    return authRequest.get('/api/v1/history/')
      .then((response) => Promise.resolve(response.data))
      .catch((error) => Promise.reject(error));
  };
const getDetail = (order) => {
    const formData = new FormData();
    formData.append("order", order);
    return authRequest.post('/api/v1/history/detail/', formData)
      .then((response) => Promise.resolve(response.data))
      .catch((error) => Promise.reject(error));
  };
  
const historyTransactions = () => {
    return authRequest.get('/api/v1/history-transaction/')
      .then((response) => Promise.resolve(response.data))
      .catch((error) => Promise.reject(error));
  };
export { historyOrders ,historyTransactions , changPage,getDetail}; 


  