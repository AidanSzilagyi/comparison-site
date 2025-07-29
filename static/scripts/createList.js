document.addEventListener("DOMContentLoaded", () => {
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
    formContainer.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            
            const container = e.target.closest('.thing-container');
            const selectedImage = container.querySelector('.js-selected-thing-image');
            const unselectedImage = container.querySelector('.js-unselected-thing-image');
            
            console.log("change detected");
            console.log(container);
            console.log(selectedImage)
            console.log(unselectedImage)

            if (selectedImage && unselectedImage) {
                console.log("We're doing it!")
                selectedImage.src = URL.createObjectURL(file);
                selectedImage.style.display = 'block';
                unselectedImage.style.display = 'none';
            }
        }
    });
});