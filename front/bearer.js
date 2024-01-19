

function checkBearer() {
    var bearer = localStorage.getItem('bearer');
    bearercontainer = document.getElementById('bearer');
    if (bearer === null || bearer.length == 0) {
      
      bearercontainer.textContent = "Bearer is NOT set. Please enter Bearer.";
      bearercontainer.innerHTML += "<form id='bearerform'><input type = 'text' id='newbearer'> <input type = 'submit' label='send' value='send'></input> </form>";
      submitBearer();
    }
    else {
      bearercontainer.innerHTML = "<p>Bearer is set!!.</p> " ;     
      bearercontainer.innerHTML += "<form id='bearerform'><input type='checkbox' id='resetbearer'> <input type = 'submit' label='send' value='reset'></input> </form>";
      submitBearer();
    }
    
}


  // 
  function submitBearer() {
    if (document.getElementById('bearerform')) {

        document.getElementById('bearerform').addEventListener('submit', function (event) {
            event.preventDefault();
            if ( document.getElementById('newbearer')){
                const bearerid = document.getElementById('newbearer').value;
                console.log("new bearer "+ bearerid);
                localStorage.setItem('bearer',bearerid);
            }
            else if (document.getElementById('resetbearer')){
                
                console.log("reset bearer ");
                localStorage.setItem('bearer',"");
            }
            window.location.reload();
           
        });
    }
    
  }

  