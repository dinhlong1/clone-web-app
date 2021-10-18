import { authRequest } from './auth';

const myUser = () => {
  return authRequest.get('/api/v1/users/me/')
    .then((response) => Promise.resolve(response.data))
    .catch((error) => Promise.reject(error));
};

const SetPassword = (new_password,current_password) => {
  const formData= {
    'new_password': new_password,
    'current_password': current_password
  }
  return authRequest.post('/api/v1/users/set_password/', formData)
    .then((response) => Promise.resolve(response.data))
    .catch((error) => Promise.reject(error));
};
export { myUser ,SetPassword}; 