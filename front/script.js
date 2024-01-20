
//APP_SERVER = "http://127.0.0.1:8012";
APP_SERVER="https://wa-gabai.azurewebsites.net/"


// Function to display the API response
function displayError(data) {
  const responseContainer = document.getElementById('responseContainer');
  console.log(data);
  if (data && data.error) {
    const responseValue = data.error;
    responseContainer.textContent = responseValue;
  } else {
    responseContainer.textContent = 'Invalid or missing response data';
    }
  //responseContainer.innerHTML = JSON.stringify(data, null, 2);
  responseContainer.style.display = 'block'; // Show the response container
}
// Function to display the API response
function displayText(data) {
    const responseContainer = document.getElementById('responseContainer');
    console.log(data);
    if (data && data.text) {
      const responseValue = data.text;
      responseContainer.textContent = responseValue;
    } else {
      responseContainer.textContent = 'Invalid or missing response data';
      }
    //responseContainer.innerHTML = JSON.stringify(data, null, 2);
    responseContainer.style.display = 'block'; // Show the response container
  }

  // Function to display the API response
function displayResponse(data) {
  const responseContainer = document.getElementById('responseContainer');
  console.log(data);
  if (data && data.response) {
    const responseValue = data.response;
    responseContainer.textContent = responseValue;
  } else {
    responseContainer.textContent = 'Invalid or missing response data';
    }
  //responseContainer.innerHTML = JSON.stringify(data, null, 2);
  responseContainer.style.display = 'block'; // Show the response container
}
  

  function searchByID() {
    // Function to handle the Text ID form submission (POST request)
    document.getElementById('textIdForm').addEventListener('submit', function (event) {
        event.preventDefault();
  
        const textId = document.getElementById('text_id').value;
  
        const apiUrl = APP_SERVER + `/v1.0/text/${encodeURIComponent(textId)}`;
        //localStorage.setItem('bearer', "");
        var bearer = localStorage.getItem('bearer');
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
            displayText(data);
          })
          .catch(error => {
            displayError({ error: 'Failed to fetch data' });
            console.error('GET Error:', error);
          });
      });
  }

  function searchByText(){
    // Function to handle the Search form submission (GET request)
    document.getElementById('searchForm').addEventListener('submit', function (event) {
        event.preventDefault();
        var bearer = localStorage.getItem('bearer');
        const searchText = document.getElementById('search').value;
  
        const apiUrl = APP_SERVER+ `/v1.0/text/ask`; 
        const requestData = {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+bearer,
          },
          body: JSON.stringify({
            "question": searchText,
            "max_result":"1"}),
        };
  
        fetch(apiUrl, requestData)
          .then(response => response.json())
          .then(data => {
            displayResponse(data);
          })
          .catch(error => {
            displayResponse({ error: 'Failed to fetch data' });
            console.error('POST Error:', error);
          });
      });
  }