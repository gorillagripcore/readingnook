const botm_dialog = document.getElementById('botm_dialog');
const date_dialog = document.getElementById('date_dialog');
const location_dialog = document.getElementById('location_dialog');

const open_botm_dialog_btn = document.getElementById('open_botm_dialog_btn');
const open_date_dialog_btn = document.getElementById('open_date_dialog_btn');
const open_location_dialog_btn = document.getElementById('open_location_dialog_btn');

open_botm_dialog_btn.addEventListener('click', () => {
    botm_dialog.showModal();
});

open_date_dialog_btn.addEventListener('click', () => {
    date_dialog.showModal();
});

open_location_dialog_btn.addEventListener('click', () => {
    location_dialog.showModal();
});

botm_dialog.addEventListener('click', (e) => {
    if (e.target === botm_dialog) {
        botm_dialog.close();
    }
});

date_dialog.addEventListener('click', (e) => {
    if (e.target === date_dialog) {
        date_dialog.close();
    }
});

location_dialog.addEventListener('click', (e) => {
    if (e.target === location_dialog) {
        location_dialog.close();
    }
});
