var selectedRow = null;


function showAlert(message, className) {
    const alertsContainer = document.querySelector('.alerts-container');

    // Create the alert div
    const div = document.createElement('div');
    div.className = `alert alert-${className}`;
    div.appendChild(document.createTextNode(message));

    // Append the alert to the container
    alertsContainer.appendChild(div);

    // Automatically remove the alert after 3 seconds
    setTimeout(() => div.remove(), 3000);
}

// SHow Alerts
// function showAlert(message, className) {
//  const div = document.createElement('div');
//    div.className = 'alert alert-${className}';

  //  div.appendChild(document.createTextNode(message));
    //const container = document.querySelector('.container');
    //const main = document.querySelector('.main');
 //   container.insertBefore(div, main);

//    setTimeout(() => document.querySelector('.alert').remove(), 3000);
//} 

// Clear All Fields

function clearFields(){
    document.querySelector('#first_name').value = '';
    document.querySelector('#last_name').value = '';
    document.querySelector('#patient_id').value = '';
    document.querySelector('#condition').value = '';
}

// Add Values

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#patient-form').addEventListener('submit', (e) => {
        e.preventDefault();

        // Get Form Values
        const first_name = document.querySelector('#first_name').value;
        const last_name = document.querySelector('#last_name').value;
        const patient_id = document.querySelector('#patient_id').value;
        const condition = document.querySelector('#condition').value;

        // Validation
        if(first_name == '' || last_name == '' || patient_id == '' || condition == '') {
            showAlert('Please fill in all fields', 'danger');
        }
        else {
            // Add to Table
            if(selectedRow == null) {
                const list = document.querySelector('#patient-list');
                const row = document.createElement('tr');

                row.innerHTML = `
                    <td>${first_name}</td>
                    <td>${last_name}</td>
                    <td>${patient_id}</td>
                    <td>${condition}</td>
                    <td>
                        <a href="#" class="btn btn-warning btn-sm edit">Edit</a>
                        <a href="#" class="btn btn-danger btn-sm delete">Delete</a>
                    </td>
                `;
                list.appendChild(row);
                selectedRow = null;
                showAlert('Patient Added', 'success');
            }
            else{
                selectedRow.children[0].textContent = first_name;
                selectedRow.children[1].textContent = last_name;
                selectedRow.children[2].textContent = patient_id;
                selectedRow.children[3].textContent = condition;
                selectedRow = null;
                showAlert('Patient Updated', 'info');
            }
            clearFields();
        }
    });
});

// Edit Data

document.querySelector('#patient-list').addEventListener('click', (e) => {
    if (e.target.classList.contains('edit')) {
        selectedRow = e.target.parentElement.parentElement;
        document.querySelector('#first_name').value = selectedRow.children[0].textContent;
        document.querySelector('#last_name').value = selectedRow.children[1].textContent;
        document.querySelector('#patient_id').value = selectedRow.children[2].textContent;
        document.querySelector('#condition').value = selectedRow.children[3].textContent;
    }
});


// Delete Data

document.querySelector('#patient-list').addEventListener('click', (e) =>{
    target = e.target;
    if(target.classList.contains('delete')){
        target.parentElement.parentElement.remove();
        showAlert('Patient Data Has Been Deleted!', 'danger');
    }
});