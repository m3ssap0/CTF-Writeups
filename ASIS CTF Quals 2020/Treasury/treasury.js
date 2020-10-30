
import {Spinner} from './spin.js';

function createSpinner(target) {
  const opts = {
    lines: 8, // The number of lines to draw
    length: 10, // The length of each line
    width: 23, // The line thickness
    radius: 84, // The radius of the inner circle
    scale: 0.75, // Scales overall size of the spinner
    corners: 1, // Corner roundness (0..1)
    color: '#72ee38', // CSS color or array of colors
    fadeColor: 'transparent', // CSS color or array of colors
    speed: 0.7, // Rounds per second
    rotate: 25, // The rotation offset
    animation: 'spinner-line-fade-quick', // The CSS animation name for the lines
    direction: -1, // 1: clockwise, -1: counterclockwise
    zIndex: 2e9, // The z-index (defaults to 2000000000)
    className: 'spinner', // The CSS class to assign to the spinner
    top: '48%', // Top position relative to parent
    left: '50%', // Left position relative to parent
    shadow: '0 0 1px transparent', // Box-shadow for the lines
    position: 'absolute' // Element positioning
  };
  return new Spinner(opts).spin(target);
}

async function anexcerpt(book) {
  const modalEl = document.createElement('div');
  modalEl.style.width = '70%';
  modalEl.style.height = '50%';
  modalEl.style.margin = '100px auto';
  modalEl.style.backgroundColor = '#fff';
  modalEl.className = 'mui-panel';
  const header = document.createElement('h2');
  header.appendChild(document.createTextNode("An Excerpt From " + book.name));
  modalEl.appendChild(header);
  const loading = createSpinner(modalEl);
  // show modal
  mui.overlay('on', modalEl);

  const response = await fetch('books.php?type=excerpt&id=' + book.id);
  const bookExcerpt = await response.text();
  const txtHolder = document.createElement('div');
  txtHolder.className = 'mui-textfield mui--z2'
  const txt = document.createElement('textarea');
  txt.appendChild(document.createTextNode(bookExcerpt));
  txt.readOnly = true;
  txt.style.height = "100%";
  txtHolder.appendChild(txt);
  txtHolder.style.height = "70%";
  loading.stop();
  modalEl.appendChild(txtHolder);
}

function readonline(book) {
  window.open(book.link);
}

function createActionButton(cls, title, txt, callback) {
  const btn = document.createElement('button');
  btn.className = 'mui-btn mui-btn--fab ' + cls;
  btn.title = title;
  btn.appendChild(document.createTextNode(txt));
  btn.addEventListener('click', callback);
  return btn;
}

const spinner = createSpinner(document.getElementById("msg"));
window.addEventListener('load', loadBooksList);

async function loadBooksList() {
  const response = await fetch('books.php?type=list');
  const books = await response.json();
  const tbody = document.getElementById("books");
  for (const book of books) {
    const tr = document.createElement('tr');
    for (const key of ['name', 'author', 'year']) {
      const td = document.createElement('td');
      td.appendChild(document.createTextNode(book[key]));
      tr.appendChild(td);
    }
    const td = document.createElement('td');
    td.appendChild(createActionButton('mui-btn--primary', 'an excerpt', 'ae', function () {
      anexcerpt(book);
    }));
    td.appendChild(createActionButton('mui-btn--accent', 'read online', 'ro', function () {
      readonline(book);
    }));
    tr.appendChild(td);
    tbody.appendChild(tr);
  }
  spinner.stop();
  document.getElementById("msg").style = 'display: none;';
}

