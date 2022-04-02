// Limit range
const limitEl = document.querySelector("[data-limit]");
const limit = limitEl.dataset.limit;
const left = limitEl.dataset.left;
limitEl.style.width = `${(left / limit) * 100}%`;
