# Sistema de Loja Online - TP1

## Sobre o Projeto

Sistema completo de loja online desenvolvido para o trabalho prático de Gerenciamento de Configuração e Evolução de Software. Inclui funcionalidades de gerenciamento de produtos, carrinho de compras, processamento de pedidos, pagamentos e entregas.

## Estrutura do Projeto

```
.
├── src/loja_online/          # Código fonte da aplicação
│   ├── carrinho.py           # Gerenciamento do carrinho
│   ├── cliente.py            # Cadastro e autenticação de clientes
│   ├── entrega.py            # Sistema de entregas
│   ├── estoque.py            # Controle de estoque
│   ├── loja.py               # Orquestração da loja
│   ├── main.py               # Ponto de entrada da aplicação
│   ├── pagamento.py          # Processamento de pagamentos
│   ├── pedido.py             # Gerenciamento de pedidos
│   ├── produto.py            # Cadastro de produtos
│   └── utilitarios.py        # Funções auxiliares
│
├── tests/                    # Suite completa de testes
│   ├── unit/                 # Testes unitários
│   ├── integration/          # Testes de integração
│   └── acceptance/           # Testes de aceitação e performance
│
├── scripts/                  # Scripts de build e automação
│   └── build.sh              # Script de build detalhado
│
├── .github/workflows/        # Pipelines CI/CD
│   ├── build.yml             # Pipeline de build
│   ├── tests.yml             # Testes automatizados
│   ├── acceptance-tests.yml  # Testes de aceitação
│   └── deploy.yml            # Deploy automático
│
├── test-results/             # Resultados de testes (gerados automaticamente)
├── app.py                    # Servidor Flask para health check
├── setup.py                  # Configuração do pacote Python
├── requirements.txt          # Dependências do projeto
├── pytest.ini                # Configuração do pytest
├── Makefile                  # Comandos principais do projeto
└── README.md                 # Este arquivo
```

## Início Rápido

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Instalação

```bash
# Clone o repositório
git clone https://github.com/anajuliateixeiracandido/TP1-Gerenciamento-de-Configuracao-e-Evolucao-de-Software.git
cd TP1-Gerenciamento-de-Configuracao-e-Evolucao-de-Software

# Instale as dependências
make install

# Configure o ambiente de desenvolvimento
make dev
```

### Executando a Aplicação

```bash
# Executar aplicação principal
make run

# Executar servidor Flask (health check)
make server
```

## Testes

### Para que Servem os Testes

#### Testes de Aceitação Funcional

Validam se o sistema funciona corretamente do ponto de vista do usuário final, testando o fluxo completo de uso:

**Teste Implementado:** `test_fluxo_completo_compra_sucesso`

- Valida todo o ciclo de vida de uma compra na loja online
- Testa 9 passos completos desde cadastro até finalização
- Garante que todas as funcionalidades integradas funcionam juntas

#### Testes de Performance

Validam requisitos não-funcionais do sistema, como velocidade e capacidade de carga:

1. **Cadastro em Massa** (`test_cadastro_massa_produtos`)
   - Cadastra 1.000 produtos em menos de 2 segundos
   - Gera arquivo: `test-results/performance-cadastro-em-massa-de-produtos.json`

2. **Pedidos Simultâneos** (`test_criacao_pedidos_simultaneos`)
   - Cria 100 pedidos concorrentes sem erros
   - Gera arquivo: `test-results/performance-criação-de-pedidos-simultâneos.json`

3. **Busca de Produtos** (`test_busca_rapida_produtos`)
   - Executa 1.000 buscas em menos de 1 segundo
   - Gera arquivo: `test-results/performance-busca-de-produtos.json`

4. **Atualização Concorrente** (`test_atualizacao_concorrente_estoque`)
   - Valida consistência com 100 operações paralelas no estoque
   - Gera arquivo: `test-results/performance-atualização-concorrente-de-estoque.json`

**Observação:** Os arquivos JSON são gerados automaticamente na pasta `test-results/` após a execução dos testes.

---

### Testes Unitários

Validam componentes individuais do sistema:

```bash
make test-unit
```

### Testes de Integração

