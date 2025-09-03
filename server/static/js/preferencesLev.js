/**
    >> This file is to ask a new user to enter his preferences.
 
    >> الله المستعان <<
*/




import { activateElem, deActivateElem, renderRecommendations, displayErrorMessages}  from "./utils.js";
const yesBtn = document.getElementById('NewUserYesBtn');
const preferencesInputs = document.getElementById('preferencesInputs');
const preferenceSubmitBtn = document.getElementById('preferenceSubmitBtn');
const preferencesLev = document.getElementById('preferencesLev');
const resetLev = document.getElementById('resetLev');
const selectedPreferences = [];





yesBtn.addEventListener('click', function() {
    setTimeout( _ => {
        // Get the buttons
        const preferencesBtns = Array.from(document.querySelectorAll('.preferenceBtn'));

        // Get the selected preferences
        preferencesBtns.forEach(btn => {
            btn.addEventListener('click', _ => {
                selectedPreferences.push(btn.textContent);
                btn.classList.add('selected');
            });
        });
    }, 1000);

    // Submit
    preferenceSubmitBtn.addEventListener('click', async _ => {
        if (selectedPreferences.length == 0) {
            displayErrorMessages(
                document.getElementById('preferencesErrors'),
                'No preferences selected'
            )
        }

        

        else {
            deActivateElem(preferencesLev);
            activateElem(resetLev);
            const payload = {
                preferences : selectedPreferences
            };

            const request = await fetch('/recommend_for_new_user', {
                method : "POST",
                headers : {"Content-Type" : "application/json"},
                body : JSON.stringify(payload)
            });

            const response = await request.json();

            // render the recommendations
            if (response['error'] == 0) {
                renderRecommendations(response['recommendations'], response['user_preferences'])
            }         
        }
    });
  
});



// document.addEventListener('DOMContentLoaded', ()=> {
//   getMovieFeatures();
// });