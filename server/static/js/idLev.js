/*
    >> This file is to handle the ID level.
    >> user inputs the id
        # if found -> recommend videos for him
        # if not -> alert then go to the preferences level


    >> الله المستعان <<
*/

import {NO_ERROR, ID_NOT_FOUND_ERROR, INVALID_INPUT, activateElem, deActivateElem, removeElem, renderRecommendations, displayErrorMessages}  from "./utils.js";





const idSubmitBtn = document.getElementById('idSubmitBtn');
const idInput = document.getElementById('idInput');
const idLev = document.getElementById('IdLev');
const preferencesLev = document.getElementById('preferencesLev');
const resetLev = document.getElementById('resetLev');
const idErrors = document.getElementById('idErrors');

idSubmitBtn.addEventListener('click',  async _ => {
    // Construting the message
    const userId = idInput.value;
    const payload = {
        user_id : userId
    };

    const request = await fetch('/recommend_for_existing_user', {
        method : "POST",
        headers : {"Content-Type" : "application/json"},
        body : JSON.stringify(payload)
    });


    // Sending & awaiting for response
    const response = await request.json()

    if (response['error'] != NO_ERROR) {
        // display the error
        displayErrorMessages(idErrors, response['message']);
    }

    else {
        deActivateElem(idLev);
        activateElem(resetLev);
        renderRecommendations(response['recommendations'], response['user_preferences']);
    }
});
