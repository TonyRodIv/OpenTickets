document.addEventListener('DOMContentLoaded', function () {
    const cpfDisplay = document.getElementById('cpfDisplay');
    const numberButtons = document.querySelectorAll('[data-number]');
    const deleteButton = document.querySelector('[data-key="del"]');
    const continueButton = document.getElementById('continueCPFbtn'); 

    function formatarCPF(value) {
        value = value.replace(/\D/g, '');
        if (value.length > 11) {
            value = value.slice(0, 11);
        }
        if (value.length > 9) {
            value = value.replace(/^(\d{3})(\d{3})(\d{3})(\d{2})$/, '$1.$2.$3-$4');
        } else if (value.length > 6) {
            value = value.replace(/^(\d{3})(\d{3})(\d{3})$/, '$1.$2.$3');
        } else if (value.length > 3) {
            value = value.replace(/^(\d{3})(\d{3})$/, '$1.$2');
        }
        return value;
    }

    function checkCpfCompletion() {
        const rawCpf = cpfDisplay.value.replace(/\D/g, '');
        if (rawCpf.length === 11) {
            continueButton.disabled = false; 
            console.log('CPF completo:', rawCpf);
        } else {
            continueButton.disabled = true; 
        }
    }

    // Adiciona evento de clique para os botões numéricos
    numberButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (cpfDisplay.value.replace(/\D/g, '').length < 11) {
                cpfDisplay.value += button.dataset.number;
                cpfDisplay.value = formatarCPF(cpfDisplay.value);
            }
            checkCpfCompletion(); 
        });
    });

    deleteButton.addEventListener('click', () => {
        let currentCpf = cpfDisplay.value.replace(/\D/g, '');
        if (currentCpf.length > 0) {
            currentCpf = currentCpf.slice(0, -1);
            cpfDisplay.value = formatarCPF(currentCpf);
        }
        checkCpfCompletion(); 
    });

    continueButton.addEventListener('click', () => {
        if (!continueButton.disabled) {
            window.location.href = '/vend/escolher_filme'; 
        }
    });
    checkCpfCompletion();
});