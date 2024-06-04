// mobile menu dropdown
const burguerIcon = document.querySelector('#burguer');
const navbarMenu = document.querySelector('#nav-links');

burguerIcon.addEventListener('click', () => {
    navbarMenu.classList.toggle('is-active');
})