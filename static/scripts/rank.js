import { getCookie } from './util.js'

let comparisonQueue = [];
let loadingComparisons = false;
let csrftoken = getCookie('csrftoken');
const listSlug = window.listSlug;
comparisonQueue.push(...window.initialThings);
let currentMatchupID = 0;

document.addEventListener('DOMContentLoaded', async () => {
    loadNewComparison();
    document.getElementById('thing-box-1').addEventListener('click', () => {
        handleChoice(1);
    });
    document.getElementById('thing-box-2').addEventListener('click', () => {
        handleChoice(2);
    });
});

async function fetchComparisons() {
    if (comparisonQueue.length < 5 && !loadingComparisons) {
        loadingComparisons = true;
        const response = await fetch(`/${listSlug}/get-comparisons`);
        const data = await response.json();
        console.log(data)
        console.log(data.comparisons)
        comparisonQueue.push(...data.comparisons);
        loadingComparisons = false;
    }
}
function loadNewComparison() {
    const comparison = comparisonQueue.shift();
    if (comparison) {
        document.getElementById('thing-box-1').innerHTML = `
            <div class="thing-text">${comparison.thing1.name}</div>
        `
        document.getElementById('thing-box-2').innerHTML = `
            <div class="thing-text">${comparison.thing2.name}</div>
        `
        currentMatchupID = comparison.id
    }
}

function handleChoice(choice) {
    fetch(`/${listSlug}/complete-comparison/`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrftoken},
        body: JSON.stringify({
            "id": currentMatchupID,
            "choice": choice,
        })
    });
    fetchComparisons();
    loadNewComparison();
}

//<img class="thing-image" src="${comparison.thing2.image}"></img>