
const pfp_dialog = document.getElementById('pfp_dialog');
const desc_dialog = document.getElementById('desc_dialog');
const update_fav_book_dialog = document.getElementById('update_fav_book_dialog');
const update_least_fav_book_dialog = document.getElementById('update_least_fav_book_dialog');
const quote_dialog = document.getElementById('quote_dialog');

const open_pfp_dialog_btn = document.getElementById('open_pfp_dialog_btn');
const open_desc_dialog_btn = document.getElementById('open_desc_dialog_btn');
const open_update_fav_book_dialog_btn = document.getElementById('open_update_fav_book_dialog_btn');
const open_update_least_fav_book_dialog_btn = document.getElementById('open_update_least_fav_book_dialog_btn');
const open_quote_dialog_btn = document.getElementById('open_quote_dialog_btn');

open_pfp_dialog_btn.addEventListener('click', () => {
  pfp_dialog.showModal();
});

open_desc_dialog_btn.addEventListener('click', () => {
  desc_dialog.showModal();
});

open_update_fav_book_dialog_btn.addEventListener('click', () => {
  update_fav_book_dialog.showModal();
});

open_update_least_fav_book_dialog_btn.addEventListener('click', () => {
  update_least_fav_book_dialog.showModal();
});

open_quote_dialog_btn.addEventListener('click', () => {
  quote_dialog.showModal();
});


pfp_dialog.addEventListener('click', (e) => {
  if (e.target === pfp_dialog) {
    pfp_dialog.close();
  }
});

desc_dialog.addEventListener('click', (e) => {
  if (e.target === desc_dialog) {
    desc_dialog.close();
  }
});

update_fav_book_dialog.addEventListener('click', (e) => {
  if (e.target === update_fav_book_dialog) {
    update_fav_book_dialog.close();
  }
});

update_least_fav_book_dialog.addEventListener('click', (e) => {
  if (e.target === update_least_fav_book_dialog) {
    update_least_fav_book_dialog.close();
  }
});

quote_dialog.addEventListener('click', (e) => {
  if (e.target === quote_dialog) {
    quote_dialog.close();
  }
});

//Poll counts
function toggleSelection(pollBox) {
  var pollBoxes = document.getElementsByClassName('poll_box');
  for (var i = 0; i < pollBoxes.length; i++) {
    pollBoxes[i].classList.remove('selected');
  }
  pollBox.classList.add('selected');
}

function countVotes() {
  var selectedPollBox = document.querySelector('.poll_box.selected');
  if (selectedPollBox) {
    var selectedPollBoxId = selectedPollBox.id;
    var pollBoxNumber = parseInt(selectedPollBoxId.split('_')[2]);
    console.log('Selected Poll Box:', pollBoxNumber);
  } else {
    console.log('No poll box selected.');
  }
}

document.getElementById('pollForm').addEventListener('submit', function (event) {
  event.preventDefault();
  countVotes();
});





