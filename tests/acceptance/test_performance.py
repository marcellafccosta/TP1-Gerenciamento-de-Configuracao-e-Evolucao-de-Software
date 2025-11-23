"""
Testes de Performance - Loja Online

Este módulo contém testes não-funcionais que validam o desempenho
e a capacidade de carga da aplicação.
"""

from loja_online.loja import Loja
from loja_online.produto import Produto
from loja_online.pedido import Pedido
import pytest
import time
import sys
import os
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../src')))


class TestPerformanceLoja:
    """
    Testes de Performance e Carga da Loja Online

    Estes testes validam:
    - Tempo de resposta das operações críticas
    - Capacidade de processamento simultâneo
    - Desempenho sob carga
    """

    def setup_method(self):
        """Configuração inicial para cada teste"""
        self.loja = Loja()
        self.metricas = {
            "nome_teste": "",
            "timestamp": datetime.now().isoformat(),
            "metricas": {}
        }

    def test_performance_cadastro_produtos_em_massa(self):
        """
        Teste de Performance: Cadastro em Massa de Produtos

        Valida o tempo necessário para cadastrar múltiplos produtos.
        Requisito: Deve cadastrar 1000 produtos em menos de 2 segundos.
        """
        print("\n" + "="*80)
        print("TESTE DE PERFORMANCE: CADASTRO EM MASSA DE PRODUTOS")
        print("="*80)

        self.metricas["nome_teste"] = "Cadastro em Massa de Produtos"

        quantidade = 1000
        tempo_inicio = time.time()

        print(f"\n[TESTE] Cadastrando {quantidade} produtos...")

        for i in range(quantidade):
            produto = self.loja.cadastrar_produto(
                i + 1,
                f"Produto {i + 1}",
                100.0 + (i * 0.5)
            )
            produto.definir_estoque(10)

        tempo_fim = time.time()
        tempo_decorrido = tempo_fim - tempo_inicio

        produtos_por_segundo = quantidade / tempo_decorrido
        tempo_por_produto = (tempo_decorrido / quantidade) * \
            1000  # em milissegundos

        print(f"\n✓ Resultados:")
        print(f"  - Produtos cadastrados: {len(self.loja.produtos)}")
        print(f"  - Tempo total: {tempo_decorrido:.3f} segundos")
        print(f"  - Produtos/segundo: {produtos_por_segundo:.2f}")
        print(f"  - Tempo médio por produto: {tempo_por_produto:.3f} ms")

        self.metricas["metricas"] = {
            "quantidade": quantidade,
            "tempo_total_segundos": tempo_decorrido,
            "produtos_por_segundo": produtos_por_segundo,
            "tempo_medio_ms": tempo_por_produto
        }

        # Validação: deve cadastrar todos os produtos em menos de 2 segundos
        assert len(self.loja.produtos) == quantidade
        assert tempo_decorrido < 2.0, f"Tempo de cadastro muito alto: {tempo_decorrido:.3f}s"

        print(
            f"\n✓ APROVADO: Cadastro completado em {tempo_decorrido:.3f}s (limite: 2.0s)")
        print("="*80 + "\n")

        self._salvar_metricas()

    def test_performance_criacao_pedidos_simultaneos(self):
        """
        Teste de Carga: Criação de Pedidos Simultâneos

        Valida a capacidade do sistema de processar múltiplos pedidos
        simultaneamente sem perda de dados ou inconsistências.
        """
        print("\n" + "="*80)
        print("TESTE DE CARGA: CRIAÇÃO DE PEDIDOS SIMULTÂNEOS")
        print("="*80)

        self.metricas["nome_teste"] = "Criação de Pedidos Simultâneos"

        # Preparar produtos
        print("\n[PREPARAÇÃO] Cadastrando produtos...")
        for i in range(10):
            produto = self.loja.cadastrar_produto(
                i + 1, f"Produto {i + 1}", 50.0)
            produto.definir_estoque(1000)

        quantidade_pedidos = 100
        produtos = list(self.loja.produtos.values())

        print(
            f"\n[TESTE] Criando {quantidade_pedidos} pedidos simultaneamente...")

        def criar_pedido_completo(pedido_id):
            """Função para criar um pedido completo"""
            inicio = time.time()
            try:
                pedido = self.loja.criar_pedido(pedido_id)

                # Adicionar 3 produtos aleatórios
                for i in range(3):
                    produto = produtos[i % len(produtos)]
                    pedido.adicionar_item(produto, 1)

                total = pedido.calcular_total()
                fim = time.time()

                return {
                    "sucesso": True,
                    "pedido_id": pedido_id,
                    "total": total,
                    "tempo": fim - inicio
                }
            except Exception as e:
                fim = time.time()
                return {
                    "sucesso": False,
                    "pedido_id": pedido_id,
                    "erro": str(e),
                    "tempo": fim - inicio
                }

        tempo_inicio = time.time()
        resultados = []

        # Executar criação de pedidos em paralelo
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(criar_pedido_completo, i + 1)
                for i in range(quantidade_pedidos)
            ]

            for future in as_completed(futures):
                resultados.append(future.result())

        tempo_fim = time.time()
        tempo_total = tempo_fim - tempo_inicio

        # Analisar resultados
        sucessos = [r for r in resultados if r["sucesso"]]
        falhas = [r for r in resultados if not r["sucesso"]]
        tempos = [r["tempo"] for r in sucessos]

        if tempos:
            tempo_medio = statistics.mean(tempos)
            tempo_minimo = min(tempos)
            tempo_maximo = max(tempos)
            desvio_padrao = statistics.stdev(tempos) if len(tempos) > 1 else 0
        else:
            tempo_medio = tempo_minimo = tempo_maximo = desvio_padrao = 0

        pedidos_por_segundo = quantidade_pedidos / tempo_total

        print(f"\n✓ Resultados:")
        print(
            f"  - Pedidos criados com sucesso: {len(sucessos)}/{quantidade_pedidos}")
        print(f"  - Pedidos com falha: {len(falhas)}")
        print(f"  - Tempo total: {tempo_total:.3f} segundos")
        print(f"  - Pedidos/segundo: {pedidos_por_segundo:.2f}")
        print(f"  - Tempo médio por pedido: {tempo_medio*1000:.3f} ms")
        print(f"  - Tempo mínimo: {tempo_minimo*1000:.3f} ms")
        print(f"  - Tempo máximo: {tempo_maximo*1000:.3f} ms")
        print(f"  - Desvio padrão: {desvio_padrao*1000:.3f} ms")

        self.metricas["metricas"] = {
            "quantidade_pedidos": quantidade_pedidos,
            "pedidos_sucesso": len(sucessos),
            "pedidos_falha": len(falhas),
            "tempo_total_segundos": tempo_total,
            "pedidos_por_segundo": pedidos_por_segundo,
            "tempo_medio_ms": tempo_medio * 1000,
            "tempo_minimo_ms": tempo_minimo * 1000,
            "tempo_maximo_ms": tempo_maximo * 1000,
            "desvio_padrao_ms": desvio_padrao * 1000
        }

        # Validações
        assert len(
            sucessos) == quantidade_pedidos, f"Alguns pedidos falharam: {len(falhas)} falhas"
        assert tempo_total < 10.0, f"Tempo total muito alto: {tempo_total:.3f}s"
        assert tempo_medio < 0.1, f"Tempo médio muito alto: {tempo_medio:.3f}s"

        print(
            f"\n✓ APROVADO: {len(sucessos)} pedidos criados em {tempo_total:.3f}s")
        print("="*80 + "\n")

        self._salvar_metricas()

    def test_performance_busca_produtos(self):
        """
        Teste de Performance: Busca de Produtos

        Valida o tempo de resposta para operações de busca em um catálogo
        com muitos produtos.
        """
        print("\n" + "="*80)
        print("TESTE DE PERFORMANCE: BUSCA DE PRODUTOS")
        print("="*80)

        self.metricas["nome_teste"] = "Busca de Produtos"

        # Cadastrar 500 produtos
        quantidade = 500
        print(f"\n[PREPARAÇÃO] Cadastrando {quantidade} produtos...")

        for i in range(quantidade):
            produto = self.loja.cadastrar_produto(
                i + 1,
                f"Produto Categoria {i % 10} Item {i}",
                100.0 + i
            )
            produto.definir_estoque(50)

        print(f"✓ {len(self.loja.produtos)} produtos cadastrados")

        # Realizar múltiplas buscas
        print(f"\n[TESTE] Realizando 1000 buscas...")

        quantidade_buscas = 1000
        tempo_inicio = time.time()

        for i in range(quantidade_buscas):
            produto_id = (i % quantidade) + 1
            produto = self.loja.buscar_produto(produto_id)
            assert produto is not None

        tempo_fim = time.time()
        tempo_total = tempo_fim - tempo_inicio

        buscas_por_segundo = quantidade_buscas / tempo_total
        tempo_por_busca = (tempo_total / quantidade_buscas) * 1000  # em ms

        print(f"\n✓ Resultados:")
        print(f"  - Buscas realizadas: {quantidade_buscas}")
        print(f"  - Tempo total: {tempo_total:.3f} segundos")
        print(f"  - Buscas/segundo: {buscas_por_segundo:.2f}")
        print(f"  - Tempo médio por busca: {tempo_por_busca:.3f} ms")

        self.metricas["metricas"] = {
            "quantidade_produtos": quantidade,
            "quantidade_buscas": quantidade_buscas,
            "tempo_total_segundos": tempo_total,
            "buscas_por_segundo": buscas_por_segundo,
            "tempo_medio_ms": tempo_por_busca
        }

        # Validação: deve realizar buscas em menos de 1 segundo
        assert tempo_total < 1.0, f"Tempo de busca muito alto: {tempo_total:.3f}s"
        assert tempo_por_busca < 1.0, f"Tempo médio por busca muito alto: {tempo_por_busca:.3f}ms"

        print(
            f"\n✓ APROVADO: {quantidade_buscas} buscas em {tempo_total:.3f}s")
        print("="*80 + "\n")

        self._salvar_metricas()

    def test_stress_atualizacao_estoque_concorrente(self):
        """
        Teste de Stress: Atualização Concorrente de Estoque

        Valida a consistência do estoque quando múltiplas operações
        tentam modificá-lo simultaneamente.
        """
        print("\n" + "="*80)
        print("TESTE DE STRESS: ATUALIZAÇÃO CONCORRENTE DE ESTOQUE")
        print("="*80)

        self.metricas["nome_teste"] = "Atualização Concorrente de Estoque"

        # Criar produto com estoque inicial
        produto = self.loja.cadastrar_produto(1, "Produto Teste", 100.0)
        estoque_inicial = 1000
        produto.definir_estoque(estoque_inicial)

        print(
            f"\n[PREPARAÇÃO] Produto criado com estoque inicial: {estoque_inicial}")

        quantidade_operacoes = 100
        quantidade_por_operacao = 5

        print(
            f"\n[TESTE] Executando {quantidade_operacoes} operações concorrentes...")
        print(
            f"         Cada operação remove {quantidade_por_operacao} unidades do estoque")

        def remover_estoque():
            """Função para remover itens do estoque"""
            try:
                produto.reduzir_estoque(quantidade_por_operacao)
                return True
            except Exception as e:
                return False

        tempo_inicio = time.time()

        # Executar remoções em paralelo
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(remover_estoque)
                       for _ in range(quantidade_operacoes)]
            resultados = [future.result() for future in as_completed(futures)]

        tempo_fim = time.time()
        tempo_total = tempo_fim - tempo_inicio

        estoque_final = produto.estoque
        estoque_esperado = estoque_inicial - \
            (quantidade_operacoes * quantidade_por_operacao)

        sucessos = sum(1 for r in resultados if r)

        print(f"\n✓ Resultados:")
        print(
            f"  - Operações bem-sucedidas: {sucessos}/{quantidade_operacoes}")
        print(f"  - Estoque inicial: {estoque_inicial}")
        print(f"  - Estoque final: {estoque_final}")
        print(f"  - Estoque esperado: {estoque_esperado}")
        print(f"  - Diferença: {abs(estoque_final - estoque_esperado)}")
        print(f"  - Tempo total: {tempo_total:.3f} segundos")

        self.metricas["metricas"] = {
            "quantidade_operacoes": quantidade_operacoes,
            "operacoes_sucesso": sucessos,
            "estoque_inicial": estoque_inicial,
            "estoque_final": estoque_final,
            "estoque_esperado": estoque_esperado,
            "tempo_total_segundos": tempo_total
        }

        # Validação: o estoque deve estar consistente
        assert estoque_final == estoque_esperado, \
            f"Estoque inconsistente! Esperado: {estoque_esperado}, Obtido: {estoque_final}"

        print(f"\n✓ APROVADO: Estoque consistente após operações concorrentes")
        print("="*80 + "\n")

        self._salvar_metricas()

    def _salvar_metricas(self):
        """Salva as métricas de performance em um arquivo JSON"""
        try:
            os.makedirs("test-results", exist_ok=True)
            nome_arquivo = f"test-results/performance-{self.metricas['nome_teste'].lower().replace(' ', '-')}.json"
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                json.dump(self.metricas, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Aviso: Não foi possível salvar métricas: {e}")


if __name__ == "__main__":
    # Executar testes diretamente
    pytest.main([__file__, "-v", "-s"])
