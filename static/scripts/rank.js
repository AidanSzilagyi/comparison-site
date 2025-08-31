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
    if (comparisonQueue.length < 2 && !loadingComparisons) {
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
    console.log("loadNewComparison - CompQueue.len: " + comparisonQueue.length)

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
        currentMatchupID = comparison.id;
    } else {
        for (let i = 0; i < 2; i++) {
            thingBoxes[i].innerHTML = "";
        }
        currentMatchupID = "";
        fetchComparisons();
    }
}

let submitting = false;
function handleChoice(choice) {
    const id = currentMatchupID;
    if (submitting || !id) return;
    
    submitting = true;
    loadNewComparison();
    submitting = false; 

    console.log("HandleChoice - CompQueue.len: " + comparisonQueue.length);
    fetch(`/${listSlug}/complete-comparison/`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrftoken},
        body: JSON.stringify({
            "id": id,
            "choice": choice,
        })
    }).then(() => {
        fetchComparisons();
    }).then(() => {
        if (!currentMatchupID && comparisonQueue.length > 0) {
            loadNewComparison();
        }
    });
}