document.addEventListener("DOMContentLoaded", () => {
    // Adding and removing List image
    const selectedListImage = document.querySelector('.js-selected-list-image');
    const unselectedListImage = document.querySelector('.js-unselected-list-image');
    const imageListInput = document.querySelector(".js-list-image-input");
    const removeListImageButton = document.getElementById("js-remove-list-image");
    if (selectedListImage && unselectedListImage && imageListInput && removeListImageButton) {
        imageListInput.addEventListener("change", function(event) {
            const file = event.target.files[0];
            if (file) {
                selectedListImage.src = URL.createObjectURL(file);
                selectedListImage.style.display = 'flex';
                unselectedListImage.style.display = 'none';
                removeListImageButton.style.display = 'flex';
            }
        });
        removeListImageButton.addEventListener("click", () => {
            selectedListImage.src = "";
            selectedListImage.style.display = 'none';
            unselectedListImage.style.display = 'flex';
            imageListInput.value = "";
            removeListImageButton.style.display = 'none';
        });
    }

    // Adding and removing Things with Add Thing and Trash Can, respectively
    const formContainer = document.getElementById("js-list-of-things");
    const emptyForm = document.getElementById("empty-form-template").innerHTML;
    const totalFormNum = document.querySelector('input[name="form-TOTAL_FORMS"]');
    
    document.getElementById("js-add-thing-button").addEventListener("click", () => {
        const formCount = parseInt(totalFormNum.value);
        const newFormHTML = emptyForm.replace(/__prefix__/g, formCount);

        const newFormElement = document.createElement('template');
        newFormElement.innerHTML = newFormHTML.trim(); 
        const newFormNode = newFormElement.content.firstChild;
        formContainer.insertBefore(newFormNode, document.getElementById("js-add-thing-button"));
        totalFormNum.value = formCount + 1;
    });

    formContainer.addEventListener('click', (e) => {
        if (e.target.closest('.trash-can-icon-container')) {
            const container = e.target.closest('.thing-container');
            const deleteCheckbox = container.querySelector('.delete-checkbox');
            if (container && deleteCheckbox) {
                container.style.display = 'none';
                deleteCheckbox.checked = true;
            }
        }
    });
    // Adding and removing Thing images
    formContainer.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            
            const container = e.target.closest('.thing-container');
            const selectedImage = container.querySelector('.js-selected-thing-image');
            const unselectedImage = container.querySelector('.js-unselected-thing-image');
            const removeFlag = container.querySelector(".js-remove-image-flag");

            console.log("change detected");
            console.log(container);
            console.log(selectedImage)
            console.log(unselectedImage)

            if (selectedImage && unselectedImage) {
                console.log("We're doing it!")
                selectedImage.src = URL.createObjectURL(file);
                selectedImage.style.display = 'block';
                unselectedImage.style.display = 'none';
                removeFlag.value = "false";
            }

            const removeImageButton = container.querySelector('.js-remove-image-button')
            if (removeImageButton) {
                removeImageButton.style.display = 'flex';
            }
        }
    });
    formContainer.addEventListener('click', (e) => {
        removeImageButton = e.target.closest('.js-remove-image-button');
        if (removeImageButton) {
            const container = e.target.closest('.thing-container');
            const selectedImage = container.querySelector('.js-selected-thing-image');
            const unselectedImage = container.querySelector('.js-unselected-thing-image');
            const imageInput = container.querySelector(".js-image-input");
            const removeFlag = container.querySelector(".js-remove-image-flag");

            if (selectedImage && unselectedImage && imageInput) {
                selectedImage.src = "";
                selectedImage.style.display = 'none';
                unselectedImage.style.display = 'flex';
                imageInput.value = "";
                removeImageButton.style.display = 'none';
                if (removeFlag) {
                    removeFlag.value = "true";
                }
            }
        }
    });

    // Descriptions for Permissions
    const radios = document.querySelectorAll('input[name="permission"]');
    const descriptionBox = document.getElementById("permission-details");
    
    function updateDescription() {
        const checked = document.querySelector('input[name="permission"]:checked');
        if (checked) {
            descriptionBox.textContent = checked.dataset.description;
        }
    }

    updateDescription(); 
    radios.forEach(radio => {
        radio.addEventListener("change", updateDescription);
    });
});