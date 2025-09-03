/*
    >> This file interacts with the client input at the first level
       (is new or not)
    
    >> if the client is new: proceed to the preferences level

    >> if not: proceed to the id-level


    >> الله المستعان <<
*/



const yesBtn = document.getElementById('NewUserYesBtn');
const noBtn = document.getElementById('NewUserNoBtn');
const firstLev = document.getElementById('firstLev');
const idLev = document.getElementById('IdLev');
const preferencesLev = document.getElementById('preferencesLev');
const preferencesInputs = document.getElementById('preferencesInputs');


import { activateElem, deActivateElem } from "./utils.js";



noBtn.addEventListener('click', _ => {
    deActivateElem(firstLev);
    activateElem(idLev);
})


yesBtn.addEventListener('click', async _ => {
    deActivateElem(firstLev);
    activateElem(preferencesLev);

    // Get dynaminc movies features
    const request = await fetch('/get_movie_features', {
        method : "POST",
        headers : {"Content-Type" : "application/json"},
    });

    const response = await request.json();
    
    if (response['error'] == 0) {
        response.features.forEach(feature => {
            const btn = document.createElement("button");
            btn.classList.add('preferenceBtn');
            btn.textContent = feature;
            preferencesInputs.appendChild(btn); 
        });
    }
 
});
