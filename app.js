var myFile = $('#fileinput').prop('files');

// FUNCTIONS:

// Submit button
function submit() {
    alert("Submit button clicked!");
    var submitted = true;
    return true;
}

// Hidden element
function hide() {
    var x = document.getElementById("hidden");
    if (submitted === true) {
        x.style.display = "none";
    } else {
        x.style.display = "inline";
    }
}
