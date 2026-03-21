const API_URL="http://127.0.0.1:8000"

function apiFetch(endpoint){

const token=localStorage.getItem("token")

return fetch(API_URL+endpoint,{

headers:{
"Authorization":"Bearer "+token
}

})

}