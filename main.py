from utils.generico import (
    path_raiz,
    estabelecer_caminho_inteligente_script,
    leitura_dados,
    existe,
    path_nome_arquivo,
    leitura,
    sistema_parametros
    )

from utils import (
    dados_estruturais,
    nomes_arquivos,
    metodos_confirmacao,
    comparacao
    )

from asyncio import (
    create_task, 
    gather, 
    run
    )

from scraping.busca.google import (
    google, 
    google_armazenamento,
    google_localizador
    )
from scraping.busca.registrobr import (
    registrobr, 
    registrobr_armazenamento,
    registrobr_localizador
    )

from utils.nomes_arquivos import (
    pagina_google,
    pagina_registro
    )

from scraping.confirmacao import master
from pandas import DataFrame

def acoes_primarias_sistema():
    core_path = estabelecer_caminho_inteligente_script(path_raiz(['temp']), path_raiz([]))
    return [core_path, '']

async def busca_google(empresa, core_path):
    """Pesquisa no google o nome da 'CNPJ empresa' e salva o html da pagina."""
    if empresa == 'nan':
        return None
    if existe(f'{core_path}registros\\google\\{pagina_google(empresa)}'):
        return None
    pagina = google.__init__(empresa)
    google_armazenamento.__init__(pagina, empresa, core_path)
    return None

async def busca_registrobr(dominio, core_path):
    """Pesquisa no registro br o dominio e salva o html da pagina"""
    if dominio == 'nan':
        return None
    if existe(f'{core_path}registros\\registrobr\\{pagina_registro(dominio)}'):
        return None
    pagina = registrobr.__init__(dominio)
    registrobr_armazenamento.__init__(pagina, dominio, core_path)
    return None

def monta_dados(empresa, dominio, core_path):
    """Localiza no html da pagina os CNPJ."""
    bar = sistema_parametros()[2]
    core_path = f'{core_path}registros{bar}'
    caminho_google_arquivo = f'{core_path}google{bar}{nomes_arquivos.pagina_google(empresa)}'
    if existe(caminho_google_arquivo):
        google_cnpj = google_localizador.__init__(leitura(caminho_google_arquivo, 'read'), empresa)
    else:
        google_cnpj = 'nan'
    caminho_registro_arquivo = f'{core_path}registrobr{bar}{nomes_arquivos.pagina_registro(dominio)}'
    if existe(caminho_registro_arquivo):
        registrobr_cnpj = registrobr_localizador.__init__(leitura(caminho_registro_arquivo, 'read'))
    else:
        registrobr_cnpj = 'nan'
    result_busca = [google_cnpj, registrobr_cnpj]
    return result_busca

def confirma_dados(empresa, result_busca, core_path):
    """Selecione os dois CNPJ de maior frequencia encontrados no Google e, a partir deles, busque a razao
    social. Repita o processo de buscar a razao social com o CNPJ do Registro.br. Em seguida, compare a razao
    social dos tres CNPJ  com o nome da empresa informado. A razao social com maior similaridade estatistica 
    em ralacao ao   nome da empresa informado e selecionada como resultado."""
    google_maior_frequencia = metodos_confirmacao.maior_frequencia(result_busca)
    confirmacao1 = 'nan', 'nan'
    confirmacao2 = 'nan', 'nan'
    confirmacao3 = 'nan', 'nan'
    if len(google_maior_frequencia) >= 1: # google maior frequencia posicao 1
        confirmacao1 = master.__init__(google_maior_frequencia[0], core_path), google_maior_frequencia[0]
    if len(google_maior_frequencia) >= 2: # google maior frequencia posicao 2
        confirmacao2 = master.__init__(google_maior_frequencia[1], core_path), google_maior_frequencia[1]
    if result_busca[1] != 'nan': # registro
        confirmacao3 = master.__init__(result_busca[1], core_path), result_busca[1]
    maior_similaridade = comparacao.__init__(empresa, confirmacao1, confirmacao2, confirmacao3)
    return maior_similaridade

async def main():
    aps = acoes_primarias_sistema()
    core_path = aps[0]
    tabela, data_path = leitura_dados(caixa_de_escolha=True, fillna='nan',
                           log_caminho=f'{core_path}temp\\data_path.txt')
    
    __dados_estruturais__ = dados_estruturais.__init__(tabela)

    lista_data = [[], [], [], []]
    for empresa, dominio in __dados_estruturais__.values:
        await gather(
            create_task(busca_google(empresa, core_path)),
            create_task(busca_registrobr(dominio, core_path))
        )
        result_busca = monta_dados(empresa, dominio, core_path)
        result_confirma = confirma_dados(empresa, result_busca, core_path)
        lista_data[0].append(empresa)
        lista_data[1].append(dominio)
        lista_data[2].append(result_confirma[0])
        lista_data[3].append(result_confirma[1])

    df = DataFrame(lista_data,
                    index=['empresa_informado', 
                           'dominio_informado', 
                           'razao_social_encontrado', 
                           'cnpj_encontrado'
                           ]).T
    
    nome_arquivo_data = path_nome_arquivo(data_path)
    df.to_excel(f'resultado {nome_arquivo_data}.xlsx')

if __name__ == '__main__':        
    run(main())