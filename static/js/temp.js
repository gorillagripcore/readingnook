const botm_dialog = document.getElementById('botm_dialog');

const open_botm_dialog_btn = document.getElementById('open_botm_dialog_btn');

open_botm_dialog_btn.addEventListener('click', () => {
    botm_dialog.showModal();
});

botm_dialog.addEventListener('click', (e) => {
    if (e.target === botm_dialog) {
        botm_dialog.close();
    }
});