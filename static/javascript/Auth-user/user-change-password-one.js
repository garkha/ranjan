
// function displayLastFourDigits(mobileNumber) {
//     // Check if the mobile number is valid (at least 4 digits)
//     if (mobileNumber.length >= 4) {
//         // Extract the last four digits
//         var lastFourDigits = mobileNumber.slice(-4);
//         // Create a string with asterisks (*) for the digits preceding the last four digits
//         var maskedNumber = "*".repeat(mobileNumber.length - 4) + lastFourDigits;
//         return maskedNumber;
//     } else {
//         // If the mobile number is less than 4 digits, return it as it is
//         return mobileNumber;
//     }
// }

// const username = displayLastFourDigits("9213284867");
// document.getElementById("username").value = username;