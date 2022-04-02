// Modal window
const refs = {
  openModalBtn: document.querySelector("[data-modal-open]"),
  closeModalBtn: document.querySelector("[data-modal-close]"),
  backdrop: document.querySelector(".js-backdrop"),
};

refs.openModalBtn.addEventListener("click", onModalOpen);
refs.closeModalBtn.addEventListener("click", onModalClose);

function onModalOpen() {
  document.body.classList.remove("backdrop--is-hidden");
  refs.backdrop.addEventListener("click", onBackdropClick);
  window.addEventListener("keydown", onEscPress);
}

function onModalClose() {
  document.body.classList.add("backdrop--is-hidden");
  refs.backdrop.removeEventListener("click", onBackdropClick);
  window.removeEventListener("keydown", onEscPress);
}

function onBackdropClick(e) {
  if (e.target === e.currentTarget) {
    onModalClose();
  }
}

function onEscPress(e) {
  const ESC_KEY_CODE = "Escape";
  if (e.code === ESC_KEY_CODE) {
    onModalClose();
  }
}
