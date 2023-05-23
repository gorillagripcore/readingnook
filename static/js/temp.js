const botm_dialog = document.getElementById('botm_dialog');
const date_dialog = document.getElementById('date_dialog');
const location_dialog = document.getElementById('location_dialog');
const bcp_dialog = document.getElementById('bcp_dialog');
const club_desc_dialog = document.getElementById('club_desc_dialog');

const open_botm_dialog_btn = document.getElementById('open_botm_dialog_btn');
const open_date_dialog_btn = document.getElementById('open_date_dialog_btn');
const open_location_dialog_btn = document.getElementById('open_location_dialog_btn');
const open_bcp_dialog_btn = document.getElementById('open_bcp_dialog_btn');
const open_club_desc_dialog_btn = document.getElementById('open_club_desc_dialog_btn');

open_botm_dialog_btn.addEventListener('click', () => {
    botm_dialog.showModal();
});

open_date_dialog_btn.addEventListener('click', () => {
    date_dialog.showModal();
});

open_location_dialog_btn.addEventListener('click', () => {
    location_dialog.showModal();
});

open_bcp_dialog_btn.addEventListener('click', () => {
    bcp_dialog.showModal();
});

open_club_desc_dialog_btn.addEventListener('click', () => {
    club_desc_dialog.showModal();
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

bcp_dialog.addEventListener('click', (e) => {
    if (e.target === bcp_dialog) {
        bcp_dialog.close();
    }
});

club_desc_dialog.addEventListener('click', (e) => {
    if (e.target === club_desc_dialog) {
        club_desc_dialog.close();
    }
});