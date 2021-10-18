import { paymentRequest } from './auth';

const payment = (category,user,quantity) => {
  const formData = new FormData();
  formData.append("category", category);
  formData.append("user", user);
  formData.append("quantity", quantity);
    return paymentRequest.post('/api/v1/payment/',formData)
      .then((response) => Promise.resolve(response.data))
      .catch((error) => Promise.reject(error));
  };
  
  export { payment }; 
  