

const resultDiv = document.getElementById('result');


// errors
export const ID_NOT_FOUND_ERROR = 1;
export const INVALID_INPUT = 2;
export const NO_ERROR = 0;



export function activateElem(elem) {
    elem.classList.add('active');
}


export function deActivateElem(elem) {
    elem.classList.remove('active');
}


export function removeElem(elem) {
    elem.remove();
}




export function displayErrorMessages(element, content) {
    element.innerHTML = content;
};

// -----------------------------------------------------

// Add the recommended movies & user preferences (for evaluating the model results)

export function renderRecommendations(recommendations, preferences) {
    const preferencesArray = Array.from(preferences);
    const recommendationsArray = Array.from(recommendations);
    addPreferences(preferencesArray);
    addRecommendations(recommendationsArray);
};


function addRecommendations(recommendations) {
    if (document.getElementById('recommendationsDiv')) {
        removeElem(document.getElementById('recommendationsDiv'))
    };

    const recommendationsDiv = document.createElement('div');
    recommendationsDiv.classList.add('recommendations');
    recommendationsDiv.id = 'recommendationsDiv';

    // add a title
    const recommendationsTitle = document.createElement('h2');
    recommendationsTitle.textContent = "Recommendations";

    // add recommendations
    const recommContainer = document.createElement('div');

    recommendations.forEach(recommended => {
        const movieDiv = document.createElement('div');
        // Movie title
        const title = document.createElement('h3');
        title.textContent = recommended['title'];

        // Genres
        const genresDiv = document.createElement('div');
        genresDiv.classList.add('genres');

        const currGenres = recommended['genres'].split('|');
        for (let i = 0; i < currGenres.length; i++) {
            const genreSpan = document.createElement('span');
            genreSpan.textContent = currGenres[i];
            genresDiv.appendChild(genreSpan);
        }

        movieDiv.append(title, genresDiv);
        recommContainer.appendChild(movieDiv);
    });

    recommendationsDiv.append(recommendationsTitle, recommContainer);
    resultDiv.append(recommendationsDiv);
};

function addPreferences(preferences) {
    if (document.getElementById('preferencesDiv')) {
        removeElem(document.getElementById('preferencesDiv'))
    };

    // construct the parent div
    const preferencesDiv = document.createElement('div');
    preferencesDiv.classList.add('preferences');
    preferencesDiv.id = 'preferencesDiv';

    // add the title
    const preferencesTitle = document.createElement('h2');
    preferencesTitle.textContent = 'Preferences';

    // add the preferences
    const prefContainer = document.createElement('div');
    preferences.forEach(pref => {
        const prefSpan = document.createElement('span');
        prefSpan.textContent = pref;
        prefContainer.appendChild(prefSpan);
    });

    preferencesDiv.append(preferencesTitle, prefContainer);
    resultDiv.appendChild(preferencesDiv);
}