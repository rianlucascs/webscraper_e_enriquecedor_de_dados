# Webscraper e Enriquecedor de Dados

![Texto Alternativo](https://github.com/rianlucascs/webscraper_e_enriquecedor_de_dados/blob/main/imagem.jpg)

Este projeto apresenta um software dedicado à automação da coleta de dados da web. Utilizando o nome da empresa e o domínio fornecidos, ele extrai informações relevantes e realiza uma filtragem para garantir a precisão dos dados obtidos. Essa abordagem simplifica significativamente o processo de obtenção de dados da internet.

# Situação problema

Buscar na web o CNPJ a partir do nome da empresa e do domínio fornecidos, e determinar qual dos CNPJs encontrados está correto.

## Formato dos dados

| empresa                   | domínio             | CNPJ   | razão social   |
|---------------------------|---------------------|--------|----------------|
| Uranus2 Comunicação       | uranus2.com.br      | x      | x              |
| MBM Comunicação Visual    | mbmvisual.com.br    | x      | x              |

# Descrição dos processos do Script

**Biblioteca utilizada para webscraping**

    Selenium

A busca do cnpj é feita por meio do Google e do Registro.br

## Google.com

1) Faz a busca no navegador do Google 'CNPJ {nome da empresa}'.
2) Armazenar as informações de todas as classes HTML 'MjjYud' - Essas que contem informações relacionadas ao CNPJ buscado.

    **Formato da informação contida na classe 'MjjYud'**

        Abase 01661685000180 Brasília
        CNPJ Biz
        https://cnpj.biz › Empresas › DF › Brasília
        A empresa Abase de CNPJ 01.661.685/0001-80, fundada em 06/08/1985 e com razão social Associacao Brasileira dos Sebrae Estaduais, está localizada na cidade ...

        Abase | Associacao Brasileira Dos Sebrae Estaduais
        CNPJ.info
        http://cnpj.info › ABASE-ASSOCIACAO-BRASILEIRA-...
        Abase | Associacao Brasileira Dos Sebrae Estaduais · CNPJ e Endereços · 94.30-8-00 - Atividades de associações de defesa de direitos sociais · 94.93-6-00 - ...


    ## Busca do CNPJ

    1) **Método A**
        1) Buscar o nome da empresa de cada elemento do arquivo que foi armazenado - Cade elemento é separado por '\n'.
        2) Se encontrar o nome então buscar o CNPJ.
        3) Armazenar em uma lista os CNPJs encontrados.

    2) **Método B**
        1) Se não encontrar nenhum CNPJ com o 'Método A', então buscar todos os CNPJs da página e armazená-los em uma lista, independentemente se a classe não contiver o nome da empresa.

    Essses processos se repetem em cada elemento da pagina que estava dentro da classe 'MjjYud'.
    
    Antes de passar para o 'Método B' todos os caracteres dos textos das classes e do nome da empresa são removidos, e a busca é feita novamente.
    

## Registro.br
1) Buscar o domínio no site Registro.br.
2) Armazenar todo o HTML da página.
3) Busca diretamente a informação que contem o CNPJ.
4) Armazena a informação.

## Validação dos CNPJs encontrados

1) Define a frequência dos CNPJs encontrados na busca feita pelo Google e seleciona apenas os CNPJs da matriz - 0001.

    **Formato dos CNPJs encontrados**
    
        [00.286.576/0001-67, 00.286.576/0001-67, 00.286.576/0001-67, 00.286.576/0001-67, 00.000.000/0001-21, 00.000.000/0001-21, 00.000.000/0001-21, 00.000.000/0001-31]   
    
    - 00.286.576/0001-67: frequência = 4
    - 00.000.000/0001-21: frequência = 3
    - 00.000.000/0001-31: frequência = 1
    
2) É selecionado os dois CNPJs que tiveram maior frequência na busca feita no Google e o CNPJ que foi encontrado na busca feita pelo domínio.

3) É feita a busca da razão social desses três CNPJs.

    **Sites onde essa busca é relizada**

        cadastro empresa
        casa dos dados
        econo data
        informe cadastral
        receita federal

    O acesso a cada site é feito de forma sequencial, o que aumenta o tempo de acesso a cada site sem sobrecarregá-lo e sem causar bloqueios de acesso.

    Especificamente no caso da 'Receita Federal', o limite de requisições de consulta é respeitado, sendo 3 por minuto.

4) É feita o cálculo da similaridade do nome da empresa informado com a razão social encontrada dos três CNPJs.

    **Biblioteca utilizada**

        difflib

5) É selecionado o CNPJ com maior similaridade como resultado final.

    **Formato do resultado**

        [cnpj, nome empresa]

# Observações

Tempo para desenvolvimento: três meses.

Uma das principais dificuldades deste projeto foi concluir que o CNPJ mais frequente na página de busca resulta em maior precisão. Durante o desenvolvimento, explorei outras abordagens semelhantes ao 'Método A', que envolve a busca por um nome de empresa similar ao informado, ou seja, por aproximação. O método encontrado é simples e eficaz, em comparação com outros.

Desenvolvi este projeto completamente, sem supervisão de outro desenvolvedor.

A maior quantidade de dados aplicado a esse script foi de 50.000 empresas.

Tempo de processamento 1000 empresas a cada 1 hora e 20 minutos =~.

O código main de execução esta disponível para visualização nessa pasta.

## Contato
> Rian Lucas da Cunha Silva

> rianlucasjp@gmail.com

> www.linkedin.com/in/rian-lucas
