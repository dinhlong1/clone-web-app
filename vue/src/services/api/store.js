import { authRequest } from './auth';

const store = () => {
  return authRequest.get('/api/v1/store/')
    .then((response) => Promise.resolve(response.data))
    .catch((error) => Promise.reject(error));
};

export { store }; // eslint-disable-line import/prefer-default-export
