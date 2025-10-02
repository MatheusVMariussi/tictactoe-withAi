import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List
import json

def plot_performance_comparison(results: Dict, depth: int):
    """Gera gráficos comparativos de desempenho"""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Comparação Minimax vs Alpha-Beta (Profundidade {depth})', 
                 fontsize=16, fontweight='bold')
    
    # Extrair dados
    configs = list(results.keys())
    
    # Dados para Minimax e Alpha-Beta
    minimax_times = []
    alphabeta_times = []
    minimax_nodes = []
    alphabeta_nodes = []
    
    for config, games in results.items():
        for game in games:
            if 'minimax_vs' in config:
                minimax_times.append(game['time_X'])
                alphabeta_times.append(game['time_O'])
                minimax_nodes.append(game['nodes_X'])
                alphabeta_nodes.append(game['nodes_O'])
            else:
                alphabeta_times.append(game['time_X'])
                minimax_times.append(game['time_O'])
                alphabeta_nodes.append(game['nodes_X'])
                minimax_nodes.append(game['nodes_O'])
    
    # Gráfico 1: Tempo de Execução Médio
    ax1 = axes[0, 0]
    agents = ['Minimax', 'Alpha-Beta']
    avg_times = [np.mean(minimax_times), np.mean(alphabeta_times)]
    std_times = [np.std(minimax_times), np.std(alphabeta_times)]
    
    bars1 = ax1.bar(agents, avg_times, yerr=std_times, capsize=5, 
                    color=['#FF6B6B', '#4ECDC4'], alpha=0.7, edgecolor='black')
    ax1.set_ylabel('Tempo (segundos)', fontweight='bold')
    ax1.set_title('Tempo de Execução Médio por Jogada', fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Adicionar valores nas barras
    for i, (bar, val) in enumerate(zip(bars1, avg_times)):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + std_times[i],
                f'{val:.4f}s', ha='center', va='bottom', fontweight='bold')
    
    # Gráfico 2: Nós Visitados
    ax2 = axes[0, 1]
    avg_nodes = [np.mean(minimax_nodes), np.mean(alphabeta_nodes)]
    std_nodes = [np.std(minimax_nodes), np.std(alphabeta_nodes)]
    
    bars2 = ax2.bar(agents, avg_nodes, yerr=std_nodes, capsize=5,
                    color=['#FF6B6B', '#4ECDC4'], alpha=0.7, edgecolor='black')
    ax2.set_ylabel('Número de Nós', fontweight='bold')
    ax2.set_title('Nós Visitados Médio por Jogada', fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    for i, (bar, val) in enumerate(zip(bars2, avg_nodes)):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + std_nodes[i],
                f'{int(val)}', ha='center', va='bottom', fontweight='bold')
    
    # Gráfico 3: Eficiência (Speedup e Redução de Nós)
    ax3 = axes[1, 0]
    speedup = np.mean(minimax_times) / np.mean(alphabeta_times)
    node_reduction = np.mean(minimax_nodes) / np.mean(alphabeta_nodes)
    
    metrics = ['Speedup\n(Tempo)', 'Redução de Nós']
    values = [speedup, node_reduction]
    
    bars3 = ax3.bar(metrics, values, color=['#95E1D3', '#F38181'], 
                    alpha=0.7, edgecolor='black')
    ax3.set_ylabel('Fator de Melhoria', fontweight='bold')
    ax3.set_title('Ganho de Eficiência com Poda Alpha-Beta', fontweight='bold')
    ax3.axhline(y=1, color='red', linestyle='--', linewidth=2, label='Baseline (1x)')
    ax3.legend()
    ax3.grid(axis='y', alpha=0.3)
    
    for bar, val in zip(bars3, values):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f'{val:.2f}x', ha='center', va='bottom', 
                fontweight='bold', fontsize=12)
    
    # Gráfico 4: Distribuição de Vitórias
    ax4 = axes[1, 1]
    
    wins_summary = {'Minimax': 0, 'Alpha-Beta': 0, 'Empate': 0}
    
    for config, games in results.items():
        for game in games:
            winner = game['winner']
            if winner == 'X':
                if 'minimax_vs' in config:
                    wins_summary['Minimax'] += 1
                else:
                    wins_summary['Alpha-Beta'] += 1
            elif winner == 'O':
                if 'minimax_vs' in config:
                    wins_summary['Alpha-Beta'] += 1
                else:
                    wins_summary['Minimax'] += 1
            else:
                wins_summary['Empate'] += 1
    
    labels = list(wins_summary.keys())
    sizes = list(wins_summary.values())
    colors = ['#FF6B6B', '#4ECDC4', '#FFE66D']
    explode = (0.05, 0.05, 0.05)
    
    ax4.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90, textprops={'fontweight': 'bold'})
    ax4.set_title('Distribuição de Resultados', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('comparacao_minimax_alphabeta.png', dpi=300, bbox_inches='tight')
    print("Gráfico salvo: comparacao_minimax_alphabeta.png")
    plt.show()


def plot_depth_analysis(depths: List[int], results_by_depth: Dict):
    """Analisa o impacto da profundidade de busca"""
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Impacto da Profundidade de Busca', fontsize=16, fontweight='bold')
    
    minimax_times_by_depth = []
    alphabeta_times_by_depth = []
    minimax_nodes_by_depth = []
    alphabeta_nodes_by_depth = []
    
    for depth in depths:
        results = results_by_depth[depth]
        
        mm_times = []
        ab_times = []
        mm_nodes = []
        ab_nodes = []
        
        for config, games in results.items():
            for game in games:
                if 'minimax_vs' in config:
                    mm_times.append(game['time_X'])
                    ab_times.append(game['time_O'])
                    mm_nodes.append(game['nodes_X'])
                    ab_nodes.append(game['nodes_O'])
                else:
                    ab_times.append(game['time_X'])
                    mm_times.append(game['time_O'])
                    ab_nodes.append(game['nodes_X'])
                    mm_nodes.append(game['nodes_O'])
        
        minimax_times_by_depth.append(np.mean(mm_times))
        alphabeta_times_by_depth.append(np.mean(ab_times))
        minimax_nodes_by_depth.append(np.mean(mm_nodes))
        alphabeta_nodes_by_depth.append(np.mean(ab_nodes))
    
    # Gráfico 1: Tempo vs Profundidade
    ax1 = axes[0]
    ax1.plot(depths, minimax_times_by_depth, 'o-', label='Minimax', 
             linewidth=2, markersize=8, color='#FF6B6B')
    ax1.plot(depths, alphabeta_times_by_depth, 's-', label='Alpha-Beta',
             linewidth=2, markersize=8, color='#4ECDC4')
    ax1.set_xlabel('Profundidade de Busca', fontweight='bold')
    ax1.set_ylabel('Tempo Médio (segundos)', fontweight='bold')
    ax1.set_title('Tempo de Execução vs Profundidade', fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(depths)
    
    # Gráfico 2: Nós vs Profundidade
    ax2 = axes[1]
    ax2.plot(depths, minimax_nodes_by_depth, 'o-', label='Minimax',
             linewidth=2, markersize=8, color='#FF6B6B')
    ax2.plot(depths, alphabeta_nodes_by_depth, 's-', label='Alpha-Beta',
             linewidth=2, markersize=8, color='#4ECDC4')
    ax2.set_xlabel('Profundidade de Busca', fontweight='bold')
    ax2.set_ylabel('Nós Visitados Médio', fontweight='bold')
    ax2.set_title('Nós Visitados vs Profundidade', fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(depths)
    
    plt.tight_layout()
    plt.savefig('analise_profundidade.png', dpi=300, bbox_inches='tight')
    print("Gráfico salvo: analise_profundidade.png")
    plt.show()


def generate_report_table(results: Dict):
    """Gera tabela formatada para o relatório"""
    
    print("\n" + "="*80)
    print("TABELA DE RESULTADOS PARA O RELATÓRIO")
    print("="*80 + "\n")
    
    print("Tabela 1: Métricas de Desempenho Médio")
    print("-" * 80)
    print(f"{'Algoritmo':<20} {'Tempo Médio (s)':<20} {'Nós Visitados':<20} {'Desvio Padrão':<20}")
    print("-" * 80)
    
    minimax_times = []
    alphabeta_times = []
    minimax_nodes = []
    alphabeta_nodes = []
    
    for config, games in results.items():
        for game in games:
            if 'minimax_vs' in config:
                minimax_times.append(game['time_X'])
                alphabeta_times.append(game['time_O'])
                minimax_nodes.append(game['nodes_X'])
                alphabeta_nodes.append(game['nodes_O'])
            else:
                alphabeta_times.append(game['time_X'])
                minimax_times.append(game['time_O'])
                alphabeta_nodes.append(game['nodes_X'])
                minimax_nodes.append(game['nodes_O'])
    
    print(f"{'Minimax':<20} {np.mean(minimax_times):<20.6f} {np.mean(minimax_nodes):<20.0f} {np.std(minimax_times):<20.6f}")
    print(f"{'Alpha-Beta':<20} {np.mean(alphabeta_times):<20.6f} {np.mean(alphabeta_nodes):<20.0f} {np.std(alphabeta_times):<20.6f}")
    print("-" * 80)
    
    speedup = np.mean(minimax_times) / np.mean(alphabeta_times)
    node_reduction = np.mean(minimax_nodes) / np.mean(alphabeta_nodes)
    
    print(f"\nSpeedup (Alpha-Beta): {speedup:.2f}x")
    print(f"Redução de Nós: {node_reduction:.2f}x ({(1-1/node_reduction)*100:.1f}% menos nós)")
    
    print("\n" + "="*80)
    print("Tabela 2: Resultados das Partidas")
    print("-" * 80)
    
    wins = {'Minimax': 0, 'Alpha-Beta': 0, 'Empate': 0}
    total_games = 0
    
    for config, games in results.items():
        for game in games:
            total_games += 1
            winner = game['winner']
            if winner == 'X':
                if 'minimax_vs' in config:
                    wins['Minimax'] += 1
                else:
                    wins['Alpha-Beta'] += 1
            elif winner == 'O':
                if 'minimax_vs' in config:
                    wins['Alpha-Beta'] += 1
                else:
                    wins['Minimax'] += 1
            else:
                wins['Empate'] += 1
    
    print(f"{'Resultado':<20} {'Quantidade':<15} {'Porcentagem':<15}")
    print("-" * 80)
    for key, value in wins.items():
        print(f"{key:<20} {value:<15} {value/total_games*100:<15.1f}%")
    print("-" * 80)
    print(f"{'Total de Partidas':<20} {total_games}")
    print("="*80 + "\n")


def save_results_to_json(results: Dict, filename: str = 'resultados_experimento.json'):
    """Salva resultados em formato JSON para análise posterior"""
    
    # Converter para formato serializável
    serializable_results = {}
    for config, games in results.items():
        serializable_results[config] = []
        for game in games:
            serializable_results[config].append({
                'winner': game['winner'],
                'moves': game['moves'],
                'time_X': float(game['time_X']),
                'time_O': float(game['time_O']),
                'nodes_X': int(game['nodes_X']),
                'nodes_O': int(game['nodes_O'])
            })
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(serializable_results, f, indent=2, ensure_ascii=False)
    
    print(f"Resultados salvos em: {filename}")


# Exemplo de uso completo
if __name__ == "__main__":
    # Importar a implementação principal
    from tictactoe_5x5 import run_experiments, MinimaxAgent, AlphaBetaAgent, TicTacToe5x5, simulate_game
    
    print("="*80)
    print("ANÁLISE COMPLETA: MINIMAX VS ALPHA-BETA")
    print("="*80 + "\n")
    
    # Experimento 1: Comparação com profundidade fixa
    print("Executando experimentos com profundidade 4...")
    results_depth4 = run_experiments(num_games=10, depth=4)
    
    # Gerar gráficos
    plot_performance_comparison(results_depth4, depth=4)
    
    # Gerar tabela
    generate_report_table(results_depth4)
    
    # Salvar resultados
    save_results_to_json(results_depth4, 'resultados_profundidade4.json')
    
    # Experimento 2: Análise de diferentes profundidades
    print("\n" + "="*80)
    print("ANÁLISE DE IMPACTO DA PROFUNDIDADE")
    print("="*80 + "\n")
    
    depths = [2, 3, 4, 5]
    results_by_depth = {}
    
    for depth in depths:
        print(f"\nTestando profundidade {depth}...")
        results_by_depth[depth] = run_experiments(num_games=5, depth=depth)
    
    plot_depth_analysis(depths, results_by_depth)
    
    # Análise adicional: Taxa de poda
    print("\n" + "="*80)
    print("ANÁLISE DA EFICIÊNCIA DA PODA ALFA-BETA")
    print("="*80 + "\n")
    
    game = TicTacToe5x5()
    ab_agent = AlphaBetaAgent('X', max_depth=4)
    
    # Fazer uma jogada para demonstrar
    move = ab_agent.get_best_move(game)
    
    print(f"Nós visitados: {ab_agent.nodes_visited}")
    print(f"Podas realizadas: {ab_agent.pruned_branches}")
    print(f"Taxa de poda: {ab_agent.pruned_branches/ab_agent.nodes_visited*100:.2f}%")
    
    print("\n" + "="*80)
    print("ANÁLISE CONCLUÍDA!")
    print("="*80 + "\n")
