export default function authHeader() {
    const user_token = JSON.parse(localStorage.getItem('user_token'));
    const user_id = JSON.parse(localStorage.getItem('user_id'));
  
    if (user_token && user_id) {
      return { Authorization: 'Bearer ' + user_token };
    } else {
      return {};
    }
  }