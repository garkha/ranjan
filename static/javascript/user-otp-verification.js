// THIS FUNCTION MOVE NEX TEB/INPUT AFTER ENTER 1 GIGIT IN INPUT BOX
var inputs = document.querySelectorAll('input'); // Get all input fields

inputs.forEach(function(input, index) {
    input.addEventListener('input', function(event) {
        const inputValue = event.target.value;
        if (/^\d$/.test(inputValue)) {
            // If input is a single digit, move to the next input field
            if (index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
        } else {
            // Clear the input field if more than one character is entered
            event.target.value = '';
        }
    });
});


  // Add keyup event listener to each input
// inputs.forEach(function(input, index) {
//     input.addEventListener('keyup', function(event) {
//         // Check if the pressed key is Enter (key code 13)
//         if (index < inputs.length - 1) {
//             inputs[index + 1].focus();
//         }
//         // If it's the last input, focus on the first input (loop)
//         else {
//             document.getElementById("submit").focus();
//         }
//     });
// });

// TIMER TO RESEND OTP
var count = 120;
let id = setInterval(function(){
    count--;
    document.getElementById("timer").innerHTML = "OTP is valid for only " + count + " Second";
    if(count==0){
        clearInterval(id);
        document.getElementById("timer").innerHTML = "Re Send OTP";
        
    }
}, 1000);


// ALERT MESSAGE IF PASSWORD LENGHT NOT EQUAL TO SIX
document.getElementById('otp_code').addEventListener("submit",function(event){
    //ACCESS FORM ALL INPUTS
    const inputElements = this.querySelectorAll('input');
    let otp = "";
    // Iterate over input elements
    inputElements.forEach(function(inputElement) {
        otp += inputElement.value
    });
    
    // CHECK THE LENGHT OF OTP
    if (otp.length != 6) {
        event.preventDefault();
        // Alert if password not 6 digits
        Swal.fire({
            title: 'Error!',
            text: 'OTP length should be 6 digit.',
            icon: 'error',
            confirmButtonText: 'Try again'
        });
    }
    
});