document.addEventListener("DOMContentLoaded", () => {
    const csvReveal = document.getElementById("js-popup-container")
    const uploadFileImage = document.getElementById("js-upload-file-image")

    document.getElementById("js-import-file").addEventListener("click", (e) => {
        if (e.target.closest("#js-popup-container")) return;
        if (csvReveal.style.display === "none") {
            csvReveal.style.display = 'flex';
            uploadFileImage.style.display = 'none';
        } else {
            csvReveal.style.display = 'none';
            uploadFileImage.style.display = 'block';
        }
    });
    const fileInput = document.getElementById("file-input");
    const fileName = document.getElementById("file-name");
    fileInput.addEventListener("change", () => {
        fileName.textContent = fileInput.files.length > 0
            ? fileInput.files[0].name
            : "No file selected";
    });

});