console.log("Script JavaScript carregado.");
document.addEventListener('DOMContentLoaded', (event) => {
    console.log("DOM completamente carregado e analisado.");
    var button = document.getElementById('btn-sobre');
    if (button) {
        console.log("Botão 'Sobre Nós' encontrado.");
        button.addEventListener('click', function(event) {
            event.preventDefault();
            console.log("Botão 'Sobre Nós' clicado.");
            var section = document.getElementById('nossa-historia');
            if (section) {
                console.log("Seção 'Nossa História' encontrada.");
                section.classList.remove('hidden');
                section.classList.add('show');
                section.scrollIntoView({ behavior: 'smooth' });
                console.log("Classe 'show' adicionada e rolagem feita.");
            } else {
                console.log("Seção 'Nossa História' não encontrada.");
            }
        });
    } else {
        console.log("Botão 'Sobre Nós' não encontrado.");
    }
});











