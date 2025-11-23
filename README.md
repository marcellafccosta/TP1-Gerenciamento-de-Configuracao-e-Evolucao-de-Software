# Testes de Aceitação

## O que foi Implementado

Este projeto implementa **Testes de Aceitação** completos para o sistema de loja online, incluindo testes funcionais end-to-end e testes não-funcionais de performance.

## Para que Servem os Testes

### Testes de Aceitação Funcional
Validam se o sistema funciona corretamente do ponto de vista do usuário final, testando o fluxo completo de uso:

**Teste Implementado:** `test_fluxo_completo_compra_sucesso`
- Valida todo o ciclo de vida de uma compra na loja online
- Testa 9 passos completos desde cadastro até finalização
- Garante que todas as funcionalidades integradas funcionam juntas

### Testes de Performance
Validam requisitos não-funcionais do sistema, como velocidade e capacidade de carga:

1. **Cadastro em Massa** - Testa se o sistema consegue cadastrar 1.000 produtos em menos de 2 segundos
2. **Pedidos Simultâneos** - Verifica se 100 pedidos podem ser criados ao mesmo tempo sem erros
3. **Busca de Produtos** - Testa se 1.000 buscas são realizadas em menos de 1 segundo
4. **Atualização Concorrente** - Valida consistência de dados com 100 operações paralelas no estoque

## Como Rodar os Testes

### Pré-requisitos
```bash
# Instalar dependências
pip install -r requirements.txt
```

### Executar Testes (Windows)

#### Todos os Testes de Aceitação
```powershell
$env:PYTHONIOENCODING='utf-8'; python -m pytest tests/acceptance/ -v
```

#### Apenas Teste Funcional
```powershell
$env:PYTHONIOENCODING='utf-8'; python -m pytest tests/acceptance/test_fluxo_completo_loja.py -v
```

#### Apenas Testes de Performance
```powershell
$env:PYTHONIOENCODING='utf-8'; python -m pytest tests/acceptance/test_performance.py -v
```

#### Com Output Detalhado
```powershell
$env:PYTHONIOENCODING='utf-8'; python -m pytest tests/acceptance/ -v -s
```

### Executar Testes (Linux/Mac)
```bash
python -m pytest tests/acceptance/ -v
```

## Pipeline CI/CD (GitHub Actions)

### Arquivo: `.github/workflows/acceptance-tests.yml`

**Quando executa:**
- Push para branch `main` ou `master`
- Pull Request para `main` ou `master`
- Após o workflow de "Testes Automatizados" passar com sucesso

**O que faz:**
1. Configura ambiente Python 3.11
2. Instala dependências automaticamente
3. Inicia a aplicação em background
4. Executa testes de aceitação funcionais
5. Executa testes de performance
6. Captura logs e evidências em caso de falha
7. Faz upload dos resultados como artefatos (disponível por 30 dias)
