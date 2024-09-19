import requests
import json
import locale

# Configuração do locale para formato de moeda brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


# Função para validar o formato do CNPJ
def validar_cnpj(cnpj):
    cnpj_limpo = cnpj.replace('.', '').replace('/', '').replace('-', '')
    if len(cnpj_limpo) == 14 and cnpj_limpo.isdigit():
        return cnpj_limpo
    else:
        return None


# Função para consultar a API de CNPJ
def consultar_cnpj(cnpj):
    url = f'https://open.cnpja.com/office/{cnpj}'

    try:
        resposta = requests.get(url)
        resposta.raise_for_status()  # Lança exceção para erros HTTP
        dados = resposta.json()
        if 'company' in dados:
            return dados
        else:
            print("CNPJ não encontrado ou sem informações na API.")
            return None

    except requests.exceptions.HTTPError as errh:
        print("Erro HTTP:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Erro de conexão:", errc)
    except requests.exceptions.Timeout as errt:
        print("Tempo de resposta excedido:", errt)
    except requests.exceptions.RequestException as err:
        print("Erro inesperado:", err)
    return None


# Função para exibir informações gerais do CNPJ
def exibir_informacoes_gerais(dados):
    print("\n=== Informações Gerais da Empresa ===")
    print(f"Nome: {dados['company']['name']}")
    print(f"CNPJ: {dados['taxId']}")
    print(f"Status: {dados['status']['text']}")
    print(f"Natureza Jurídica: {dados['company']['nature']['text']}")
    print(f"Capital Social: {locale.currency(dados['company']['equity'], grouping=True)}")
    print(f"Atividade Principal: {dados['mainActivity']['text']}")
    print(
        f"Endereço: {dados['address']['street']}, {dados['address']['number']} - {dados['address']['city']}/{dados['address']['state']}")
    print("===============================\n")


# Função para exibir sócios da empresa
def exibir_socios(dados):
    print("\n=== Sócios da Empresa ===")
    if 'members' in dados['company']:
        for membro in dados['company']['members']:
            print(f"Nome: {membro['person']['name']}")
            print(f"Função: {membro['role']['text']}")
            print(f"Idade Estimada: {membro['person']['age']}")
            print("===============================\n")
    else:
        print("Nenhum sócio encontrado.\n")


# Função para exibir atividades secundárias da empresa
def exibir_atividades_secundarias(dados):
    print("\n=== Atividades Secundárias ===")
    if 'sideActivities' in dados and dados['sideActivities']:
        for atividade in dados['sideActivities']:
            print(f"ID: {atividade['id']}")
            print(f"Descrição: {atividade['text']}")
            print("===============================\n")
    else:
        print("Nenhuma atividade secundária encontrada.\n")


# Menu de opções após a seleção do CNPJ
def menu_opcoes(dados):
    while True:
        print("\nMenu de Opções:")
        print("1 - Ver Informações Gerais")
        print("2 - Ver Sócios da Empresa")
        print("3 - Ver Atividades Secundárias")
        print("4 - Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            exibir_informacoes_gerais(dados)
        elif escolha == '2':
            exibir_socios(dados)
        elif escolha == '3':
            exibir_atividades_secundarias(dados)
        elif escolha == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


# Função principal para rodar no terminal
def main():
    while True:
        cnpj = input("Digite o CNPJ (somente números ou com formatação): ")
        cnpj_valido = validar_cnpj(cnpj)

        if cnpj_valido:
            dados = consultar_cnpj(cnpj_valido)
            if dados:
                menu_opcoes(dados)  # Exibe o menu de opções
                break
        else:
            print("CNPJ inválido! Certifique-se de que o CNPJ contém 14 dígitos numéricos.\nTente novamente.")


# Execução do programa
if __name__ == "__main__":
    main()
