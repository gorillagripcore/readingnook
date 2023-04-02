const pfp_dialog = document.getElementById('pfp_dialog');
const desc_dialog = document.getElementById('desc_dialog');
const updatefavbook_dialog = document.getElementById('updatefavbook_dialog');
const newfavbook_dialog = document.getElementById('newfavbook_dialog');

const openpfpDialogBtn = document.getElementById('openpfpDialogBtn');
const opendescDialogBtn = document.getElementById('opendescDialogBtn');
const open_updatefavbook_DialogBtn = document.getElementById('open_updatefavbook_DialogBtn');
const open_newfavbook_DialogBtn = document.getElementById('open_newfavbook_DialogBtn');



openpfpDialogBtn.addEventListener('click', () => {
  pfp_dialog.showModal();
});
  
opendescDialogBtn.addEventListener('click', () => {
  desc_dialog.showModal();
});

open_updatefavbook_DialogBtn.addEventListener('click', () => {
  updatefavbook_dialog.showModal();
});

open_newfavbook_DialogBtn.addEventListener('click', () => {
  newfavbook_dialog.showModal();
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

updatefavbook_dialog.addEventListener('click', (e) => {
  if (e.target === updatefavbook_dialog) {
    updatefavbook_dialog.close();
  }
});

newfavbook_dialog.addEventListener('click', (e) => {
  if (e.target === newfavbook_dialog) {
    newfavbook_dialog.close();
  }
});




