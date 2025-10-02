document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".js-list-author").forEach((card) => {
        card.addEventListener("click", (event) => {
            event.stopPropagation()
        })
    })
});