Validam a integração entre componentes:

```bash
make test-integration
```

### Testes de Aceitação

Validam o fluxo completo do ponto de vista do usuário:

```bash
make test-acceptance
```

### Testes de Performance

Validam requisitos não-funcionais (velocidade, capacidade):

```bash
make test-performance
```

### Executar Todos os Testes

```bash
make test
```

## 🔨 Build

### Build Local

```bash
# Build completo (inclui validação e geração de artefatos)
make build

# Apenas validar sintaxe Python
make validate

# Limpar artefatos de build
make clean
```

### Build via Scripts

```bash
# Executar script de build detalhado
chmod +x scripts/build.sh
./scripts/build.sh
```

## Comandos Disponíveis

Execute `make` ou `make help` para ver todos os comandos disponíveis:

```
CONFIGURAÇÃO:
  make install              Instalar dependências
  make dev                  Configurar ambiente de desenvolvimento
  make clean                Limpar artefatos de build

BUILD:
  make build                Executar build completo
  make validate             Validar sintaxe Python

EXECUÇÃO:
  make run                  Executar aplicação principal
  make server               Executar servidor Flask (health check)

TESTES:
  make test                 Executar todos os testes
  make test-unit            Executar testes unitários
  make test-integration     Executar testes de integração
  make test-acceptance      Executar testes de aceitação
  make test-performance     Executar testes de performance
```

## CI/CD Pipeline

O projeto possui 4 pipelines automatizados no GitHub Actions:

### 1. Build Pipeline (`.github/workflows/build.yml`)
**Triggers:** Push ou PR para `main`/`master`  
**Matrix:** Python 3.8, 3.9, 3.10, 3.11

- Validação de sintaxe Python
- Verificação de execução da aplicação
- Build do pacote Python (wheel + source distribution)
- Upload de artefatos (disponível por 30 dias)
- Cache de dependências pip

### 2. Testes Automatizados (`.github/workflows/tests.yml`)
**Triggers:** Push ou PR para `main`/`master`  
**Matrix:** Python 3.9, 3.10, 3.11

- Testes unitários
- Testes de integração
- Cobertura de código (mínimo 70%)
- Relatórios HTML e XML de cobertura
- Upload de artefatos de teste

### 3. Testes de Aceitação (`.github/workflows/acceptance-tests.yml`)
**Triggers:** Push ou PR para `main`/`master` e após workflow "Testes Automatizados" passar com sucesso

**Funcionalidades:**
1. Configura ambiente Python 3.11
2. Instala dependências
3. Inicia aplicação em background
4. Executa testes de aceitação funcionais
5. Executa testes de performance:
   - Cadastro em massa (1.000 produtos < 2s)
   - Pedidos simultâneos (100 pedidos concorrentes)
   - Busca de produtos (1.000 buscas < 1s)
   - Atualização concorrente (100 operações paralelas)
6. Captura logs e evidências em caso de falha
7. Gera relatório completo de evidências
8. Upload de artefatos (disponível por 30 dias)

### 4. Deploy Pipeline (`.github/workflows/deploy.yml`)
**Trigger:** Após Build Pipeline passar com sucesso em `main`/`master`

- Deploy automático para Render
- Health check da aplicação
- Validação de disponibilidade (30 tentativas)

## Endpoints da Aplicação

### Health Check
```bash
GET /health
```
Retorna status do servidor: `{"status": "ok"}`

## Estrutura de Dados

### Produto
- ID, nome, descrição, preço, categoria, estoque

### Cliente
- ID, nome, email, CPF, endereço, telefone

### Pedido
- ID, cliente, itens, total, status, data

### Pagamento
- ID, pedido, método, status, valor

### Entrega
- ID, pedido, endereço, status, prazo

## Tecnologias Utilizadas

- **Python 3.11**: Linguagem principal
- **Pytest**: Framework de testes
- **Flask**: Servidor web para health check
- **GitHub Actions**: CI/CD
- **Render**: Plataforma de deploy
- **Make**: Automação de tarefas


## Fluxo de Contribuição e Políticas de Branching e Versionamento
Esta seção detalha as regras de governança e o fluxo de trabalho obrigatório.

