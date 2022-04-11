function zanatlijaReg() {
    var checkBox = document.getElementById("btn-check-2-outlined");
    
    if (checkBox.checked == true){
        document.getElementById('formaZanatlije').style.display = "block";
    } else {
        document.getElementById('formaZanatlije').style.display = "none";
    }
}