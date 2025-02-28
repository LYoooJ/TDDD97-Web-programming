displayView = function(){
    // the code required to display a view
    let token = localStorage.getItem("token");
    let nowview;
    //change view depending on token
    if (token) {
        nowview = document.getElementById("profileview");
    } else {
        nowview = document.getElementById("welcomeview");
    }
    document.getElementById("view").innerHTML = nowview.innerHTML;
};

let first_time = true;

window.onload = function(){
//code that is executed as the page is loaded.
//You shall put your own custom code here.
//window.alert() is not allowed to be used in your implementation.
let token = localStorage.getItem("token");
let nowview;
//change view depending on token
if (token) {
    nowview = document.getElementById("profileview");
} else {
    nowview = document.getElementById("welcomeview");
}
document.getElementById("view").innerHTML = nowview.innerHTML;

//only reload one time
if(token && first_time){
    get_homedata();
    first_time =  false;
}
};

function start_socket() {
    let socket = new WebSocket("ws://" + location.host + "/connect")

    socket.onopen = function(event) {
        // console.log("Websocket connection");
        token = localStorage.getItem('token');
        if (token) {
            socket.send(token);
        }
    }

    socket.onmessage = function(event) {
        // console.log("Event!!");
        // console.log(event.data);
        if (event.data == 'user logout') {
            // console.log("Log out!!!!!");
            localStorage.removeItem('token');
            displayView();
        }
    }

    socket.onclose = function(event) {
        console.log("Websocket connection closed! ");
    };
}

function get_homedata(){
    let token = localStorage.getItem("token");

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_user_data_by_token', true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8"); 
    xhr.setRequestHeader("Authorization", token);
    xhr.send();

    xhr.onreadystatechange = function() {
        if (xhr.readyState == xhr.DONE) {
            let return_info = JSON.parse(xhr.responseText);
            if (return_info.success) {
                document.getElementById("email_info").innerText = return_info.data[0];
                document.getElementById("firstname_info").innerText = return_info.data[1];
                document.getElementById("familyname_info").innerText = return_info.data[2];
                document.getElementById("gender_info").innerText = return_info.data[3];
                document.getElementById("city_info").innerText = return_info.data[4];
                document.getElementById("country_info").innerText = return_info.data[5];

                loadMessage("message_container_home", return_info.data[0]);
            }
        }
    }
}

function signUp(form){
    try {
        let profile = {
            'email' : form.email_signup.value,
            'password' : form.password_signup.value,
            'firstname' : form.firstname.value,
            'familyname' :form.familyname.value,
            'gender' :form.gender.value,
            'city' :form.city.value,
            'country' :form.country.value,
        }
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/sign_up', true);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8"); 
        xhr.send(JSON.stringify(profile));
    
        xhr.onreadystatechange = function() {
            if (xhr.readyState == xhr.DONE) {
                let return_info = JSON.parse(xhr.responseText);
                if (return_info.success) {
                    nowview = document.getElementById("profileview");                
                }   
                else {
                    nowview = document.getElementById("welcomeview");
                }
    
                sign_in(form.email_signup.value, form.password_signup.value);
                document.getElementById("view").innerHTML = nowview.innerHTML;
                get_homedata();
    
                let errorMessageElement = document.getElementById("error_message");
                if (errorMessageElement) {
                    errorMessageElement.textContent = return_info.message;
                }
            }
        }
    }
    catch(e) {
        console.log(e);
    }

}

function sign_in(email, password) {
    try {
        let login = {
            'username' : email,
            'password' : password,
        }
    
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/sign_in', true);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8"); 
        xhr.send(JSON.stringify(login));
        
        xhr.onreadystatechange = function() {
            if (xhr.readyState == xhr.DONE) {
                let return_info = JSON.parse(xhr.responseText);
                if (return_info.success) {
                    localStorage.setItem("token", return_info.data);
                    nowview = document.getElementById("profileview");    
                    start_socket();            
                }   
                else {
                    nowview = document.getElementById("welcomeview");
                }
                document.getElementById("view").innerHTML = nowview.innerHTML;
                if (return_info.success)
                    get_homedata();
    
                let errorMessageElement = document.getElementById("login_error_message");
                if (errorMessageElement) {
                    errorMessageElement.textContent = return_info.message;
                }
            }
        }
    }
    catch(e) {
        console.log(e);
    }
}

function login_validate(form){
    sign_in(form.email.value, form.password.value);
}

