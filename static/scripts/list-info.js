let listSlug;
let numThingsLoaded = 0;
let totalNumThings;
let allThingsList; 
let allThingsButton;
let permission;
//templates
let emptyBox; let textAndImage; let textOnly;
document.addEventListener("DOMContentLoaded", async () => {
    totalNumThings = document.getElementById("total-num-things").textContent;
    listSlug = document.getElementById("list-slug").textContent;
    allThingsList = document.getElementById("all-things-list");
    permission = document.getElementById("permission").textContent;

    emptyBox = document.getElementById("empty-thing-box");
    textAndImage = document.getElementById("text-and-image");
    textOnly = document.getElementById("text-only");
    wonMatchup = document.getElementById("won-matchup");
    lostMatchup = document.getElementById("lost-matchup");

    allThingsButton = document.getElementById("all-things-button");
    allThingsButton.addEventListener("click", () => {
        fetchAllThings();
    });
    // Add initial Top/Bottom 5 Event Listeners
    for (const thingBox of document.getElementById("js-top-five").children) {
        addLoadMatchupsListener(thingBox);
    }
    for (const thingBox of document.getElementById("js-bottom-five").children) {
        addLoadMatchupsListener(thingBox);
    }
});
async function fetchAllThings() {
    const response = await fetch(`/${listSlug}/get-all-things?loaded=${numThingsLoaded}`);
    const data = await response.json();
    console.log(data.things);
    data.things.forEach(async thing => {
        const thingBox = emptyBox.content.cloneNode(true).querySelector("#thing-box");
        numThingsLoaded++;
        thingBox.querySelector(".js-position-number").textContent = numThingsLoaded;
        
        if (thing.image) {
            const nameBox = textAndImage.content.cloneNode(true);
            nameBox.querySelector(".js-thing-name").textContent = thing.name;
            nameBox.querySelector(".js-thing-image").src = thing.image;
            thingBox.insertBefore(nameBox, thingBox.querySelector("#thing-record"));
        } else {
            const nameBox = textOnly.content.cloneNode(true);
            nameBox.querySelector(".js-thing-name-only").textContent = thing.name;
            thingBox.insertBefore(nameBox, thingBox.querySelector("#thing-record"));
        }
        thingBox.querySelector(".js-thing-wins").textContent = thing.wins;
        thingBox.querySelector(".js-thing-losses").textContent = thing.losses;
        addLoadMatchupsListener(thingBox);
        allThingsList.appendChild(thingBox);
    });
    if (totalNumThings == numThingsLoaded) {
        allThingsButton.style.display = "none";
    }
}
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