// TELIPHONE COUNTRY CODE
const username = document.querySelector("#username");
var iti_username = window.intlTelInput(username, {
    // IF I ADD THIS LINK THEN A 1 TAB SPACE IN MIDDLE: 92132 84867 like this
    // utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@19.5.5/build/js/utils.js",
    initialCountry: "in",
    showSelectedDialCode : true,
});
username.addEventListener('change', function() {
    var fullNumber = iti_username.getNumber();
    this.value = fullNumber;
    console.log(fullNumber); // This will log the full number with country code
});

// ALERT MESSAGE IF MOBILE NUMBER NOT 10 13 DIGIT "+91" 
document.getElementById('forgot_password').addEventListener("submit",function(event){
    //ACCESS FORM ALL INPUTS
    const phone_number = document.getElementById('username').value;
    if (phone_number.length != 13) {
        event.preventDefault();
        // Alert if password not 6 digits
        Swal.fire({
            title: 'Error!',
            text: 'Phone number should be 10 digits for Country code india.',
            icon: 'error',
            confirmButtonText: 'Try again'
        });
    }
});