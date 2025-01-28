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