## 1. Conexão com Banco de Dados PostgreSQL (`connections.py`)

### Função: `postgres_conn()`

- **Descrição:** Estabelece conexão com o banco PostgreSQL usando variáveis de ambiente para credenciais.
- **Variáveis usadas:** `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`.
- **Retorno:** Retorna um objeto `engine` do SQLAlchemy para executar queries.
- **Validação:** Executa `SELECT 1` para garantir que a conexão está ativa.
- **Tratamento de erro:** Retorna `None` e imprime o erro caso a conexão falhe.

---

## 2. Leitura e Transformação dos Arquivos `.ods` (`ida_reader.py`)

### Função: `read_ods(file_path, sheet=0, skiprows=8)`

- **Descrição:** Lê arquivo `.ods` pulando linhas iniciais (metadados).
- **Filtragem:** Seleciona apenas linhas onde a coluna `VARIÁVEL` contém "IDA".
- **Transformação:** Converte colunas mensais em formato longo (wide → long).
- **Classificação:** Identifica tipo de serviço (Telefonia Celular, Fixa, Banda Larga ou Desconhecido) com base no nome do arquivo.
- **Retorno:** DataFrame transformado; se erro, retorna DataFrame vazio e imprime o erro.

### Função: `read_all_ods(folder)`

- **Descrição:** Lê todos os arquivos `.ods` da pasta especificada, aplica `read_ods` em cada um e concatena resultados.
- **Normalização:** Padroniza nomes das colunas para minúsculas, sem acentos e com underscores.
- **Retorno:** DataFrame único com dados combinados; vazio se não houver arquivos válidos.

---

## 3. Script Principal (`main.py`)

- Importa as funções `postgres_conn` e `read_all_ods`.
- Realiza a conexão com o banco.
- Lê e transforma os arquivos `.ods` da pasta `./files`.
- Insere os dados lidos na tabela `raw.ida` usando `to_sql` do pandas.
- Trata exceções e imprime mensagens de sucesso ou erro.

---

## 4. Criação da Tabela `raw.ida`

- Cria a tabela que armazena os dados importados dos arquivos `.ods`.
- Campos principais: grupo econômico, variável, mês, valor do IDA e tipo de serviço.

---

## 5. Criação da View `vw_taxa_variacao_ida`

- Cria uma view que calcula a taxa de variação mensal do indicador IDA para cada grupo econômico.
- Compara o IDA do mês atual com o mês anterior para obter a variação percentual.
- Calcula a média da variação para todos os grupos.
- Retorna a diferença entre a variação de cada grupo e a média, facilitando análise comparativa por mês.