> **CCB (Change Control Board)**: Processo de controle de mudanças que garante qualidade através de:
> - **CCB Automatizado**: Pipelines de CI/CD (Build, Testes, Aceitação) que validam automaticamente as mudanças
> - **CCB Humano**: Revisão por pares através de aprovação de Pull Requests

## 1. Política de Branching e Versionamento

Adotamos o **Git Flow Simplificado** para manter a estabilidade da ramificação `main`, que representa o código em produção.

| Branch | Status                         | Regras de Trabalho                                                                                 | Versionamento                                         |
|-------------|--------------------------------|----------------------------------------------------------------------------------------------------------------------|------------------------------------------------------|
| `main`      | Linha de Base de Produção      | **Recomendado:** Proteger branch com aprovação de PR obrigatória + status checks (Build, Testes, Aceitação).<br>Commits diretos devem ser evitados.                   | SemVer (`MAJOR.MINOR.PATCH`). Tagging manual após o merge. |
| `feature/*` | Desenvolvimento                | Ramificada a partir de `main` para novas funcionalidades (`feat`).                                                  | Não versionada.                                      |
| `fix/*`     | Manutenção                     | Ramificada a partir de `main` para correções de bugs (`fix`).                                                       | Não versionada.                                      |
| `docs/*`    | Documentação / Governança      | Ramificada a partir de `main` para atualizações de documentação e regras de CM (`docs`).                            | Não versionada.                                      |


## Como Funciona o Versionamento Semântico 

O projeto usa o formato **X.Y.Z** (`MAJOR.MINOR.PATCH`) para comunicar o tipo de mudança em cada *release*.

- **X (MAJOR)**: Incrementado para mudanças **incompatíveis** com versões anteriores (quebram o contrato).
- **Y (MINOR)**: Incrementado para **novas funcionalidades** (`feat`) compatíveis.
- **Z (PATCH)**: Incrementado para **correções de bugs** (`fix`) compatíveis.

### Exemplo de Incremento de Versão

Se a versão atual é **`1.2.5`**:

- **PATCH (Z)**  
  Se você corrige um cálculo errado no carrinho (`fix`), a versão se torna:  
  ➜ **`1.2.6`**

- **MINOR (Y)**  
  Se você adiciona um novo método para calcular descontos (`feat`), a versão se torna:  
  ➜ **`1.3.0`**

- **MAJOR (X)**  
  Se você muda a estrutura de dados principal de **Cliente** de forma que a versão `1.2.5` não consiga mais interagir com a nova, a versão se torna:  
  ➜ **`2.0.0`**

---

## Como Atualizar a Versão do Projeto

O versionamento no projeto acontece em **DUAS etapas distintas**:

### 1️⃣ Atualização da Versão no Código (`setup.py`)

**Quando:** Durante o desenvolvimento, ANTES de fazer o commit da mudança  
**Onde:** Arquivo `setup.py` na raiz do projeto

```python
# setup.py
setup(
    name="loja-online",
    version="1.2.6",  # ← Atualize este número manualmente
    # ...
)
```

**Como fazer:**
```bash
# 1. Edite o arquivo setup.py
vim setup.py

# 2. Altere a linha version="1.2.5" para version="1.2.6"

# 3. Commit a mudança junto com seu código
git add setup.py
git commit -m "fix: corrige cálculo do carrinho"
```

### 2️⃣ Criação de Tag Git (Release)

**Quando:** APÓS o merge do PR na `main`  
**Onde:** Repositório Git (cria um marco/snapshot)  
**Propósito:** Formalizar a versão e permitir criar Releases no GitHub

**Como fazer:**
```bash
# 1. Atualize sua branch main local
git checkout main
git pull origin main

# 2. Crie a tag com a versão apropriada (deve ser a MESMA do setup.py)
git tag -a v1.2.6 -m "fix: corrige cálculo do carrinho"
# ou
git tag -a v1.3.0 -m "feat: adiciona sistema de descontos"
# ou
git tag -a v2.0.0 -m "BREAKING CHANGE: nova estrutura de Cliente"

# 3. Envie a tag para o repositório remoto
git push origin v1.2.6

# 4. (Opcional) Crie uma Release no GitHub
# Acesse: GitHub → Releases → Draft a new release → Escolha a tag → Publique
```

