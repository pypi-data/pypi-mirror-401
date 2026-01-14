# MaxScienceLib

Biblioteca com funções utilitárias para a rotina de **Ciência de Dados** na **Maxpar**, focada em **produtividade**, **padronização** e **alta performance**.


## 📚 Sumário

* [Instalação e uso](#-instalação-e-uso)
* [Módulos disponíveis](#-módulos-disponíveis)

  * [`leitura_snowflake`](#leitura_snowflake)
  * [`leitura_tableau`](#leitura_tableau)
  * [`leitura_fipe`](#leitura_fipe)
  * [`upload_sharepoint`](#upload_sharepoint)
  * [`agrupar_produto`](#agrupar_produto)
  * [`media_saneada`](#media_saneada)

    * [`media_saneada`](#media_saneada-core)
    * [`media_saneada_expr`](#media_saneada_expr)
* [Licença](#licença)
* [Autores](#autores)

## Instalação e uso

Instale a biblioteca via `pip`:

```bash
pip install maxscientelib
```

Importe os módulos no seu código:

```python
from maxsciencelib import leitura_snowflake
```

---

## Módulos disponíveis

## leitura-snowflake

Biblioteca Python para leitura de dados do **Snowflake** de forma simples, segura e performática, retornando os resultados diretamente como **DataFrame Polars**.

A biblioteca abstrai toda a complexidade de conexão, autenticação via `externalbrowser` e execução de queries, permitindo que o usuário execute consultas com apenas **uma função**.



### Funcionalidades

- Conexão automática com Snowflake via `externalbrowser`
- Execução de queries SQL
- Retorno direto em **Polars DataFrame**
- Uso nativo de **Apache Arrow** (alta performance)
- Silenciamento de logs e warnings internos
- Fechamento seguro de conexão e cursor


### Requisitos

- Python **3.11+** (recomendado)
- Acesso ao Snowflake configurado no navegador


### Uso básico

```python
from leitura_snowflake import leitura_snowflake

query = """
SELECT *
FROM MINHA_TABELA
LIMIT 1000
"""

df = leitura_snowflake(
    email_corporativo="nome.sobrenome@empresa.com",
    token_account="abc123.us-east-1",
    query=query
)

df.head()
```

O retorno será um objeto:

```python
polars.DataFrame
```

| Parâmetro           | Tipo  | Descrição                                         |
| ------------------- | ----- | ------------------------------------------------- |
| `email_corporativo` | `str` | Email corporativo utilizado no login do Snowflake |
| `token_account`     | `str` | Identificador da conta Snowflake                  |
| `query`             | `str` | Query SQL a ser executada                         |

--- 

## leitura-tableau

Biblioteca Python para leitura de dados do **Tableau Server** de forma simples, segura e performática, retornando os resultados diretamente como **DataFrame Polars**.

A biblioteca abstrai toda a complexidade de autenticação via **Personal Access Token**, conexão com o Tableau Server (HTTP/HTTPS) e download da view, permitindo que o usuário consuma dados com apenas **uma função**.


### Funcionalidades

* Autenticação via **Personal Access Token (PAT)**
* Conexão automática com Tableau Server (fallback HTTP → HTTPS)
* Download de views diretamente do Tableau
* Retorno direto em **Polars DataFrame**
* Leitura eficiente de CSV em memória
* Silenciamento de warnings internos
* Encerramento seguro da sessão (`sign_out`)

### Requisitos

* Python **3.10+** (recomendado)
* Acesso ao Tableau Server
* Personal Access Token ativo no Tableau


### Uso básico

```python
from maxsciencelib.leitura_tableau import leitura_tableau

df = leitura_tableau(
    nome_token="meu_token_tableau",
    token_acesso="XXXXXXXXXXXXXXXXXXXXXXXX",
    view_id="abcd1234-efgh-5678"
)

df.head()
```

### Retorno

O retorno da função será um objeto:

```python
polars.DataFrame
```

### Parâmetros

| Parâmetro      | Tipo  | Descrição                                           |
| -------------- | ----- | --------------------------------------------------- |
| `nome_token`   | `str` | Nome do Personal Access Token cadastrado no Tableau |
| `token_acesso` | `str` | Token de acesso pessoal do Tableau                  |
| `view_id`      | `str` | Identificador da view no Tableau Server             |

---

## leitura_fipe

Biblioteca Python para **categorização de veículos com base na Tabela FIPE**, utilizando **quantis dinâmicos por tipo de veículo** e separação entre **veículos antigos e recentes**, retornando os resultados em **Polars DataFrame**.

A biblioteca abstrai toda a lógica estatística de cálculo de quantis, tratamento de dados e categorização, permitindo que o usuário obtenha a classificação do veículo com **apenas uma função**.

### Funcionalidades

* Leitura da Tabela FIPE diretamente de arquivo Excel
* Padronização automática de colunas
* Tratamento do ano (`ZERO KM` → ano vigente)
* Criação da chave `FIPE-ANO`
* Separação automática entre:

  * Veículos **antigos** (`ano < 2015`)
  * Veículos **recentes** (`ano ≥ 2015`)
* Categorização baseada em quantis por tipo de veículo:

  * **Antigo Popular**
  * **Antigo Premium**
  * **Popular**
  * **Intermediário**
  * **Premium**
* Processamento totalmente vetorizado em **Polars**
* Alta performance para grandes volumes de dados
* Interface simples e pronta para uso analítico

### Requisitos

* Python **3.10+** (recomendado)
* Acesso ao arquivo da Tabela FIPE
* Estrutura de colunas compatível com a base FIPE padrão

### Dependências

```bash
pip install polars pyarrow fastexcel
```

> O pacote `fastexcel` é utilizado pelo Polars para leitura eficiente de arquivos Excel.

### Uso básico

```python
from maxsciencelib.fipes_categoria import leitura_fipe

df_fipe_categoria = leitura_fipe()

df_fipe_categoria.head()
```

### Retorno

A função retorna um objeto do tipo:

```python
polars.DataFrame
```

com as seguintes colunas:

| Coluna      | Descrição                                    |
| ----------- | -------------------------------------------- |
| `fipe_ano`  | Código FIPE concatenado com o ano do veículo |
| `ano`       | Ano do veículo                               |
| `marca`     | Marca do veículo                             |
| `modelo`    | Modelo do veículo                            |
| `categoria` | Categoria FIPE calculada                     |


### Lógica de categorização

A categorização é feita **por tipo de veículo**, seguindo as regras abaixo:

#### Veículos antigos (`ano < 2015`)

| Condição      | Categoria      |
| ------------- | -------------- |
| `valor ≤ P60` | Antigo Popular |
| `valor > P60` | Antigo Premium |

#### Veículos recentes (`ano ≥ 2015`)

| Condição            | Categoria     |
| ------------------- | ------------- |
| `valor ≤ P50`       | Popular       |
| `P50 < valor ≤ P70` | Intermediário |
| `valor > P70`       | Premium       |

> Os percentis são calculados **dinamicamente por `tipo_veiculo`**.

---

## upload-sharepoint

Biblioteca Python para **upload automático de arquivos no SharePoint** utilizando automação via navegador (**Selenium + Microsoft Edge**).

A função abstrai toda a complexidade de interação com a interface web do SharePoint, permitindo realizar o upload de **todos os arquivos de um diretório local** com apenas **uma chamada de função**.

> Esta funcionalidade utiliza automação de UI e depende do layout do SharePoint. Recomendada para uso interno e controlado.


### Funcionalidades

- Upload automático de múltiplos arquivos para SharePoint
- Suporte a upload em massa a partir de um diretório local
- Automação via Microsoft Edge (Selenium)
- Detecção automática de sobrescrita (`Substituir tudo`)
- Controle de timeout e tempo de espera
- Fechamento seguro do navegador


### Requisitos

- Python **3.11+** (recomendado)
- Microsoft Edge instalado
- Edge WebDriver compatível
- Acesso ao SharePoint via navegador (login manual)


### Dependências

```bash
pip install selenium
```
 
Caso esteja usando a biblioteca `maxsciencelib` recomenda-se instalar com:

```bash
pip install maxsciencelib[selenium]
```


### Uso básico

```python
from maxsciencelib import upload_sharepoint

upload_sharepoint(
    url_sharepoint="https://autoglass365.sharepoint.com/sites/XXXXXXXXX/Shared%20Documents/Forms/AllItems.aspx",
    diretorio=r"C:\Users\usuario\Desktop\arquivos_para_upload"
)
```


### Comportamento da função

* Todos os arquivos presentes no diretório informado serão enviados
* Caso o arquivo já exista no SharePoint, a função tentará clicar em **“Substituir tudo”**
* O navegador será fechado automaticamente ao final do processo
* Em caso de erro, a função lança exceções claras (`FileNotFoundError`, `RuntimeError`)


### Parâmetros

| Parâmetro          | Tipo  | Descrição                                                               |
| ------------------ | ----- | ----------------------------------------------------------------------- |
| `url_sharepoint`   | `str` | URL do diretório do SharePoint onde os arquivos serão carregados        |
| `diretorio`        | `str` | Caminho local contendo **apenas** os arquivos a serem enviados          |
| `tempo_espera_fim` | `int` | Tempo (em segundos) de espera após o upload antes de fechar o navegador |
| `timeout`          | `int` | Timeout máximo (em segundos) para espera de elementos na interface      |


### Retorno

```python
None
```

A função não retorna valores.
Caso ocorra algum erro durante o processo, uma exceção será lançada.


---

## agrupar-produto

Biblioteca Python para **padronização e agrupamento de descrições de produtos automotivos**, abstraindo regras complexas de **marca**, **lado (LE/LD)** e **casos específicos por tipo de peça**, retornando o resultado diretamente no **DataFrame original** com uma nova coluna agrupada.

A biblioteca foi desenhada para que o usuário precise chamar **apenas uma função**, informando o **DataFrame**, a **coluna de origem** e o **nome da nova coluna**, mantendo a coluna original intacta.


### Funcionalidades

* Agrupamento automático por **tipo de produto**

  * Vidro
  * Retrovisor
  * Farol / Lanterna
* Remoção padronizada de **marca**
* Remoção padronizada de **lado (LE / LD / E / D)**
* Tratamento de **casos específicos**
* Limpeza de sufixos como:

  * `EXC`
  * `AMT`
  * `AMT CNT`
  * `AMT AER`
* Preserva a coluna original
* Compatível com valores nulos (`NaN`)
* Interface simples, orientada a **DataFrame**
* Pronta para uso em pipelines analíticos e feature engineering


### Requisitos

* Python **3.9+**
* Pandas

### Dependências

```bash
pip install pandas
```

### Uso básico

```python
from maxsciencelib.agrupamento import agrupar_produto

df = agrupar_produto(
    df,
    coluna_origem="produto_descricao",
    coluna_nova="produto_agrupado"
)

df.head()
```

### Uso com controle de regras

```python
df = agrupar_produto(
    df,
    coluna_origem="produto_descricao",
    coluna_nova="produto_agrupado",
    agrupar_marca=False,
    agrupar_lado=True
)
```

### Retorno

A função retorna o próprio DataFrame com a nova coluna adicionada:

```python
pandas.DataFrame
```

### Parâmetros

| Parâmetro       | Tipo      | Descrição                                                      |
| --------------- | --------- | -------------------------------------------------------------- |
| `df`            | DataFrame | DataFrame de entrada                                           |
| `coluna_origem` | `str`     | Nome da coluna que contém a descrição original do produto      |
| `coluna_nova`   | `str`     | Nome da nova coluna com o produto agrupado                     |
| `agrupar_marca` | `bool`    | Remove marcas do produto (`True` por padrão)                   |
| `agrupar_lado`  | `bool`    | Remove indicação de lado (LE / LD / E / D) (`True` por padrão) |


### Regras de agrupamento (interno)

A função identifica automaticamente o tipo de produto com base na descrição:

| Tipo identificado | Regra aplicada                    |
| ----------------- | --------------------------------- |
| `VID`             | Agrupamento de vidros             |
| `RETROV`          | Agrupamento de retrovisores       |
| `FAROL` / `LANT`  | Agrupamento de faróis e lanternas |
| Outros            | Mantém a descrição original       |

---

## media-saneada

Funções para cálculo de **média saneada**, removendo outliers de forma iterativa com base no **coeficiente de variação (CV)**, garantindo maior robustez estatística e **alto desempenho computacional**.

A implementação foi projetada para **grandes volumes de dados**, utilizando:

* **NumPy puro no caminho crítico**
* **Paralelização real por grupo (multiprocessing)**

São disponibilizadas **duas funções públicas**:

* uma função **core**, para cálculo direto sobre vetores numéricos
* uma função **groupby**, para agregações eficientes em **DataFrames Pandas**, com paralelização automática

---

## Funcionalidades

* Cálculo de média robusta com saneamento iterativo
* Remoção automática de outliers com base em:

  * média
  * desvio padrão
  * coeficiente de variação (CV)
* Fallback seguro para **mediana**
* Controle de:

  * número mínimo de amostras
  * CV máximo permitido
* Alta performance:

  * NumPy puro no loop crítico
  * Paralelização por múltiplos processos
* Compatível com:

  * `list`
  * `numpy.ndarray`
  * `pandas.Series`
* Integração nativa com **Pandas `groupby`**

---

## Requisitos

* Python **3.9+** (recomendado 3.10+)
* NumPy
* Pandas
* joblib

---

## Dependências

```bash
pip install numpy pandas joblib
```

---

## `media_saneada`

Calcula a média saneada de um conjunto de valores numéricos, removendo iterativamente valores fora do intervalo
**[média ± desvio padrão]** até que o coeficiente de variação esteja dentro do limite aceitável.

### Assinatura

```python
media_saneada(
    valores,
    min_amostras: int = 3,
    cv_max: float = 0.25
) -> float
```

### Parâmetros

| Parâmetro      | Tipo                                | Descrição                                |
| -------------- | ----------------------------------- | ---------------------------------------- |
| `valores`      | `list` | `np.ndarray` | `pd.Series` | Conjunto de valores numéricos            |
| `min_amostras` | `int`                               | Número mínimo de amostras permitidas     |
| `cv_max`       | `float`                             | Coeficiente de variação máximo aceitável |

### Retorno

```python
float
```

* Retorna a **média saneada** se o CV estiver dentro do limite
* Caso contrário, retorna a **mediana** dos últimos `min_amostras` valores
* Nunca lança erro para vetores pequenos (fallback seguro)

### Uso básico

```python
from maxsciencelib import media_saneada

media = media_saneada([100, 102, 98, 500, 101])
```

---

## `media_saneada_groupby`

Aplica a média saneada por grupo em um **DataFrame Pandas**, utilizando **paralelização por múltiplos processos** para reduzir drasticamente o tempo de execução.

### Assinatura

```python
media_saneada_groupby(
    df: pd.DataFrame,
    group_cols: list[str],
    value_col: str,
    min_amostras: int = 3,
    cv_max: float = 0.25,
    n_jobs: int = -1,
    output_col: str = "media_saneada"
) -> pd.DataFrame
```

### Parâmetros

| Parâmetro      | Tipo           | Descrição                                             |
| -------------- | -------------- | ----------------------------------------------------- |
| `df`           | `pd.DataFrame` | DataFrame de entrada                                  |
| `group_cols`   | `list[str]`    | Colunas de agrupamento                                |
| `value_col`    | `str`          | Coluna numérica a ser agregada                        |
| `min_amostras` | `int`          | Número mínimo de amostras por grupo                   |
| `cv_max`       | `float`        | Coeficiente de variação máximo aceitável              |
| `n_jobs`       | `int`          | Número de processos paralelos (`-1` = todos os cores) |
| `output_col`   | `str`          | Nome da coluna de saída                               |

### Retorno

```python
pd.DataFrame
```

DataFrame agregado contendo uma linha por grupo e a média saneada calculada.

---

### Exemplo de uso

```python
import pandas as pd
from maxsciencelib import media_saneada_groupby

df = pd.DataFrame({
    "grupo": ["A", "A", "A", "A", "B", "B", "B"],
    "valor": [100, 102, 98, 500, 50, 52, 51]
})

resultado = media_saneada_groupby(
    df,
    group_cols=["grupo"],
    value_col="valor"
)
```

---

## Licença

The MIT License (MIT)

## Autores

Daniel Antunes Cordeiros