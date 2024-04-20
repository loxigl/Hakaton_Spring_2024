let base = '/api/v1'

window.onload = function () {
    fetch(base + '/user/id')
        .then(response => response.json())
        .then(data => {
            let userId = data.user_id;
            fetch(base + '/worksheet/' + userId)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Worksheet not found');
                    }
                    return response.json();
                })
                .then(worksheetData => {
                        document.querySelector('input[name="given_name"]').value = worksheetData.given_name;
                        document.querySelector('input[name="family_name"]').value = worksheetData.family_name;
                        document.querySelector('input[name="phone_number"]').value = worksheetData.phone_number;
                        document.querySelector('input[name="chosen_datetime"]').value = worksheetData.chosen_datetime;
                        document.querySelector('select[name="meeting_duration"]').value = worksheetData.meeting_duration;
                        let hobbyInputs = document.querySelectorAll('input[name="radio"]');
                        for (let input of hobbyInputs) {
                            if (worksheetData.hobby.includes(input.nextElementSibling.textContent)) {
                                input.checked = true;
                            }
                        }

                        let formatInputs = document.querySelectorAll('input[name="radio2"]');
                        for (let input of formatInputs) {
                            if (input.nextElementSibling.textContent === worksheetData.format) {
                                input.checked = true;
                            }
                        }
                    }
                )
                .catch(error => {
                    console.error('Error:', error);
                });
        });
}

async function submitForm() {
    let form = document.querySelector('form');
    let formData = new FormData(form);
    let formJson = {};
    for (let [key, value] of formData.entries()) {
        formJson[key] = value;
    }
    let selectedHobbies = Array.from(document.querySelectorAll('input[name="radio"]:checked'), input => input.nextElementSibling.textContent);
    let selectedFormat = document.querySelector('input[name="radio2"]:checked').nextElementSibling.textContent;
    formJson['hobby'] = selectedHobbies;
    formJson['format'] = selectedFormat;
    delete formJson['radio'];
    delete formJson['radio2'];
    let userId = await fetch(base + '/user/id').then(response => response.json()).then(data => data.user_id)
    let userHasWorksheet = await checkUserWorksheet();
    let method = userHasWorksheet ? 'PUT' : 'POST';
    console.log(method)
    let response = await fetch(base + '/worksheet/' + userId, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formJson)
    });

    if (response.ok) {
        console.log("Worksheet submitted successfully");
    } else {
        console.error("Error submitting worksheet: " + response.statusText);
    }
}

async function checkUserWorksheet() {
    let result = false;
    await fetch(base + '/user/id')
        .then(response => response.json())
        .then(data => {
            let userId = data.user_id;
            return fetch(base + '/worksheet/' + userId);
        })
        .then(response => {
            if (response.ok) {
                result = true;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    console.log(result)
    return result;

}