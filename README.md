# Lumiere-Python

**Lumiere-Python** é um sistema desenvolvido em Python, focado no gerenciamento de consumo de energia elétrica. Ele permite que usuários se cadastrem e registrem seus consumos de luz de forma manual ou automatizada, utilizando contas de luz em PDF. Após o registro de pelo menos três meses de consumo, o sistema oferece gráficos com análises baseadas na média inicial.

## Tecnologias Utilizadas

- **Python** - Linguagem de programação principal.
- **Oracle SQL** - Banco de dados para armazenar dados do usuário.
- **PyMuPDF** - Biblioteca para extração de informações de PDFs.

## Funcionalidades

- **Cadastro de Usuários** - Armazena informações do usuário de forma segura.
- **Registro de Consumos**:
  - Manual: Inserção direta de dados.
  - Automático: Extração de informações específicas do PDF da conta de luz:
    - `Consumo kWh`
    - `Data da Conta`
    - `CEP`
- **Análise de Consumo**:
  - Geração de gráficos de consumo por mês.
  - Inclusão de uma linha de base, calculada pela média dos três primeiros meses cadastrados.

## Estrutura do Projeto

- `cria_conexao.py` - Configura a conexão com o banco de dados.
- `extrai_texto_pdf.py` - Realiza a extração de dados das contas de luz em PDF.
- `lumiere.py` - Arquivo principal que integra o sistema.

## Instruções de Uso

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/ViniciuSaeSouza/Lumiere-Python.git
   ```
2. **Crie e ative um ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/Scripts/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```
3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure o banco de dados**:
   Edite o arquivo `cria_conexao.py` com suas credenciais Oracle.
5. **Execute o projeto**:
   ```bash
   python lumiere.py
   ```

## Autor

- Vinicius Souza - [GitHub](https://github.com/ViniciuSaeSouza)
