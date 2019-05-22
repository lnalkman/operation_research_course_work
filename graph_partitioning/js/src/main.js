import 'babel-polyfill';
import * as axios from 'axios';

let graphDescriptionInput = document.querySelector('#graph-description-input');

// Reading graph description from file and write to the textarea with graph description
document.querySelector('#graph-file-input').addEventListener('change', event => {
  const reader = new FileReader();

  reader.addEventListener('loadend', () => {
    graphDescriptionInput.value = reader.result;
  });

  reader.readAsText(event.target.files[0]);
});


