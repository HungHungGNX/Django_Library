const modal = document.querySelector('.modal');
const modal_btn_close = document.querySelector('.modal-btn-close');
const btn_login = document.querySelector('.banner-btn');
const modal_contanier = document.querySelector('.cookiesContent')
const btn_admin = document.querySelector('.btn-admin')
const btn_user = document.querySelector('.btn-user')


function hiddenModal() {
    modal.classList.remove('open');
}

function showModal() {
    modal.classList.add('open');
}



modal_btn_close.addEventListener('click', function() {
    hiddenModal();
})

btn_login.addEventListener('click', function() {
    showModal();
})

modal.addEventListener('click', function() {
    hiddenModal();
})


modal_contanier.addEventListener('click', function(event) {
    event.stopImmediatePropagation();
})

btn_admin.addEventListener('click', function(event) {
    window.location.href = '/adminlogin'
})
btn_user.addEventListener('click', function(event) {
    window.location.href = '/studentlogin'
})