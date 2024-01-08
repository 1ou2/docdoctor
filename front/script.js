//import { APP_SERVER  } from './menv';

APP_SERVER = "http://127.0.0.1:8012";

function checkBearer() {
    var bearer = localStorage.getItem('bearer');
    bearercontainer = document.getElementById('bearer');
    if (bearer === null || bearer.length == 0) {
    bearercontainer.textContent = "Bearer - Not set";
    bearercontainer.innerHTML += "<form id='bearerform'><input type = 'text' id='newbearer'></form>";
    }
    else {
    bearercontainer.textContent = "Bearer is set " + APP_SERVER ;          
    }
}

// Function to display the API response
function displayResponse(data) {
    const responseContainer = document.getElementById('responseContainer');
    if (data && data.text) {
      const responseValue = data.text;
      responseContainer.textContent = responseValue;
    } else {
      responseContainer.textContent = 'Invalid or missing response data';
      }
    //responseContainer.innerHTML = JSON.stringify(data, null, 2);
    responseContainer.style.display = 'block'; // Show the response container
  }

  // 
  function submitBearer() {
    document.getElementById('bearerform').addEventListener('submit', function (event) {
        event.preventDefault();
        const bearerid = document.getElementById('newbearer').value;
        console.log("new bearer "+ bearerid);
        localStorage.setItem('bearer',bearerid);
        
    });
  }

  function searchByID() {
    // Function to handle the Text ID form submission (POST request)
    document.getElementById('textIdForm').addEventListener('submit', function (event) {
        event.preventDefault();
  
        const textId = document.getElementById('text_id').value;
  
        const apiUrl = APP_SERVER + `/v1.0/text/${encodeURIComponent(textId)}`;
        //localStorage.setItem('bearer', "");
        var bearer = localStorage.getItem('bearer');
        console.log("bearer "+ bearer)
        const requestData = {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+bearer,
          },
          //body: JSON.stringify({
          //  text_id: textId,
          //}),
        };
  
        fetch(apiUrl, requestData)
          .then(response => response.json())
          .then(data => {
            displayResponse(data);
          })
          .catch(error => {
            displayResponse({ error: 'Failed to fetch data' });
            console.error('GET Error:', error);
          });
      });
  }

  function searchByText(){
    // Function to handle the Search form submission (GET request)
    document.getElementById('searchForm').addEventListener('submit', function (event) {
        event.preventDefault();
  
        const searchText = document.getElementById('search').value;
  
        const apiUrl = APP_SERVER+ `/v1.0/text?text_id=${encodeURIComponent(searchText)}`; 
        const requestData = {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+bearer,
          },
        };
  
        fetch(apiUrl, requestData)
          .then(response => response.json())
          .then(data => {
            displayResponse(data);
          })
          .catch(error => {
            displayResponse({ error: 'Failed to fetch data' });
            console.error('GET Error:', error);
          });
      });
  }