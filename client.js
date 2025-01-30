displayView = function(){
    // the code required to display a view
};

window.onload = function(){
//code that is executed as the page is loaded.
//You shall put your own custom code here.
//window.alert() is not allowed to be used in your implementation.

let welcomeView = document.getElementById("welcomeview");
let profileView = document.getElementById("profileview");
let nowview = welcomeView;
document.getElementById("view").innerHTML += nowview.innerHTML;
// window.alert("Hello TDDD97!");
};

function login_validate(form){
    let login = {
        email : form.email.value,
        password : form.password.value,
    }
    let return_info =serverstub.signIn(login.email, login.password);
    if(return_info.success){
        nowview = document.getElementById("profileview");
    }else{
        nowview = document.getElementById("welcomeview");
    }
    document.getElementById("view").innerHTML = nowview.innerHTML;
    
    let errorMessageElement = document.getElementById("login_error_message");
    if (errorMessageElement) {
        errorMessageElement.textContent = return_info.message;
    }
}


function matchPassword() {
    let psw = document.getElementById("password_signup").value;
    let rePsw = document.getElementById("repeatPSW").value;
    if (psw != rePsw) {
        return false;
    }
    return true;
};

function minLengthPassword() {
    let psw = document.getElementById("password_signup").value;
    let rePsw = document.getElementById("repeatPSW").value;    

    if (psw.length < 8 || rePsw.length < 8) {
        return false;
    }
    return true;
}

function validate() {
    let errorMsg = document.getElementById("error_message");
    
    if (!matchPassword()) {
        errorMsg.textContent = "Your passwords must be the same.";
        return false;
    }
    if (!minLengthPassword()) {
        errorMsg.textContent = "Password should be at least 8 characters.";
        return false;
    }
    errorMsg.textContent = "";
    signUp(document.getElementById("signupform"))
    return true;
    
};

function signUp(form){
    let profile = {
        email : form.email_signup.value,
        password : form.password_signup.value,
        firstname : form.firstname.value,
        familyname :form.familyname.value,
        gender :form.gender.value,
        city :form.city.value,
        country :form.country.value,
    }
    let return_info =serverstub.signUp(profile);

    if(return_info.success.valueOf()){
        nowview = document.getElementById("profileview");
    }else{
        nowview = document.getElementById("welcomeview");
    }
    document.getElementById("view").innerHTML = nowview.innerHTML;

    let errorMessageElement = document.getElementById("error_message");
    if (errorMessageElement) {
        errorMessageElement.textContent = return_info.message;
    }
}
    