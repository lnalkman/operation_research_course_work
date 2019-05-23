import 'babel-polyfill';
import * as axios from 'axios';

let graphDescriptionInput = document.querySelector('#graph-description-input');
let randomGraphDescriptionForm = document.querySelector('#random-graph-description-form');

// Reading graph description from file and write to the textarea with graph description
document.querySelector('#graph-file-input').addEventListener('change', event => {
  const reader = new FileReader();

  reader.addEventListener('loadend', () => {
    graphDescriptionInput.value = reader.result;
  });

  reader.readAsText(event.target.files[0]);
});


// Random graph generation
document.querySelector('#generate-random-graph-btn').addEventListener('click',async event => {
  const graphDescriptionFormData = new FormData(randomGraphDescriptionForm);

  let queryParams = {};
  graphDescriptionFormData.forEach((value, key) => {
    queryParams[key] = value;
  });

  const response = await axios.get('/random_graph/', {
    params: queryParams
  });

  const graph = response.data.data;
  graphDescriptionInput.value = graph
    .map(edge => edge.join(', '))
    .join('\n');

  $(document.querySelector('#random-graph-generation-modal')).modal('hide')
});