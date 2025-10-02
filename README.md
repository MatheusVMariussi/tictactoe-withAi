# TDE 2 - Busca Competitiva: Minimax vs Poda Alfa-Beta

## 📋 Descrição do Projeto

Implementação e análise comparativa dos algoritmos Minimax e Minimax com Poda Alfa-Beta aplicados ao jogo da velha em um tabuleiro 5x5, onde o objetivo é alinhar 4 peças consecutivas.

## 🎯 Objetivos

- Implementar o algoritmo Minimax básico
- Implementar Minimax com otimização Poda Alfa-Beta
- Comparar desempenho computacional (tempo e nós visitados)
- Analisar qualidade das decisões
- Avaliar trade-offs entre os algoritmos

## 🛠️ Requisitos

### Dependências

```bash
python >= 3.7
numpy
matplotlib
```

### Instalação

```bash
# Criar ambiente virtual (opcional, mas recomendado)
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install numpy matplotlib
```

## 📁 Estrutura do Projeto

```
TDE2-Minimax-AlphaBeta/
│
├── tictactoe_5x5.py          # Implementação principal do jogo e agentes
├── analysis_plots.py          # Scripts de análise e visualização
├── report_template.md         # Template do relatório
├── README.md                  # Este arquivo
│
├── resultados/                # Diretório para resultados (criado automaticamente)
│   ├── resultados_profundidade4.json
│   ├── comparacao_minimax_alphabeta.png
│   └── analise_profundidade.png
│
└── relatorio/                 # Diretório para o relatório final
    └── TDE2_Relatorio.pdf
```

## 🚀 Como Executar

### 1. Partida Demonstrativa

Execute uma partida única entre Minimax e Alpha-Beta:

```bash
python tictactoe_5x5.py
```

**Saída esperada:**
- Visualização do tabuleiro após cada jogada
- Tempo de execução de cada movimento
- Número de nós visitados
- Podas realizadas (Alpha-Beta)
- Resultado final

### 2. Experimentos Completos

Execute múltiplas partidas e colete estatísticas:

```python
# No arquivo tictactoe_5x5.py, na seção main:
results = run_experiments(num_games=10, depth=4)
analyze_results(results)
```

**Parâmetros:**
- `num_games`: Número de partidas a simular
- `depth`: Profundidade máxima de busca

### 3. Análise com Gráficos

Gere gráficos e análises visuais:

```bash
python analysis_plots.py
```

**Gráficos gerados:**
1. Comparação de tempo de execução
2. Nós visitados por algoritmo
3. Ganho de eficiência (speedup)
4. Distribuição de vitórias
5. Impacto da profundidade

### 4. Experimentos com Diferentes Profundidades

```python
from tictactoe_5x5 import run_experiments
from analysis_plots import plot_depth_analysis

depths = [2, 3, 4, 5]
results_by_depth = {}

for depth in depths:
    results_by_depth[depth] = run_experiments(num_games=5, depth=depth)

plot_depth_analysis(depths, results_by_depth)
```

## 📊 Interpretando os Resultados

### Métricas Coletadas

1. **Tempo de Execução**: Tempo total gasto por cada agente em todas as suas jogadas
2. **Nós Visitados**: Número de estados explorados durante a busca
3. **Podas Realizadas**: Número de ramos cortados pela poda alfa-beta
4. **Resultado da Partida**: Vencedor (X, O ou Empate)

### Exemplo de Saída

```
Partida 1: Vencedor = X, Jogadas = 17, Tempo X = 2.453s, Tempo O = 0.987s

ANÁLISE DOS RESULTADOS
==================================================
Configuração: minimax_vs_alphabeta
Vitórias X: 5 (50.0%)
Vitórias O: 4 (40.0%)
Empates: 1 (10.0%)

Tempo médio X (Minimax): 2.3456s
Tempo médio O (Alpha-Beta): 0.9234s
Nós médios X: 145023
Nós médios O: 52341

Speedup (Alfa-Beta): 2.54x
Eficiência de nós (Alfa-Beta): 2.77x menos nós
```

## 🧪 Experimentos Recomendados

### Experimento 1: Comparação Básica
```python
# Profundidade 4, 10 partidas
results = run_experiments(num_games=10, depth=4)
analyze_results(results)
```

### Experimento 2: Análise de Profundidade
```python
# Teste com profundidades 2, 3, 4, 5
for depth in [2, 3, 4, 5]:
    print(f"\n=== Profundidade {depth} ===")
    results = run_experiments(num_games=5, depth=depth)
    analyze_results(results)
```

### Experimento 3: Análise Detalhada de Uma Partida
```python
game = TicTacToe5x5()
agent_x = MinimaxAgent('X', max_depth=4)
agent_o = AlphaBetaAgent('O', max_depth=4)

result = simulate_game(agent_x, agent_o, verbose=True)
```