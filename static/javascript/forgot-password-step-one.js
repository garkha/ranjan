// TELIPHONE COUNTRY CODE
const username = document.querySelector("#username");
var iti_username = window.intlTelInput(username, {
    // IF I ADD THIS LINK THEN A 1 TAB SPACE IN MIDDLE: 92132 84867 like this
    // utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@19.5.5/build/js/utils.js",
    initialCountry: "in",
    showSelectedDialCode : true,
});
username.addEventListener('change', function() {
    // For country code only
    var country_code = iti_username.getSelectedCountryData().dialCode; // RETURN DIAL CODE
    document.getElementById("country_code").value = country_code;
});