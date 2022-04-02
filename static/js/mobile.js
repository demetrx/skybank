const refs = {
  openMenuBtn: document.querySelector("[data-mobile='open']"),
  closeMenuBtn: document.querySelector("[data-mobile='close']"),
  menu: document.querySelector("[data-mobile='menu']"),
};

refs.openMenuBtn.addEventListener("click", onMenuOpen);
refs.closeMenuBtn.addEventListener("click", onMenuClose);

function onMenuOpen() {
  refs.menu.classList.add("mobile--show");
  console.log("Click");
}

function onMenuClose() {
  refs.menu.classList.remove("mobile--show");
}
