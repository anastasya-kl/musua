import axios from 'axios';


axios.post('http://127.0.0.1:5000/api/sign_up_user/', {
    "nickname" : "rock_2024",
    "password" : "password",
    "email" : "email4@gmail.com"
  })
  .then((response) => {
    console.log(response);
  }, (error) => {
    console.log(error);
  });
