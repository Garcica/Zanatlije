function pretraga() {
    if(Array.from(document.getElementsByClassName("tabela"))[0].style.display == "block")
        Array.from(document.getElementsByClassName("tabela"))[0].style.display = "none";
    else
        Array.from(document.getElementsByClassName("tabela"))[0].style.display = "block"
}

function zanatlija()
{
    Array.from(document.getElementsByClassName("zanatlija"))[0].style.display = "block";
}

function potrazioc()
{
    Array.from(document.getElementsByClassName("zanatlija"))[0].style.display = "none";
}
function uncheck()
{
    document.getElementsByName("mestoP")[0].value = "";
    var arr = document.getElementsByName("checkbox");
    for(var cb of arr)
    {
        cb.checked = false;
    }
}

var loged = false;
function login()
{
    loged = true;
    window.location.href = "index.html?log="+loged;
}

function logging()
{
    loged = window.location.href.split("=")[1];
    if(loged == "true")
    {
        Array.from(document.getElementsByClassName("reg"))[0].style.display = "none";
        Array.from(document.getElementsByClassName("ime"))[0].style.display = "inline";
        Array.from(document.getElementsByClassName("admin"))[0].style.display = "inline";
    }
}

function osoba()
{
    window.location.href = "osoba.html?log="+loged;
}

function osobaLoged()
{
    loged = window.location.href.split("=")[1];
    if(loged != "true")
    {
        Array.from(document.getElementsByClassName("rezervacija"))[0].style.display = "none";
        Array.from(document.getElementsByClassName("kom"))[0].style.display = "none";
        document.getElementById("opis").style.display = "none ";
    }
}

function rezervisi()
{
    document.getElementById("rez").disabled = true;
    document.getElementById("rez").style.backgroundColor = "red";
    document.getElementById("rez").textContent = "Ceka se odgovor majstora";
    document.getElementById("rez").style.color = "black";
    document.getElementById("rez").style.fontSize = "20px";
}

function back()
{
    window.location.href = "index.html?log="+loged;
}