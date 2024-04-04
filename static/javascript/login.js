// CLICK ON SIGN UP BUTTON REDIRECT SIGN UP PAGE 
document.getElementById("SignunBtn").addEventListener("click",function() {
    window.location.href = "/sign-up";
});

// TELIPHONE COUNTRY CODE
const username = document.querySelector("#username");
var iti_username = window.intlTelInput(username, {

    // IF I ADD THIS LINK THEN A 1 TAB SPACE IN MIDDLE: 92132 84867 like this
    // utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@19.5.5/build/js/utils.js",
    initialCountry: "in",
    showSelectedDialCode : true,
    separateDialCode: true,
});
username.addEventListener('change', function() {

    // For full number with country code : +919213284867
    var fullNumber = iti_username.getNumber();

    // For country code only
    var country_code = iti_username.getSelectedCountryData().dialCode; // RETURN DIAL CODE
    document.getElementById("country_code").value = country_code;

    // console.log(country_code); 
    // console.log(fullNumber); // This will log the full number with country code
});


// FOR TOGGLE PASSWORD HIDE AND SHOW in login
const VisibilityToggle = document.querySelector('.Visibility');
const input = document.getElementById("password");
var password = true;
VisibilityToggle.addEventListener("click",function(){
    if (password) {
        input.setAttribute('type','text')
        VisibilityToggle.classList.remove('fa-eye-slashe'); 
        VisibilityToggle.classList.add('fa-eye'); 
    } else {
        input.setAttribute('type','password')
        VisibilityToggle.classList.remove('fa-eye'); 
        VisibilityToggle.classList.add('fa-eye-slashe'); 
    }

    password = !password;
    
});


// ALERT MESSAGE
// ALERT MESSAGE WHEN FORM IS SUBMIT
document.getElementById('login_form').addEventListener("submit",function(event){

    //ACCESS phone or username
    let username = document.getElementById("username");
    let password = document.getElementById("password");
    
    // CHECK THE LENGHT OF phone
    if (username.value.length != 10) {
        event.preventDefault();
        // Alert if password not 6 digits

        Swal.fire({
            title: 'Error!',
            text: `Phone number ${username.value} must be 10 digits.`,
            icon: 'error',
            confirmButtonText: 'Try again'
        });
    }
        

    // CHECK THE phone no can not be blanck
    if (username.value == null) {
        event.preventDefault();
        // Alert if password not 6 digits
        Swal.fire({
            title: 'Error!',
            text: 'Phone number can not be blanck',
            icon: 'error',
            confirmButtonText: 'Try again'
        });
    }

    // CHECK THE password can not be blanck
    if (password.value == null) {
        event.preventDefault();
        // Alert if password not 6 digits
        Swal.fire({
            title: 'Error!',
            text: 'Please Enter the valid password',
            icon: 'error',
            confirmButtonText: 'Try again'
        });
    }
    
      
});