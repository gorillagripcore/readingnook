
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
// initialize the vote count for each poll box to 0
let voteCount = [0, 0];

// function to toggle the selected state of a poll box
function toggleSelection(pollBox) {
  // get the index of the poll box that was clicked
  let index = Array.from(pollBox.parentNode.children).indexOf(pollBox);
  
  // set the vote count for this poll box to 1 and reset the vote count for the other poll box to 0
  voteCount[index] = 1;
  voteCount[1 - index] = 0;
  
  // update the style of the poll boxes to reflect the selected state
  for (let i = 0; i < 2; i++) {
    let pollBox = document.getElementById(`poll_box_${i+1}`);
    pollBox.classList.toggle("selected", voteCount[i] > 0);
  }
}

// function to count the votes and display the results
function countVotes() {
  // get the vote count for each poll box
  let voteCount1 = voteCount[0];
  let voteCount2 = voteCount[1];

  // calculate the total number of votes
  let totalVotes = voteCount1 + voteCount2;

  // display the vote count for each poll box and the total number of votes
  document.getElementById("poll_box_1").innerHTML = `Vote count for poll box 1: ${voteCount1}`;
  document.getElementById("poll_box_2").innerHTML = `Vote count for poll box 2: ${voteCount2}`;
  document.getElementById("submitBtn").style.display = "none";
}












