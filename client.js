displayView = function(){
    // the code required to display a view
};


window.onload = function(){
//code that is executed as the page is loaded.
//You shall put your own custom code here.
//window.alert() is not allowed to be used in your implementation.
let token = localStorage.getItem("token");
let nowview;
let first_time = true;
if (token) {
    nowview = document.getElementById("profileview");
} else {
    nowview = document.getElementById("welcomeview");
}
document.getElementById("view").innerHTML += nowview.innerHTML;
if(first_time){
    get_homedata();
    first_time =  false;
}
// window.alert("Hello TDDD97!");
};

function login_validate(form){
    let login = {
        email : form.email.value,
        password : form.password.value,
    }
    let return_info =serverstub.signIn(login.email, login.password);
    if(return_info.success){
        localStorage.setItem("token", return_info.data.valueOf());
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

function signout_validate() {
    try {
    let token = localStorage.getItem("token");
    let return_info = serverstub.signOut(token);

        if (return_info.success) {
            localStorage.removeItem("token");
            nowview = document.getElementById("welcomeview");
            document.getElementById("view").innerHTML = nowview.innerHTML;
        }
        else {
            let errorMessageElement = document.getElementById("signout_error");
            if (errorMessageElement) {
                errorMessageElement.textContent = return_info.message;
            }
        }
    }
    catch(e) {
        console.error("error");
    }
}

function tryChangePassword(form) {
    let token = localStorage.getItem("token");
    let currentPsw = form.currentpsw.value;
    let newPsw = form.changepsw.value;
    let repeatNewPsw = form.repeatchangepsw.value;
    let errorMsg = document.getElementById("changepsw_error");

    if (!matchPassword(newPsw, repeatNewPsw)) {
        errorMsg.textContent = "Your passwords must be the same.";
        return false;
    }

    let return_info = serverstub.changePassword(token, currentPsw, newPsw);
    errorMsg.textContent = return_info.message;
    if (!return_info.success.valueOf()) {
        return false;
    } else {
        return true;
    }
}

function matchPassword(psw, rePsw) {
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
    let password_signup = document.getElementById("password_signup").value;
    let repeatPsw = document.getElementById("repeatPSW").value;
    
    if (!matchPassword(password_signup, repeatPsw)) {
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

function trySearchUser(form) {
    let searchEmail = form.useremail.value;
    let token = localStorage.getItem("token");
    let errorMsg = document.getElementById("search_error");
    let messageContainer = document.getElementById("message_container");
    messageContainer.innerHTML = "";
    let return_info = serverstub.getUserDataByEmail(token, searchEmail);
    if (return_info.success.valueOf()) {
        document.getElementById("search_email_info").innerText = return_info.data.email;
        document.getElementById("search_firstname_info").innerText = return_info.data.firstname;
        document.getElementById("search_familyname_info").innerText = return_info.data.familyname;
        document.getElementById("search_gender_info").innerText = return_info.data.gender;
        document.getElementById("search_city_info").innerText = return_info.data.city;
        document.getElementById("search_country_info").innerText = return_info.data.country;

        loadMessage("message_container", return_info.data.email);

        let searchUserInfo = document.getElementById("searchuserinfo");
        if (!searchUserInfo.classList.contains("on")) {
            searchUserInfo.classList.add("on");
        }
    } else {
        errorMsg.textContent = return_info.message;
        let searchUserInfo = document.getElementById("searchuserinfo");
        if (searchUserInfo.classList.contains("on")) {
            searchUserInfo.classList.remove("on");
        }        
        return false;
    }
    errorMsg.textContent = "";
    return true;
}

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
        let return_info =serverstub.signIn(profile.email, profile.password);
        if (return_info.success.valueOf()) {
            localStorage.setItem("token", return_info.data.valueOf());
            nowview = document.getElementById("profileview");
        }
        else {
            nowview = document.getElementById("welcomeview");
        }
    }else{
        nowview = document.getElementById("welcomeview");
    }
    document.getElementById("view").innerHTML = nowview.innerHTML;

    let errorMessageElement = document.getElementById("error_message");
    if (errorMessageElement) {
        errorMessageElement.textContent = return_info.message;
    }
}


function get_homedata(){
    let token = localStorage.getItem("token");
    homedata = serverstub.getUserDataByToken(token);
    document.getElementById("email_info").innerText = homedata.data.email;
    document.getElementById("firstname_info").innerText = homedata.data.firstname;
    document.getElementById("familyname_info").innerText = homedata.data.familyname;
    document.getElementById("gender_info").innerText = homedata.data.gender;
    document.getElementById("city_info").innerText = homedata.data.city;
    document.getElementById("country_info").innerText = homedata.data.country;

    loadMessage("message_container_home", homedata.data.email);
}


function openTab(tabId) {
    let allTab = document.querySelectorAll('.tab_button, .tab_page');
    allTab.forEach(function(element) {
        element.classList.remove('on');
    });

    let onButton = document.getElementById(tabId);
    onButton.classList.add('on');

    let onTab = document.getElementById(tabId + '_tab');
    onTab.classList.add('on');

    if (tabId === "browse") {
        let searchUserInfo = document.getElementById("searchuserinfo");
        if (searchUserInfo.classList.contains("on")) {
            searchUserInfo.classList.remove("on");
        }  
        
        let errorMsg = document.getElementById("search_error");
        errorMsg.textContent = "";        
    }
}

function tryPostMessage(form){
    let text = form.post_msg_content.value;
    let token = localStorage.getItem("token");
    let return_info =serverstub.postMessage(token, text, null);
    let errorMessageElement = document.getElementById("post_error_message");
    errorMessageElement.textContent = return_info.message;
}

function tryPostMessageToOther(form) {
    let text = form.post_msg_content_to_other.value;
    let token = localStorage.getItem("token");
    let email = document.getElementById("search_email_info").textContent;
    let return_info = serverstub.postMessage(token, text, email);
    let errorMessageElement = document.getElementById("post_error_message_to_other");
    errorMessageElement.textContent = return_info.message;
    form.post_msg_content_to_other.value = "";
}

function loadMessage(message_container, email) {
    let messageContainer = document.getElementById(message_container);
    let token = localStorage.getItem("token");
    let return_info = serverstub.getUserMessagesByEmail(token, email);

    if (return_info.data) {
        return_info.data.forEach(e => {
            let newMsg = '<div>' + e.writer + ': ' + e.content + '</div>';
            messageContainer.innerHTML += newMsg;
        });
    }
}