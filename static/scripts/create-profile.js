document.addEventListener("DOMContentLoaded", () => {
    document.querySelector(".js-image-input").addEventListener("change", function(event) {
        const file = event.target.files[0];
        if (file) {
            const img = document.getElementById("js-profile-image");
            img.src = URL.createObjectURL(file);
            img.style.display = "block";
        }
    });
});