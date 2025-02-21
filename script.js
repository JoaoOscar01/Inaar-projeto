document.getElementById('btn-sobre').addEventListener('click', function(event) {
    event.preventDefault();
    var section = document.getElementById('sobre-nos');
    section.classList.remove('hidden');
    section.classList.add('show');
    section.scrollIntoView({ behavior: 'smooth' });
});








