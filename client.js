displayView = function(){
    // the code required to display a view
};

window.onload = function(){
//code that is executed as the page is loaded.
//You shall put your own custom code here.
//window.alert() is not allowed to be used in your implementation.

let welcomeView = document.getElementById("welcomeview");
document.getElementById("view").innerHTML += welcomeView.innerHTML;
// window.alert("Hello TDDD97!");
};

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
    return true;
    
};