function signout_validate() {
    let token = localStorage.getItem("token");

    var xhr = new XMLHttpRequest();
    xhr.open('DELETE', '/sign_out', true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8"); 
    xhr.setRequestHeader("Authorization", token);
    xhr.send();

    xhr.onreadystatechange = function() {
        if (xhr.readyState == xhr.DONE) {
            let return_info = JSON.parse(xhr.responseText);
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

    if (!minLengthPassword(newPsw, repeatNewPsw)) {
        errorMsg.textContent = "should be at least 8 characters.";
        return false;
    }

    let data = {
        'oldpassword': currentPsw,
        'newpassword': newPsw
    }
    var xhr = new XMLHttpRequest();
    xhr.open('PUT', '/change_password', true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8"); 
    xhr.setRequestHeader("Authorization", token);
    xhr.send(JSON.stringify(data));

    xhr.onreadystatechange = function() {
        if (xhr.readyState == xhr.DONE) {
            let return_info = JSON.parse(xhr.responseText);
            errorMsg.textContent = return_info.message;
        }
    }
}

function matchPassword(psw, rePsw) {
    if (psw != rePsw) {
        return false;
    }
    return true;
};

function minLengthPassword(psw, rePsw) {
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
    if (!minLengthPassword(password_signup, repeatPsw)) {
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

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_user_data_by_email/' + encodeURIComponent(searchEmail), true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8"); 
    xhr.setRequestHeader("Authorization", token);
    xhr.send();

    xhr.onreadystatechange = function() {
        if (xhr.readyState == xhr.DONE) {
            let return_info = JSON.parse(xhr.responseText);
            if (return_info.success) {
                document.getElementById("search_email_info").innerText = return_info.data[0];
                document.getElementById("search_firstname_info").innerText = return_info.data[1]
                document.getElementById("search_familyname_info").innerText = return_info.data[2];
                document.getElementById("search_gender_info").innerText = return_info.data[3];
                document.getElementById("search_city_info").innerText = return_info.data[4];
                document.getElementById("search_country_info").innerText = return_info.data[5];
            
                loadMessage("message_container", return_info.data[0]);
    
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
        } 
    }   
    errorMsg.textContent = "";
    return true;
}

function msgRenew(tabId) {
    if (tabId === "home") {
        loadMessage("message_container_home", document.getElementById("email_info").innerText);
    }
    else if (tabId === "browse") {
        loadMessage("message_container", document.getElementById("search_email_info").innerText);
    }
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
    try{
        let text = form.post_msg_content.value;
        let token = localStorage.getItem("token");
        let email = document.getElementById('email_info').textContent;
        let errorMessageElement = document.getElementById("post_error_message");
    
        let post = {
            'email': email,
            'message': text,
        }
    
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/post_message', true);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8"); 
        xhr.setRequestHeader("Authorization", token);
        xhr.send(JSON.stringify(post));   
        
        xhr.onreadystatechange = function() {
            if (xhr.readyState == xhr.DONE) {
                let return_info = JSON.parse(xhr.responseText);
                if (xhr.status === 201) {
                    errorMessageElement.textContent = "Message Posted";
                } else if(xhr.status === 401) {
                    errorMessageElement.textContent = "You are not signed in";
                } else {
                    errorMessageElement.textContent = "No such User";
                }
            }
        }    
        form.post_msg_content.value = "";
    }
    catch(e) {
        console.log(e);
    }
}

function tryPostMessageToOther(form) {
    try{
        let text = form.post_msg_content_to_other.value;
        let token = localStorage.getItem("token");
        let errorMessageElement = document.getElementById("post_error_message_to_other");
        let email = document.getElementById("search_email_info").textContent;
    
        let post = {
            "email": email,
            "message": text
        }

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/post_message', true);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8"); 
        xhr.setRequestHeader("Authorization", token);
        xhr.send(JSON.stringify(post));  
    
        xhr.onreadystatechange = function() {
            if (xhr.readyState == xhr.DONE) {
                let return_info = JSON.parse(xhr.responseText);
                if (xhr.status === 201) {
                    errorMessageElement.textContent = "Message Posted";
                } else if(xhr.status === 401) {
                    errorMessageElement.textContent = "You are not signed in";
                } else {
                    errorMessageElement.textContent = "No such User";
                }
            }
        }    
        form.post_msg_content_to_other.value = "";
    }
    catch(e) {
        console.log(e);
    }
}

function loadMessage(message_container, email) {
    let messageContainer = document.getElementById(message_container);
    let token = localStorage.getItem("token");

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_user_messages_by_email/' + email, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8"); 
    xhr.setRequestHeader("Authorization", token);
    xhr.send();  

    xhr.onreadystatechange = function() {
        if (xhr.readyState === xhr.DONE) {
            let return_info = JSON.parse(xhr.responseText);
            messageContainer.innerHTML = [];
            if (return_info.data) {
                return_info.data.forEach(e => {
                    let newMsg = '<div>' + e[0] + ': ' + e[2] + '</div>';
                    messageContainer.innerHTML += newMsg;
                });
            }
        }
    }         
}