document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('cnpjForm');
    const resultContainer = document.getElementById('resultContainer');
    const cnpjInput = document.getElementById('cnpjInput');

    // Elementos HTML para preencher com os dados da empresa
    const companyName = document.getElementById('companyName');
    const companyCnpj = document.getElementById('companyCnpj');
    const companyStatus = document.getElementById('companyStatus');
    const companyEquity = document.getElementById('companyEquity');
    const companyNature = document.getElementById('companyNature');
    const companyActivity = document.getElementById('companyActivity');
    const companyAddress = document.getElementById('companyAddress');
    const companyPhone = document.getElementById('companyPhone');
    const companyEmail = document.getElementById('companyEmail');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const cnpj = cnpjInput.value;

        if (cnpj.length === 14 && /^\d+$/.test(cnpj)) {
            fetchCnpjData(cnpj);
        } else {
            alert("CNPJ inválido. Certifique-se de inserir 14 dígitos numéricos.");
        }
    });

    function formatCurrency(value) {
        // Configura o formatador para o Brasil
        const formatter = new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
        return formatter.format(value);
    }

    function fetchCnpjData(cnpj) {
        const apiUrl = `https://open.cnpja.com/office/${cnpj}`;

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                if (data && data.company) {
                    // Preenche as informações da empresa no card
                    companyName.textContent = data.company.name;
                    companyCnpj.textContent = data.taxId;
                    companyStatus.textContent = data.status.text;
                    companyEquity.textContent = formatCurrency(data.company.equity);
                    companyNature.textContent = data.company.nature.text;
                    companyActivity.textContent = data.mainActivity.text;

                    companyAddress.textContent = `${data.address.street}, ${data.address.number}, ${data.address.city}/${data.address.state}`;
                    companyPhone.textContent = `(${data.phones[0].area}) ${data.phones[0].number}`;
                    companyEmail.textContent = data.emails[0].address;

                    // Exibe o container de resultado
                    resultContainer.style.display = 'block';
                } else {
                    alert("CNPJ não encontrado.");
                }
            })
            .catch(error => {
                console.error('Erro ao consultar a API:', error);
                alert('Erro ao consultar o CNPJ. Tente novamente mais tarde.');
            });
    }
});
