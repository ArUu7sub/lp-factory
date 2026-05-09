document.querySelectorAll(".lp-faq__question").forEach((button) => {
  button.addEventListener("click", () => {
    const answer = button.nextElementSibling;
    const isOpen = button.getAttribute("aria-expanded") === "true";
    const mark = button.querySelector(".lp-faq__mark");

    button.setAttribute("aria-expanded", String(!isOpen));
    answer.hidden = isOpen;

    if (mark) {
      mark.textContent = isOpen ? "＋" : "−";
    }
  });
});
