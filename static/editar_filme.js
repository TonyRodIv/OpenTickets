document.addEventListener('DOMContentLoaded', function () {
    let todosOsFilmes = [];
    fetch('/adm/api/filmes') // Faz a requisição pra rota Flask
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erro HTTP! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(filmes => {
        console.log('Filmes carregados com sucesso:', filmes);
        todosOsFilmes = filmes;
    })
    .catch(error => {
        console.error('Flopou na hora de carregar os filmes:', error);
    });
    tituloOriginal = document.getElementById('titulo_original');
    tituloNovo = document.getElementById('titulo');
    duracaoNovo = document.getElementById('duracao');
    generoNovo = document.getElementById('genero');
    classificacaoNovo = document.getElementById('classificacao');
    tituloOriginal.addEventListener('change', function () {
        console.log('Título original alterado:', tituloOriginal.value);
        todosOsFilmes.forEach(filme => {
            if (filme.titulo === tituloOriginal.value) {
                console.log('Filme encontrado:', filme);
                tituloNovo.value = filme.titulo;
                duracaoNovo.value = filme.duracao;
                generoNovo.value = filme.genero;
                classificacaoNovo.value = filme.classificacao;
                
            }
        });
    });
});