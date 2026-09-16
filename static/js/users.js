import helper from "./helper.js";

export class Users {

  constructor() {
    const auth_headers = {
      "USER-ID": localStorage.getItem('USER_ID'),
      "USER-NAME": localStorage.getItem('USER_NAME'),
      'Content-Type': 'application/json'
    }
  }

  // user login
  async login() {
    try {
      const username = document.getElementById("login-username").value.trim();
      const password = document.getElementById("login-password").value.trim();

      if (!username || !password) {
        let errorMsg = 'Please enter both username and password.'
        helper.showNotification(errorMsg, 'error');
        return;
      }
      console.log('11111111')

      const response = await fetch('/users/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      const result = await response.json();
      if (response && response.status == 200) {
        helper.showNotification(result.message, 'success');
        localStorage.setItem('USER_EMAIL', result.data.USER_EMAIL);
        localStorage.setItem('USER_ID', result.data.USER_ID);
        localStorage.setItem('USER_LOC_LAT', result.data.USER_LOC_LAT);
        localStorage.setItem('USER_NAME', result.data.USER_NAME);
        localStorage.setItem('USER_TYPE', result.data.USER_TYPE);
        localStorage.setItem('USER_ADDRESS', result.data.USER_ADDRESS);
        window.location.href = 'home'
      } else {
        console.log(result)
        if(result.error){
          helper.showNotification(result.error, 'error');
        } else {
          helper.showNotification(result.message,'error')
        }
      }

    } catch (error) {
      console.log(error);
      helper.showNotification(error, 'error');
    }
  }

  // user register
  async register(params) {
    try {
      // const username = document.getElementById('reg_username').value.trim();
      // const password = document.getElementById('reg_password').value.trim();
      // const email = document.getElementById('reg_email').value.trim();
      let errorMsg = null
      if (!params.email) {
        errorMsg = "Please enter emailID";
      }
      if (!params.username) {
        errorMsg = "Please enter username";
      }
      if (!params.password) {
        errorMsg = "Please enter Password";
      }
      if (errorMsg) {
        helper.showNotification(errorMsg, 'error')
      }
      console.log(params)
      let doesExists = await this.checkUsername(params.userName);
      console.log(doesExists)
      if(doesExists.data != {}){
        helper.showNotification("Username already exists", 'error');
      }
      const response = await fetch('/users/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify(params)
      })
      const result = await response.json()
      if (response && response.status == 200) {
        helper.showNotification(result.message, 'success');
        window.location.href = '/'
      } else {
        helper.showNotification(result.error, 'error');
      }
    } catch (error) {
      console.log(error);
      helper.showNotification(error, 'error')
    }
  }

  async checkUsername(username) {
    try {
      if (!username) {
        let errorMsg = 'Please enter valid username'
        helper.showNotification(errorMsg, 'error');
        return;
      }
      console.log('username: ', username)
      const response = await fetch(`/users/name/${username}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json', USER_NAME: username },
      });
      const result = await response.json();
      console.log('result: ', result)
      if (response && response.status == 200) {
        return response
      } else {
        helper.showNotification('User Doest Exists', 'error')
        return {
          status: 500,
          error: "Internal Server Error"
        }
      }
    } catch (error) {
      console.log(error);
      helper.showNotification(error, 'error')
    }
  }

  async resetPassword(params) {
    try {
      if (!params.username || !params.newPassword) {
        const message = 'Enter a valid Username or Password'
        helper.showNotification(message, 'error');
        return;
      }
      const response = await fetch('/users/resetPassword', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: params.username, password: params.newPassword })
      });

      const data = await response.json();
      if (response && response.status == 200) {
        helper.showNotification('Password Reset Successful', 'success');
        return true;
      } else {
        helper.showNotification('Error resetting password', 'error')
      }

    } catch (error) {
      console.log(error)
      helper.showNotification(error);
    }
  }
}