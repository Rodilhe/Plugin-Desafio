# Plugin-Desafio

## Sumário
1. Proposta do Desafio
2. Principais Obstáculos
3. Preparação do Ambiente
4. Execução do Gripy
5. Apresentação do Plugin "Desafio"

## Proposta do Desafio

1. **Instalação e operação básica do GRIPy;**
2. **Construção de um plugin simples para o GRIPy com os seguintes requisitos:**
   - Leitura de um dado de poço;
   - Aplicação de uma operação matemática básica;
   - Escrita do resultado da operação matemática;
3. **Estruturação dos dados do GRIPy em uma estrutura de projeto gerenciável com os seguintes requisitos:**
   - Estruturação do projeto em pasta específica;
   - Estruturação do metadados utilizando o SQLite;
   - Importação dos dados de I/O do GRIPy e armazenamento na estrutura do projeto;
   - Funcionalidades para exportação e importação de um projeto.

## Preparação do Ambiente

### Requisitos do Gripy (para Windows ou Linux)
1. Python 3.6 (ou maior)
2. NumPy 1.17.2 (ou maior)
3. Matplotlib 3.1.1 (ou maior)
4. SciPy 1.2.1 (não pode ser maior)
5. scikit-learn 0.21.3 (ou maior)
6. PyMC 3.6 (ou maior)
7. wxPython 4.0.0 (ou maior)

### Passos para execução do Gripy:
1. Instalar o **ANACONDA.NAVIGATOR**;
2. Criar novo ambiente com versão Python > 3.7;
3. Instalar biblioteca **Conda**;
4. Na aba Home, executar **VS Code** a partir do novo ambiente criado;
5. Abrir o diretório do projeto baixado no **VS Code** e executar o terminal;
6. Instalar bibliotecas necessárias através do terminal do **VS Code**. Ex: `conda install numpy==1.17.2`.

### Pontos de Observação:
- Pode ser necessário ajustar o diretório de algumas bibliotecas após a instalação.

## Execução do Gripy
Após a configuração do ambiente, o Gripy pode ser executado através do botão "Run" a partir do arquivo `main.py` do projeto, no VS Code.

### Importar Dados de Poços
Para importar dados de poços no formato .LAS:
- Acesse a aba **Well > Import Well > LAS File** e navegue até onde se encontram os arquivos .LAS.
- Ao importar os dados de poços, eles serão exibidos na barra "Object Manager" à esquerda do Gripy.

## Apresentação do Plugin "Desafio"

### Criação do Plugin
1. Utilizou-se como base o exemplo de plugin existente no projeto:
   - O exemplo "Example" é um simples "Hello world" que exibe "oi" no terminal quando executado.
2. Foi criado o diretório "Desafio" com os mesmos arquivos iniciais contidos no diretório "Example".
3. O arquivo `.yapsy-plugin` é o identificador de plugin reconhecido pelo Gripy.

### Estrutura do Plugin
No Plugin Desafio, foram criados 2 diretórios além do arquivo principal `Desafio.py`:
- `ui` (para classes relacionadas a interface de usuário);
- `db` (para classes relacionadas a banco de dados).

### Execução do Plugin
Para executar o Plugin Desafio:
1. Acesse a aba **Plugins > Desafio**.

### Funcionalidades do Plugin
- **Combo 1:** Exibe os nomes dos poços carregados no Object Manager do Gripy.
- **Combo 2:** Após selecionar o poço, exibe as curvas que esse poço possui.
- **Botão "Exibir curva selecionada":** Abre o gráfico da curva selecionada.

### Funções Extras:
- **Botão Zoom:** Para dar zoom em uma área selecionada no gráfico.
- **Reset:** Retorna a exibição da curva ao modo default.
- **Add filter:** Abre uma nova janela com opções de filtros e operações a serem aplicados no gráfico original.
- **Toggle Plot:** Habilita/desabilita uma curva plotada.
- **Legend:** Habilita/desabilita a legenda.
- **Save pick:** Salva a imagem exibida.

---
