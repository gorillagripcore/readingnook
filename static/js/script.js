
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
// initialize the vote counts
var voteCount1 = 0;
var voteCount2 = 0;

// function to toggle the selection of a poll box
function toggleSelection(pollBox) {
  // remove the selected class from all poll boxes
  var pollBoxes = document.getElementsByClassName("poll_box");
  for (var i = 0; i < pollBoxes.length; i++) {
    pollBoxes[i].classList.remove("selected");
  }

  // add the selected class to the clicked poll box
  pollBox.classList.add("selected");
}

// function to count the votes
function countVotes() {
  // get the selected poll box
  var selectedPollBox = document.getElementsByClassName("selected")[0];

  // increment the vote count for the selected poll box
  if (selectedPollBox.id === "poll_box_1") {
    voteCount1++;
  } else if (selectedPollBox.id === "poll_box_2") {
    voteCount2++;
  }

  // display the vote counts
  alert("Vote count for poll box 1: " + voteCount1 + "\nVote count for poll box 2: " + voteCount2);
}

// add event listeners to the poll boxes
var pollBoxes = document.getElementsByClassName("poll_box");
for (var i = 0; i < pollBoxes.length; i++) {
  pollBoxes[i].addEventListener("click", function() {
    toggleSelection(this);
  });
}

// add event listener to the submit button
var submitButton = document.getElementById("submitBtn");
submitButton.addEventListener("click", function() {
  countVotes();
});