**Importante:** A criação da tag **não dispara** o deploy automaticamente. O deploy é acionado pelo merge do PR após o Build Pipeline passar.

---

## 2. Guia de Contribuição Rápido

O processo de trabalho deve seguir este fluxo:

### Passo 1: Crie sua Branch

Utilize o prefixo `feature/`, `fix/` ou `docs/` a partir de `main`.

### Passo 2: Desenvolvimento e Testes

Implemente a mudança e crie/ajuste os testes necessários (Unitário / Integração) para manter a **cobertura de código ≥ 70%**.

### Passo 3: Commit com Conventional Commits

Registre suas alterações seguindo o padrão de mensagem de commits.

### Passo 4: Push e Abertura do Pull Request

Abra o PR da sua *branch* para `main` e aplique a label **`needs review`**.

### Passo 5: Aprovação Automatizada (CCB Automatizado)

Os seguintes **status checks** executarão automaticamente:

- **Build Pipeline**: Valida sintaxe e gera artefatos
- **Testes Automatizados**: Executa testes unitários e integração
- **Testes de Aceitação**: Valida fluxo completo e performance

**Todos devem passar** para permitir o merge.

### Passo 6: Revisão Humana (CCB Humano)

- Um ou mais revisores analisarão o código
- Faça ajustes se necessário baseado no feedback
- Após aprovação, o PR estará pronto para merge

### Passo 7: Merge e Deploy

1. **Merge do PR**: Após aprovações e checks passarem
2. **Tagging** (se aplicável): Crie tag de versão conforme descrito acima
3. **Deploy Automático**: O pipeline de deploy executará automaticamente para `main`



## Convenção de Commits

Seguimos **[Conventional Commits](https://www.conventionalcommits.org/)**. A mensagem de commit deve seguir o formato:

`<tipo>(<escopo opcional>): <descrição_curta>`

---

### Tipos de Commit
| Tipo        | Descrição                                                                                                      | Exemplo de commit                                                            | Implica Versionamento |
|------------|----------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|---------------------------------|
| `feat`     | Implementa uma nova funcionalidade ou recurso para o usuário.                                                  | `feat(carrinho): implementa metodo para obter itens do carrinho`            | Incrementa MINOR (Y)            |
| `fix`      | Corrige um bug no código de produção.                                                                          | `fix(pedido): corrige erro de arredondamento no cálculo do total`           | Incrementa PATCH (Z)            |
| `test`     | Adiciona, corrige ou refatora testes (unitário, integração ou aceitação). Não altera código de produção.      | `test(checkout): adiciona testes de integração do fluxo de pagamento`       | Não                             |
| `build`    | Alterações que afetam o sistema de build, dependências externas (ex: `requirements.txt`) ou escopos.          | `build: atualiza versao do Python para 3.11 e dependencias`                 | Não                             |
| `ci`       | Alterações nos arquivos de configuração do CI/CD (ex: workflows `.yml` no GitHub Actions).                    | `ci(build): adiciona cache de dependencias ao workflow de build`            | Não                             |
| `docs`     | Alterações apenas na documentação (`README`, comentários de código, etc.).                                     | `docs: atualiza instrucoes de setup no readme`                              | Não                             |
| `refactor` | Reestruturação de código que não corrige bug e não adiciona feature.                                          | `refactor(auth): simplifica validacao de token jwt`                         | Não                             |
| `chore`    | Outras tarefas de manutenção que não se encaixam nas categorias acima (ex: `.gitignore`).                     | `chore: adiciona regras de ignore para arquivos temporarios`                | Não                             |



## Links Úteis

- [Repositório no GitHub](https://github.com/anajuliateixeiracandido/TP1-Gerenciamento-de-Configuracao-e-Evolucao-de-Software)
- [GitHub Actions](https://github.com/anajuliateixeiracandido/TP1-Gerenciamento-de-Configuracao-e-Evolucao-de-Software/actions)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning (SemVer)](https://semver.org)
