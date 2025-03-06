document.addEventListener("DOMContentLoaded", () => {
    // Função para rolar até a seção "Sobre Nós"
    const btnSobre = document.getElementById("btn-sobre");
    btnSobre.addEventListener("click", () => {
        document.getElementById("sobre-nos").scrollIntoView({ behavior: "smooth" });
    });

    // Função para rolar até a seção "Contatos"
    const btnContato = document.getElementById("btn-contato");
    btnContato.addEventListener("click", () => {
        document.getElementById("contatos").scrollIntoView({ behavior: "smooth" });
    });
});









