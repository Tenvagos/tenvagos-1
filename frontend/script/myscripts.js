const navToggle = document.querySelector(".nav-toggle-harold");
const nav = document.querySelector(".nav-harold");

navToggle.addEventListener("click", () => {
  nav.classList.toggle("nav--visible-harold");
});