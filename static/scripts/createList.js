

let numThings = 1; // change this to 2 at some point
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.js-thing-adder').addEventListener('click', () => {
        document.querySelector('.js-list-of-things').innerHTML += `
                <div class="thing-container"">
                    <input class="thing-name-input" name="thing-${numThings}-name" type="text" placeholder="Enter a thing">
                    <input style="display: none;" name="thing-${numThings}-image" type="file" id="file-input-${numThings}">
                    <label class="thing-file-input" for="file-input-${numThings}">Choose Image</label>
                    <div class="trash-can-icon-container">
                        <img class="trash-can-icon-image" src="{% static 'images/trash-can-icon.png' %}">
                    </div>
                    <div class="info-icon-container">
                        <img class="info-icon-image" src="{% static 'images/info-icon-a.png' %}">
                    </div>
                </div>
        `;
        document.querySelector('.')
        numThings++;
    });

    document.querySelector('.js-list-of-things').addEventListener('click', (e) => {
        if (e.target.closest('.trash-can-icon-container')) {
            const container = e.target.closest('.thing-container');
            if (container) container.remove();
        }
    });
});



document.addEventListener("DOMContentLoaded", () => {
    const formContainer = document.getElementById("list-of-things-container");
    const emptyForm = document.getElementById("empty-form-template");
    const totalFormNum = document.querySelector('input[name="form-TOTAL_FORMS"]');

    document.getElementById("add-thing-button").addEventListener("click", () => {
        const formCount = parseInt(totalFormNum.value);
        const newFormHTML = emptyForm.replace(/__prefix__/g, formCount);
        formContainer.insertAdjacentHTML("beforeend", newFormHTML);
        totalFormNum.value = formCount + 1;
    });
});