import { getCookie, BigText } from './util.js'

let comparisonQueue = [];
let loadingComparisons = false;
let csrftoken = getCookie('csrftoken');
const listSlug = window.listSlug;
comparisonQueue.push(...window.initialThings);
let currentMatchupID = 0;
let thingBoxes = [];

document.addEventListener('DOMContentLoaded', async () => {
    thingBoxes[0] = document.getElementById('thing-box-1');
    thingBoxes[1] = document.getElementById('thing-box-2');
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
        let matchupIDs = currentMatchupID;
        comparisonQueue.forEach((comparison) => {
            matchupIDs += "," + comparison.id
        })
        console.log(matchupIDs)
        const response = await fetch(`/${listSlug}/get-comparisons?ids=${matchupIDs}`);
        const data = await response.json();
        comparisonQueue.push(...JSON.parse(data.comparisons));
        loadingComparisons = false;
    }
}
function loadNewComparison() {
    const comparison = comparisonQueue.shift();
    if (comparison) {
        let comparisonThings = [comparison.thing1, comparison.thing2];
        for (let i = 0; i < 2; i++) {
            if (comparisonThings[i].name && comparisonThings[i].image) {
                thingBoxes[i].innerHTML = `
                    <img class="thing-image" src="${comparisonThings[i].image}">
                    <div class="thing-text-container">
                        <span class="thing-text" id="text-${i}">${comparisonThings[i].name}</span>
                    </div>
                `;
                BigText(`span#text-${i}`);
            } else if (comparisonThings[i].name) {
                thingBoxes[i].innerHTML = `
                    <span class="thing-text-only" id="text-${i}">${comparisonThings[i].name}</span>
                `;
                BigText(`span#text-${i}`, {
                    maximumFontSize: 100,
                });
            } else {
                thingBoxes[i].innerHTML = `
                    <img class="thing-image-only" src="${comparisonThings[i].image}">
                `;
            }
        }
        currentMatchupID = comparison.id
    } else {
        currentMatchupID = ""
        // Load next matchup after fetch
    }
}

function handleChoice(choice) {
    console.log(comparisonQueue)
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