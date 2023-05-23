
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
document.getElementById("submitBtn").addEventListener("click", function() {
  // Get the selected poll option
  var selectedOption = document.querySelector(".poll_box.selected");

  if (selectedOption) {
    // Get the ID of the selected poll box
    var selectedBoxId = selectedOption.getAttribute("id");

    // Remove the "poll_box_" prefix to get the selected option number
    var selectedOptionNumber = selectedBoxId.replace("poll_box_", "");

    // Display the selected option in the console (you can modify this part to perform other actions)
    console.log("Selected option: " + selectedOptionNumber);
  } else {
    // No option selected, display an error message (you can modify this part to perform other actions)
    console.log("Please select an option.");
  }
});

// Event listener for the poll boxes
var pollBoxes = document.querySelectorAll(".poll_box");
pollBoxes.forEach(function(box) {
  box.addEventListener("click", function() {
    // Remove the "selected" class from all poll boxes
    pollBoxes.forEach(function(box) {
      box.classList.remove("selected");
      box.classList.remove("selected-box"); // Remove the border highlight class from all poll boxes
    });

    // Add the "selected" class to the clicked poll box
    this.classList.add("selected");
    this.classList.add("selected-box"); // Add the border highlight class to the selected poll box
  });
});

function selectPollBox(pollBox) {
  var pollBoxes = document.querySelectorAll(".poll_box");
  pollBoxes.forEach(function(box) {
    box.classList.remove("selected");
  });

  pollBox.classList.add("selected");
}




