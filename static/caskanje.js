"use strict";

const chatWindow = document.querySelector("#chatWindow");
const idkorisnik = document.querySelector("#idkorisnik").getAttribute("value");
const idzanatlija = document
  .querySelector("#idzanatlija")
  .getAttribute("value");
const porukeUrl = document.querySelector("#porukeUrl").innerHTML;
const sendButton = document.querySelector("#sendButton");
const chatInput = document.querySelector("#chatInput");
const tipKorisnika = document.querySelector("#tipKorisnika").innerHTML;
sendButton.addEventListener("click", (e) => {
  setTimeout(() => {
    chatInput.value = "";
  }, 100);
});

setInterval(() => {
  const messages = fetch(
    porukeUrl +
      new URLSearchParams({
        idkorisnik,
        idzanatlija,
      })
  )
    .then((response) => response.json())
    .then((json) => {
      chatWindow.innerHTML = "";
      json.poruke.forEach((poruka) => {
        let smer = "align-self-end";
        if (poruka.smer == "1") {
          smer = "align-self-start";
        }
        const poruka_html = `
        <div class="${smer} poruka">
                <p>${poruka.poruka}</p>
        </div>
        `;
        chatWindow.innerHTML += poruka_html;
        chatWindow.scrollTop = chatWindow.scrollHeight;
      });
    });
}, 1000);
