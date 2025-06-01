document.addEventListener('DOMContentLoaded', function () {
    let todosOsFilmes = [];
    let todasAsSalas = [];
    fetch('/adm/api/dados') // Faz a requisição pra rota Flask
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro HTTP! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(dados => {
            console.log('Dados recebidos:', dados);
            todosOsFilmes = dados.filmes; // Pegando os filmes do objeto 'dados'
            todasAsSalas = dados.salas;
        })
        .catch(error => {
            console.error('Deu ruim fio:', error);
        });

    tituloOriginal = document.getElementById('titulo_original');

    tituloNovo = document.getElementById('titulo');
    duracaoNovo = document.getElementById('duracao');
    generoNovo = document.getElementById('genero');
    classificacaoNovo = document.getElementById('classificacao');

    tituloOriginal.addEventListener('change', function () {
        console.log('Filme selecionado:', tituloOriginal.value);
        todasAsSalas.forEach(sala => {
            const salaCheckbox = document.getElementById(`sala_${sala.numero}`);
            if (salaCheckbox) {
                salaCheckbox.checked = false; // Desmarca todas as salas
            }
        });
        todosOsFilmes.forEach(filme => {
            if (filme.titulo === tituloOriginal.value) {
                console.log('Filme encontrado:', filme);
                tituloNovo.value = filme.titulo;
                duracaoNovo.value = filme.duracao;
                generoNovo.value = filme.genero;
                classificacaoNovo.value = filme.classificacao;
                filme.salas.forEach(sala => {
                    const salaCheckbox = document.getElementById(`sala_${sala}`);
                    if (salaCheckbox) {
                        salaCheckbox.checked = true;
                    }
                });
            }
        });
    });
});