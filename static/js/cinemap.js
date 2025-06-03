 const seatMap = document.getElementById('seat-map');
        const numAssentosSelecionadosDisplay = document.getElementById('num-assentos-selecionados');
        const totalPriceDisplay = document.getElementById('total-price');
        const formVenda = document.getElementById('form-venda');
        const hiddenInputsContainer = document.getElementById('hidden-inputs-container');
        const quantityValidationMessage = document.getElementById('quantity-validation-message');

        const PRICES = {
            'inteira': 25.00,
            'meia': 12.50
        };

        let selectedSeatCodes = []; // Armazena apenas os códigos dos assentos selecionados
        let ticketQuantities = {
            'inteira': 0,
            'meia': 0
        };

        function updateCountsAndTotal() {
            // Atualiza os contadores de inteira/meia
            document.getElementById('count-inteira').textContent = ticketQuantities.inteira;
            document.getElementById('count-meia').textContent = ticketQuantities.meia;

            // Atualiza o número de assentos selecionados
            numAssentosSelecionadosDisplay.textContent = selectedSeatCodes.length;

            // Calcula e atualiza o preço total
            let total = (ticketQuantities.inteira * PRICES.inteira) + (ticketQuantities.meia * PRICES.meia);
            totalPriceDisplay.textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;

            // Validação visual (esconde/mostra a mensagem)
            validateQuantities();
        }

        function validateQuantities() {
            const totalTickets = ticketQuantities.inteira + ticketQuantities.meia;
            if (selectedSeatCodes.length === 0) {
                quantityValidationMessage.style.display = 'none'; // Não mostra mensagem se nenhum assento foi selecionado
            } else if (totalTickets !== selectedSeatCodes.length) {
                quantityValidationMessage.style.display = 'block'; // Mostra a mensagem de erro
            } else {
                quantityValidationMessage.style.display = 'none'; // Esconde a mensagem
            }
        }

        // Evento de clique no mapa de assentos
        seatMap.addEventListener('click', function(event) {
            const clickedSeat = event.target.closest('.seat');

            if (clickedSeat && !clickedSeat.classList.contains('occupied')) {
                const assentoCode = clickedSeat.dataset.assentoCode;

                if (clickedSeat.classList.contains('selected')) {
                    // Desselecionar assento
                    clickedSeat.classList.remove('selected');
                    selectedSeatCodes = selectedSeatCodes.filter(code => code !== assentoCode);
                } else {
                    // Selecionar assento
                    clickedSeat.classList.add('selected');
                    selectedSeatCodes.push(assentoCode);
                }
                updateCountsAndTotal(); // Atualiza tudo
            }
        });

        // Eventos para os botões de quantidade (+/-)
        document.querySelectorAll('.increase-quantity').forEach(button => {
            button.addEventListener('click', function() {
                const type = this.dataset.type;
                if ((ticketQuantities.inteira + ticketQuantities.meia) < selectedSeatCodes.length) {
                    ticketQuantities[type]++;
                    updateCountsAndTotal();
                } else {
                    alert('Você já atingiu o número máximo de ingressos para os assentos selecionados.');
                }
            });
        });

        document.querySelectorAll('.decrease-quantity').forEach(button => {
            button.addEventListener('click', function() {
                const type = this.dataset.type;
                if (ticketQuantities[type] > 0) {
                    ticketQuantities[type]--;
                    updateCountsAndTotal();
                }
            });
        });

        // Evento de submit do formulário
        formVenda.addEventListener('submit', function(event) {
            const totalTickets = ticketQuantities.inteira + ticketQuantities.meia;

            if (selectedSeatCodes.length === 0) {
                alert('Por favor, selecione pelo menos um assento.');
                event.preventDefault();
                return;
            }

            if (totalTickets !== selectedSeatCodes.length) {
                alert('O número de ingressos (inteira + meia) não corresponde ao número de assentos selecionados. Por favor, ajuste.');
                event.preventDefault();
                return;
            }

            // Preenche os inputs hidden para o Flask
            hiddenInputsContainer.innerHTML = ''; // Limpa antigos
            
            // Distribui os tipos de ingresso para os assentos
            let finalAssentosComTipo = [];
            let inteiraCount = ticketQuantities.inteira;
            let meiaCount = ticketQuantities.meia;

            // Atribui inteira primeiro, depois meia, ou como preferir
            for (let i = 0; i < selectedSeatCodes.length; i++) {
                const assentoCode = selectedSeatCodes[i];
                let type = '';
                if (inteiraCount > 0) {
                    type = 'inteira';
                    inteiraCount--;
                } else if (meiaCount > 0) {
                    type = 'meia';
                    meiaCount--;
                }
                finalAssentosComTipo.push({ code: assentoCode, type: type });

                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = `assentos_comprados[${assentoCode}]`; // Ex: assentos_comprados[A1]
                input.value = type; // Ex: inteira ou meia
                hiddenInputsContainer.appendChild(input);
            }
        });

        // Chamada inicial
        updateCountsAndTotal();