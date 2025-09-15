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
        updateThingNumbering();
    });

    formContainer.addEventListener('click', (e) => {
        if (e.target.closest('.trash-can-icon-container')) {
            const container = e.target.closest('.thing-container');
            const deleteCheckbox = container.querySelector('.delete-checkbox');
            if (container && deleteCheckbox) {
                container.style.display = 'none';
                deleteCheckbox.checked = true;
            }
            updateThingNumbering();
        }
    });
    // Adding Thing images
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
    // Removing Thing images
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


    // Numbers on each thing
    const numThingsHeader = document.getElementById("num-things-header");
    function updateThingNumbering() {
        console.log("updating the numbering")
        const thingContainers = formContainer.querySelectorAll('.thing-container');
        let numThings = 0
        thingContainers.forEach((thingContainer) => {
            if (thingContainer.style.display !== 'none') {
                thingContainer.querySelector('.thing-number').textContent = numThings + 1;
                numThings += 1;
            }
        });
        numThingsHeader.innerText = numThings;
    }
    updateThingNumbering();

    /* Handle invite users popup when invite radio selector is changed */
    const inviteContainer = document.getElementById("invite-users-container");
    const permissionRadio = document.querySelectorAll('.js-permission-radio');

    function handleChange(event) {
        const requiresInvite = event.target.dataset.requiresInvite === "True";
        inviteContainer.style.display = requiresInvite ? "block" : "none";
    }
    permissionRadio.forEach(radio => {
        radio.addEventListener("change", handleChange);
    });

    handleChange({ target: document.querySelector('.js-permission-radio:checked') });
});

function addLoadMatchupsListener(thingBox) {
    thingBox.querySelector(".js-load-matchups").addEventListener("mouseover", async () => {
        const matchupHistory = thingBox.querySelector(".js-matchup-history");
        const ranking = thingBox.querySelector(".js-position-number").textContent;
        const response = await fetch(`/${listSlug}/get-matchups-from-thing?ranking=${ranking}`);
        const data = await response.json();
        matchupHistory.innerHTML = "";
        data.matchups.forEach(matchup => {
            let matchupBox;
            if (matchup.result == "win") {
                matchupBox = wonMatchup.content.cloneNode(true);
            } else {
                matchupBox = lostMatchup.content.cloneNode(true);
            }
            matchupBox.querySelector(".js-opponent").textContent = matchup.opponent;
            if (permission == "Public"){
                matchupBox.querySelector(".js-matchup-username").textContent = `by ${matchup.username}`;
            }
            matchupHistory.appendChild(matchupBox);
        });
    }, { once: true });
}