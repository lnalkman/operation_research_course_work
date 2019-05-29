import 'babel-polyfill';
import * as axios from 'axios';
import * as vis from 'vis';

let graphDescriptionInput = document.querySelector('#graph-description-input');
let randomGraphDescriptionForm = document.querySelector('#random-graph-description-form');
let graphInputForm = document.querySelector('#graph-input-form');

const formDataToObject = formData => {
  let formDataAsObject = {};
  formData.forEach((value, key) => {
    formDataAsObject[key] = value;
  });

  return formDataAsObject
};

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

  const response = await axios.get('/random_graph/', {
    params: formDataToObject(graphDescriptionFormData)
  });

  const graph = response.data.data;
  graphDescriptionInput.value = graph
    .map(edge => edge.join(', '))
    .join('\n');

  $(document.querySelector('#random-graph-generation-modal')).modal('hide')
});

graphInputForm.addEventListener('submit', async event => {
  event.preventDefault();
  event.stopPropagation();

  let formData = new FormData(graphInputForm);

  const response = await axios.get('/kernighan_lin/', {
    params: formDataToObject(formData)
  });

  const data = response.data.data;
  const graph = data.graph;
  const kernighanLinInfo = data.kernighan_lin;
  let modifiedAlgorithmInfo = data.modified_algorithm;
  if (modifiedAlgorithmInfo === null) {
    modifiedAlgorithmInfo = kernighanLinInfo;
  }
  console.log(modifiedAlgorithmInfo);

  let edges = [];
  for (const node of Object.keys(graph)) {
    for (const connectedNode of Object.keys(graph[node])) {
      if (connectedNode < node) {
        edges.push({
          from: node,
          to: connectedNode,

          // Edge weight
          label: String(graph[node][connectedNode])
        })
      }
    }
  }

  let kernighanLinNodes = [];
  const kernighanLinPartitions = kernighanLinInfo.partitions;
  for (let partition = 0; partition < 3; partition++) {
    for (const node of kernighanLinPartitions[partition]) {
      kernighanLinNodes.push({
        id: node,
        label: String(node),
        group: partition
      })
    }
  }

  let modifiedAlgorithmNodes = [];
  const modifiedAlgorithmPartitions = modifiedAlgorithmInfo.partitions;
  for (let partition = 0; partition < 3; partition++) {
    for (const node of modifiedAlgorithmPartitions[partition]) {
      modifiedAlgorithmNodes.push({
        id: node,
        label: String(node),
        group: partition
      })
    }
  }

  const networkOptions = {
    width: '100%',
    height: '500px'
  };

  // Draw graph(network) with Kernighan-Lin partitioned subgraphs
  const kernighanLinGraphContainer = document.getElementById(
    'kernighan-lin-partitioned-graph'
  );
  const kernighanLinNetworkData = {
    nodes: kernighanLinNodes,
    edges
  };
  new vis.Network(
    kernighanLinGraphContainer,
    kernighanLinNetworkData,
    networkOptions
  );

  // Draw graph(network) with modified Kernighan-Lin algorithm partitioned subgraphs
  const modifiedAlgorithmGraphContainer = document.getElementById(
    'modified-algorithm-partitioned-graph'
  );
  const modifiedAlgorithmNetworkData = {
    nodes: modifiedAlgorithmNodes,
    edges
  };
  new vis.Network(
    modifiedAlgorithmGraphContainer,
    modifiedAlgorithmNetworkData,
    networkOptions
  );

  document.querySelector('.kernighan-lin-result .target-function-value').textContent = kernighanLinInfo.target_function;
  document.querySelector('.kernighan-lin-result .time-to-complete').textContent = kernighanLinInfo.time;

  let partitionContainers = document.querySelectorAll('.kernighan-lin-result .partition-nodes');
  for (let partition = 0; partition < 3; partition++) {
    partitionContainers[partition].textContent = kernighanLinPartitions[partition].join(', ');
  }

  document.querySelector('.modified-algorithm-result .target-function-value').textContent = modifiedAlgorithmInfo.target_function;
  document.querySelector('.modified-algorithm-result .time-to-complete').textContent = modifiedAlgorithmInfo.time;

  partitionContainers = document.querySelectorAll('.modified-algorithm-result .partition-nodes');
  for (let partition = 0; partition < 3; partition++) {
    partitionContainers[partition].textContent = modifiedAlgorithmPartitions[partition].join(', ');
  }

});