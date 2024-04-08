let password_validation_one = false;
let password_validation_two = false;
let password_validation_three = false;
let password_validation_four = false;



// PASSWORD VALIDATION RULES
document.getElementById("signUpPassword").addEventListener("keyup",function(){
    var current_key = this.value;
    
    // Check if the password contains at least 8 character
    if (current_key.length >= 8) {
        document.getElementById("v1").style = "color:green";
        // FOR CHANGE ICON
        var element = document.getElementById('iv1'); // GET ELEMENT
        // Replace the class
        element.classList.remove('fa-circle-xmark'); // Remove old class
        element.classList.add('fa-circle-check');    // Add new class
        element.style = "color:green";
        password_validation_one = true;
    }else{
        document.getElementById("v1").style = "color:red";
        // Get the element
        var element = document.getElementById('iv1');
        // Replace the class
        element.classList.remove('fa-circle-check'); // Add new class
        element.classList.add('fa-circle-xmark'); // Remove old class
        element.style = "color:red";
        password_validation_one = false;
    }

    // Password contains at least one numeric and one special character
    var numericCharacters = /\d/;
    var specialCharacters = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/;
    if (numericCharacters.test(current_key) && specialCharacters.test(current_key)) {
        document.getElementById("v2").style = "color:green";
        
        // FOR CHANGE ICON
        var element = document.getElementById('iv2'); // GET ELEMENT
        // Replace the class
        element.classList.remove('fa-circle-xmark'); // Remove old class
        element.classList.add('fa-circle-check');    // Add new class
        element.style = "color:green";
        password_validation_two = true;
    }else{
        document.getElementById("v2").style = "color:red";
        // Get the element
        var element = document.getElementById('iv2');
        // Replace the class
        element.classList.remove('fa-circle-check'); // Add new class
        element.classList.add('fa-circle-xmark'); // Remove old class
        element.style = "color:red";
        password_validation_two = false;
    }

    // Check if the password contains lowercase and uppercase letters
    var uppercaseCharacters = /[A-Z]/;
    var lowercaseCharacters = /[a-z]/;
    if (uppercaseCharacters.test(current_key) && lowercaseCharacters.test(current_key)) {
        document.getElementById("v3").style = "color:green";
        // FOR CHANGE ICON
        var element = document.getElementById('iv3'); // GET ELEMENT
        // Replace the class
        element.classList.remove('fa-circle-xmark'); // Remove old class
        element.classList.add('fa-circle-check');    // Add new class
        element.style = "color:green";
        password_validation_three = true;
    }else{
        document.getElementById("v3").style = "color:red";
        // Get the element
        var element = document.getElementById('iv3');
        // Replace the class
        element.classList.remove('fa-circle-check'); // Add new class
        element.classList.add('fa-circle-xmark'); // Remove old class
        element.style = "color:red";
        password_validation_three= false;
    }
 
});


//  FOR TOGGLE HIDE AND SHOW password IN SIGN UP -- PASSWORD
const VisibilityToggle_2 = document.querySelector('.Visibility-2');
const input_2 = document.getElementById("signUpPassword");
var password_2 = true;
VisibilityToggle_2.addEventListener("click",function(){
    if (password_2) {
        input_2.setAttribute('type','text')
        VisibilityToggle_2.classList.remove('fa-eye-slashe'); 
        VisibilityToggle_2.classList.add('fa-eye'); 
    } else {
        input_2.setAttribute('type','password')
        VisibilityToggle_2.classList.remove('fa-eye'); 
        VisibilityToggle_2.classList.add('fa-eye-slashe'); 
    }
    password_2 = !password_2;
});

//  FOR TOGGLE HIDE AND SHOW Confirm_password IN SIGN UP -- CONFIRM PASSWORD
const VisibilityToggle_3 = document.querySelector('.Visibility-3');
const input_3 = document.getElementById("signUpConfirmPassword");
var password_3 = true;
VisibilityToggle_3.addEventListener("click",function(){
    if (password_3) {
        input_3.setAttribute('type','text')
        VisibilityToggle_3.classList.remove('fa-eye-slashe'); 
        VisibilityToggle_3.classList.add('fa-eye'); 
    } else {
        input_3.setAttribute('type','password')
        VisibilityToggle_3.classList.remove('fa-eye'); 
        VisibilityToggle_3.classList.add('fa-eye-slashe'); 
    }
    password_3 = !password_3;
});

document.getElementById('signUpConfirmPassword').addEventListener("keyup", function(){
    let newPassword = document.getElementById("signUpPassword");
    password_validation_four = this.value != newPassword.value ? false : true;
    
    if (password_validation_one && password_validation_two && password_validation_three && password_validation_four) {
        this.style = "border: 1px solid green";
        newPassword.style = "border: 1px solid green";
    }else{
        newPassword.style = "border: 1px solid red";
        this.style = "border: 1px solid red";
    }
})



document.getElementById('update_user_password').addEventListener("submit",function(event){
    var new_pass = document.getElementById("signUpPassword").value;
    var cnf_pass = document.getElementById("signUpConfirmPassword").value;
    
    if (!(password_validation_one && password_validation_two && password_validation_three && password_validation_four)) {
        event.preventDefault();
        // Alert if password roole is not follow
        document.getElementById("error_message").innerHTML = "Please follow the password rule";
    }

    if(new_pass!= cnf_pass){
        event.preventDefault();
        document.getElementById("error_message").innerHTML = "New password and confirm password not match.";
    }
});




