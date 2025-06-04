document.addEventListener('DOMContentLoaded', function () {
    let todosOsFilmes = [];
    let todasAsSalas = [];
    const tituloOriginalSelect = document.getElementById('titulo_original');
    const tituloNovoInput = document.getElementById('titulo');
    const duracaoNovoInput = document.getElementById('duracao');
    const generoNovoSelect = document.getElementById('genero');

    fetch('/adm/api/dados')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro HTTP! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(dados => {
            console.log('Dados recebidos:', dados);
            todosOsFilmes = dados.filmes;
            todasAsSalas = dados.salas; 

            tituloOriginalSelect.addEventListener('change', function () {
                const tituloSelecionado = this.value;
                let filmeEscolhido = null;

                todasAsSalas.forEach(sala => {
                    const salaCheckbox = document.getElementById(`sala_${sala.numero}`);
                    const parentDiv = salaCheckbox ? salaCheckbox.closest('div') : null;
                    if (salaCheckbox && parentDiv) {
                        salaCheckbox.checked = false;
                        salaCheckbox.disabled = false;
                        parentDiv.style.display = '';
                    }
                });


                if (tituloSelecionado) {
                    filmeEscolhido = todosOsFilmes.find(f => f.titulo === tituloSelecionado);
                }

                if (filmeEscolhido) {
                    console.log('Filme encontrado:', filmeEscolhido);
                    tituloNovoInput.value = filmeEscolhido.titulo;
                    duracaoNovoInput.value = filmeEscolhido.duracao;
                    generoNovoSelect.value = filmeEscolhido.genero;
                    const radiosClassificacao = document.querySelectorAll('input[name="classificacao"]');
                    radiosClassificacao.forEach(radio => {
                        radio.checked = (radio.value === filmeEscolhido.classificacao);
                    });

                    const salasOcupadasPorOutros = new Set();
                    todosOsFilmes.forEach(outroFilme => {
                        if (outroFilme.titulo !== filmeEscolhido.titulo) {
                            outroFilme.salas.forEach(salaNum => salasOcupadasPorOutros.add(String(salaNum)));
                        }
                    });

                    todasAsSalas.forEach(sala => {
                        const salaNumeroStr = String(sala.numero);
                        const salaCheckbox = document.getElementById(`sala_${salaNumeroStr}`);
                        const parentDiv = salaCheckbox ? salaCheckbox.closest('div') : null;

                        if (!salaCheckbox || !parentDiv) return;

                        const pertenceAoFilmeEscolhido = filmeEscolhido.salas.map(s => String(s)).includes(salaNumeroStr);
                        const ocupadaPorOutro = salasOcupadasPorOutros.has(salaNumeroStr);

                        if (pertenceAoFilmeEscolhido) {
                            salaCheckbox.checked = true;
                            salaCheckbox.disabled = false;
                            parentDiv.style.display = ''; // Garante que está visível
                        } else if (ocupadaPorOutro) {
                            salaCheckbox.checked = false;
                            salaCheckbox.disabled = true; 
                            parentDiv.style.display = 'none'; 
                        } else {
                            salaCheckbox.checked = false;
                            salaCheckbox.disabled = false;
                            parentDiv.style.display = '';
                        }
                    });

                } else {
                    tituloNovoInput.value = '';
                    duracaoNovoInput.value = '';
                    generoNovoSelect.value = '';
                    document.querySelectorAll('input[name="classificacao"]').forEach(radio => radio.checked = false);
                }
            });
        })
        .catch(error => {
            console.error('Deu ruim no fetch inicial, fml:', error);
        });
});