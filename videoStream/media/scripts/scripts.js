// script.js

const dropArea = document.getElementById('drop-area');
const fileElem = document.getElementById('id_video_file');
const fileList = document.getElementById('file-list');
const continueBtn = document.getElementById('continueBtn');
const videoDetails = document.getElementById('videoDetails');
const videoForms = document.getElementById('videoForms');
const submitBtn = document.getElementById('submit-button');

let uploadedFiles = [];

// Highlight drop area when dragging over
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

// Highlight drop area when dragging over
['dragenter', 'dragover'].forEach(eventName => {
  dropArea.addEventListener(eventName, highlight, false);
});

// Remove highlight when dragging leaves drop area
['dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, unhighlight, false);
});

function highlight() {
  dropArea.classList.add('highlight');
}

function unhighlight() {
  dropArea.classList.remove('highlight');
}

// Handle dropped files
dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
  let dt = e.dataTransfer;
  let files = dt.files;

  handleFiles(files);
}

// Handle files selected via file input
fileElem.addEventListener('change', handleFilesSelected, false);

function handleFilesSelected(e) {
  let files = e.target.files;

  handleFiles(files);
}

// Display the list of files
function handleFiles(files) {
  fileList.innerHTML = '';
  uploadedFiles = [];

  for (let i = 0; i < files.length; i++) {
    let file = files[i];
    if (file.type.startsWith('video/')) {
      uploadedFiles.push(file);
      let listItem = document.createElement('div');
      listItem.textContent = `${file.name} (${formatBytes(file.size)})`;
      fileList.appendChild(listItem);
    }
  }

  if (uploadedFiles.length > 0) {
    continueBtn.style.display = 'block';
    continueBtn.addEventListener('click', showVideoDetailsForm);
  } else {
    continueBtn.style.display = 'none';
  }

  if (fileList.children.length === 0) {
    let p = document.createElement('p');
    p.textContent = 'No videos uploaded yet';
    fileList.appendChild(p);
  }
}

// Show video details form
function showVideoDetailsForm() {
  videoForms.innerHTML = '';

  dropArea.style.display = 'none';
  continueBtn.style.display = 'none';
  fileList.style.display = 'none';
  submitBtn.style.display = 'block';

  uploadedFiles.forEach((file, index) => {
    let formDiv = document.createElement('div');
    formDiv.innerHTML = `
      <div class="form-container">
          <h4>${file.name}</h4>
          <label for="title">Title:</label>
          <input class="form-control" type="text" id="title" name="title" required><br><br>
          <label for="description">Description:</label><br>
          <textarea class="form-control" id="description" name="description" rows="4" cols="50" required></textarea><br><br>
          <label for="description">Thumbnail:</label><br>
          <input class="form-control" type="file" id="thumbnail" accept="image/*" name="thumbnail">
         </div>
    `;
    videoForms.appendChild(formDiv);
  });

  videoDetails.style.display = 'block';
}


// Helper function to format file size
function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}
