# Scripts de Anotação e Avaliação YOLO

Este repositório contém scripts utilitários para preparação de dados, avaliação e visualização de modelos de detecção de objetos com **YOLO**.

### Autor

- Pedro Renã da Silva Moreira: [@Pedrordsm](https://github.com/Pedrordsm)

# Instalação e Execução

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

* **Python 3.x** (Recomendado 3.8+)
* Os dados de anotações e pesos do modelo YOLO treinado

## Clone o repositório

```bash
git clone https://github.com/Pedrordsm/seu-repositorio.git
```

Abra o terminal, escreva `cd` e cole o caminho onde o repositório está salvo:

```bash
# No Windows
cd C:\Users\NomedoUsuario\Documents\seu-repositorio

# No Linux/WSL
cd /home/usuario/seu-repositorio
```

## Criar e utilizar um ambiente virtual

### Criação do ambiente virtual

```bash
# No Windows
py -m venv .venv

# No Linux/WSL
python3 -m venv .venv
```

### Ativação do ambiente virtual

```bash
# No Windows (PowerShell)
.\.venv\Scripts\activate

# No Linux/WSL
source .venv/bin/activate
```

## Instale os requirements

```bash
pip install -r requirements.txt
```

# Scripts

## `anotacao.py`

Lê o CSV de anotações do Vindr-CXR e gera um arquivo `.txt` por radiologista com suas respectivas anotações.

```bash
python anotacao.py --csv nomearquivo.csv
```

| Argumento | Padrão | Descrição |
|-----------|--------|-----------|
| `--csv` | `csvs/annotations_train.csv` | Caminho para o CSV de anotações |

---

## `split.py`

Divide um dataset de imagens e labels em conjuntos de treino e validação.

```bash
python split.py --images caminho/imagens --labels caminho/labels --pct 0.2 --seed 42
```

| Argumento | Padrão | Descrição |
|-----------|--------|-----------|
| `--images` | *(obrigatório)* | Pasta com as imagens |
| `--labels` | *(obrigatório)* | Pasta com os labels |
| `--pct` | `0.2` | Porcentagem para validação |
| `--seed` | `42` | Seed para reprodutibilidade |

---

## `metricas.py`

Avalia um modelo YOLO e salva as métricas (Precision, Recall, mAP) em um arquivo TXT.

```bash
python metricas.py --modelo runs/detect/train3/weights/best.pt --saida metricas.txt
```

| Argumento | Padrão | Descrição |
|-----------|--------|-----------|
| `--modelo` | `runs/detect/train3/weights/best.pt` | Caminho para os pesos do modelo |
| `--saida` | `metricas.txt` | Arquivo de saída das métricas |

---

## `graficar_metricas.py`

Lê o arquivo de métricas gerado pelo `metricas.py` e gera gráficos de barras por classe.

```bash
python graficar_metricas.py --metricas metricas.txt
```

| Argumento | Padrão | Descrição |
|-----------|--------|-----------|
| `--metricas` | `metricask14.txt` | Caminho para o arquivo de métricas |

---

## `graficar_anotadores.py`

Lê os arquivos TXT gerados pelo `anotacao.py` e gera gráficos de distribuição de classes por anotador.

```bash
python graficar_anotadores.py --pasta anotadores
```

| Argumento | Padrão | Descrição |
|-----------|--------|-----------|
| `--pasta` | `anotadores` | Pasta com os arquivos TXT dos anotadores |
