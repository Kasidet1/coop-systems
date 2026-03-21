const response=await fetch("http://127.0.0.1:8000/auth/login",{

method:"POST",

headers:{
"Content-Type":"application/x-www-form-urlencoded"
},

body:new URLSearchParams({
username:username,
password:password
})

})