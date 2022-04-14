function zanatlijaReg() {
    var checkBox = document.getElementById("btn-check-2-outlined");
    var form = document.getElementsByClassName("formaZanatlije");
    for (var i = 0; i < form.length; i++) {
        if (checkBox.checked == true) {
            form[i].style.display = "inline-block";
        } else {
            form[i].style.display = "none";
        }
    }


    if (checkBox.checked == true) {
        document.getElementById('formaZanatlije').style.display = "block";
    } else {
        document.getElementById('formaZanatlije').style.display = "none";
    }
}

function onChange(id) {
    var elem = document.getElementById(id);
    if (elem.value == "Dodaj") {
        elem.value = "Ukloni";
        elem.innerHTML = "Ukloni";
    } else {
        elem.value = "Dodaj";
        elem.innerHTML = "Dodaj";
    }
}