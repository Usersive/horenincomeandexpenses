

const appTable = document.querySelector('#apptable');
const searchField = document.querySelector('#searchField');
const tableOutput = document.querySelector('#table-output');
const paginationContainer = document.querySelector('#pagination-container');

tableOutput.style.display ="none";

searchField.addEventListener('keyup', (e)=>{
  const searchValue=e.target.value;

  if(searchValue.trim().length > 0){
      paginationContainer.style.display="none";
      fetch("expense/search_expenses", {
            body: JSON.stringify({searchText: searchValue}),
            method: "POST",
        })
        .then(res => res.json());
        .then(data => {
            console.log('data', data);
            appTable.style.display="none";
            tableOutput.style.display="block";

            if (data.length===0){
                tableOutput.innerHTML="No result found";

            }
        });
    }else{
      appTable.style.display="block";
      paginationContainer.style.display="block";
      tableOutput.style.display="none";
    }
});
