import time
import random
from typing import List, Tuple, Optional
from collections import defaultdict
import json

class TicTacToe5x5:
    """Jogo da Velha 5x5 - objetivo: alinhar 4 peças"""
    
    def __init__(self):
        self.board = [[' ' for _ in range(5)] for _ in range(5)]
        self.current_player = 'X'
        
    def copy(self):
        """Cria uma cópia do estado atual"""
        new_game = TicTacToe5x5()
        new_game.board = [row[:] for row in self.board]
        new_game.current_player = self.current_player
        return new_game
    
    def get_available_moves(self) -> List[Tuple[int, int]]:
        """Retorna lista de posições vazias"""
        moves = []
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == ' ':
                    moves.append((i, j))
        return moves
    
    def make_move(self, row: int, col: int) -> bool:
        """Faz uma jogada"""
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False
    
    def check_winner(self) -> Optional[str]:
        """Verifica se há um vencedor (4 em linha)"""
        # Verifica linhas
        for i in range(5):
            for j in range(2):
                if (self.board[i][j] != ' ' and
                    self.board[i][j] == self.board[i][j+1] == 
                    self.board[i][j+2] == self.board[i][j+3]):
                    return self.board[i][j]
        
        # Verifica colunas
        for j in range(5):
            for i in range(2):
                if (self.board[i][j] != ' ' and
                    self.board[i][j] == self.board[i+1][j] == 
                    self.board[i+2][j] == self.board[i+3][j]):
                    return self.board[i][j]
        
        # Verifica diagonais (descendentes)
        for i in range(2):
            for j in range(2):
                if (self.board[i][j] != ' ' and
                    self.board[i][j] == self.board[i+1][j+1] == 
                    self.board[i+2][j+2] == self.board[i+3][j+3]):
                    return self.board[i][j]
        
        # Verifica diagonais (ascendentes)
        for i in range(3, 5):
            for j in range(2):
                if (self.board[i][j] != ' ' and
                    self.board[i][j] == self.board[i-1][j+1] == 
                    self.board[i-2][j+2] == self.board[i-3][j+3]):
                    return self.board[i][j]
        
        return None
    
    def is_terminal(self) -> bool:
        """Verifica se o jogo terminou"""
        return self.check_winner() is not None or len(self.get_available_moves()) == 0
    
    def get_utility(self, player: str) -> int:
        """Retorna a utilidade do estado para um jogador"""
        winner = self.check_winner()
        if winner == player:
            return 1000
        elif winner is not None:
            return -1000
        return 0
    
    def print_board(self):
        """Imprime o tabuleiro"""
        print("\n  0 1 2 3 4")
        for i, row in enumerate(self.board):
            print(f"{i} {' '.join(row)}")
        print()


class MinimaxAgent:
    """Agente usando Minimax básico"""
    
    def __init__(self, player: str, max_depth: int = 4):
        self.player = player
        self.opponent = 'O' if player == 'X' else 'X'
        self.max_depth = max_depth
        self.nodes_visited = 0
        
    def heuristic(self, game: TicTacToe5x5) -> int:
        """Função heurística para estados não-terminais"""
        score = 0
        
        # Avalia todas as possíveis sequências de 4
        for i in range(5):
            for j in range(5):
                # Horizontal
                if j <= 1:
                    score += self._evaluate_sequence(game, i, j, 0, 1)
                # Vertical
                if i <= 1:
                    score += self._evaluate_sequence(game, i, j, 1, 0)
                # Diagonal descendente
                if i <= 1 and j <= 1:
                    score += self._evaluate_sequence(game, i, j, 1, 1)
                # Diagonal ascendente
                if i >= 3 and j <= 1:
                    score += self._evaluate_sequence(game, i, j, -1, 1)
        
        return score
    
    def _evaluate_sequence(self, game: TicTacToe5x5, row: int, col: int, 
                          dr: int, dc: int) -> int:
        """Avalia uma sequência de 4 posições"""
        player_count = 0
        opponent_count = 0
        empty_count = 0
        
        for k in range(4):
            r, c = row + k*dr, col + k*dc
            if game.board[r][c] == self.player:
                player_count += 1
            elif game.board[r][c] == self.opponent:
                opponent_count += 1
            else:
                empty_count += 1
        
        # Se ambos os jogadores têm peças, a sequência é inútil
        if player_count > 0 and opponent_count > 0:
            return 0
        
        # Pontuação baseada no número de peças
        if player_count > 0:
            return 10 ** player_count
        elif opponent_count > 0:
            return -(10 ** opponent_count)
        
        return 0
    
    def minimax(self, game: TicTacToe5x5, depth: int, 
                is_maximizing: bool) -> Tuple[int, Optional[Tuple[int, int]]]:
        """Algoritmo Minimax básico"""
        self.nodes_visited += 1
        
        # Caso base: estado terminal ou profundidade máxima
        if depth == 0 or game.is_terminal():
            if game.is_terminal():
                return game.get_utility(self.player), None
            else:
                return self.heuristic(game), None
        
        moves = game.get_available_moves()
        best_move = None
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in moves:
                new_game = game.copy()
                new_game.make_move(move[0], move[1])
                eval_score, _ = self.minimax(new_game, depth - 1, False)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
            
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in moves:
                new_game = game.copy()
                new_game.make_move(move[0], move[1])
                eval_score, _ = self.minimax(new_game, depth - 1, True)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
            
            return min_eval, best_move
    
    def get_best_move(self, game: TicTacToe5x5) -> Tuple[int, int]:
        """Retorna a melhor jogada"""
        self.nodes_visited = 0
        is_maximizing = (game.current_player == self.player)
        _, move = self.minimax(game, self.max_depth, is_maximizing)
        return move


class AlphaBetaAgent:
    """Agente usando Minimax com Poda Alfa-Beta"""
    
    def __init__(self, player: str, max_depth: int = 4):
        self.player = player
        self.opponent = 'O' if player == 'X' else 'X'
        self.max_depth = max_depth
        self.nodes_visited = 0
        self.pruned_branches = 0
        
    def heuristic(self, game: TicTacToe5x5) -> int:
        """Função heurística para estados não-terminais"""
        score = 0
        
        for i in range(5):
            for j in range(5):
                if j <= 1:
                    score += self._evaluate_sequence(game, i, j, 0, 1)
                if i <= 1:
                    score += self._evaluate_sequence(game, i, j, 1, 0)
                if i <= 1 and j <= 1:
                    score += self._evaluate_sequence(game, i, j, 1, 1)
                if i >= 3 and j <= 1:
                    score += self._evaluate_sequence(game, i, j, -1, 1)
        
        return score
    
    def _evaluate_sequence(self, game: TicTacToe5x5, row: int, col: int, 
                          dr: int, dc: int) -> int:
        """Avalia uma sequência de 4 posições"""
        player_count = 0
        opponent_count = 0
        
        for k in range(4):
            r, c = row + k*dr, col + k*dc
            if game.board[r][c] == self.player:
                player_count += 1
            elif game.board[r][c] == self.opponent:
                opponent_count += 1
        
        if player_count > 0 and opponent_count > 0:
            return 0
        
        if player_count > 0:
            return 10 ** player_count
        elif opponent_count > 0:
            return -(10 ** opponent_count)
        
        return 0
    
    def alpha_beta(self, game: TicTacToe5x5, depth: int, alpha: float, 
                   beta: float, is_maximizing: bool) -> Tuple[int, Optional[Tuple[int, int]]]:
        """Algoritmo Minimax com Poda Alfa-Beta"""
        self.nodes_visited += 1
        
        if depth == 0 or game.is_terminal():
            if game.is_terminal():
                return game.get_utility(self.player), None
            else:
                return self.heuristic(game), None
        
        moves = game.get_available_moves()
        best_move = None
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in moves:
                new_game = game.copy()
                new_game.make_move(move[0], move[1])
                eval_score, _ = self.alpha_beta(new_game, depth - 1, alpha, beta, False)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    self.pruned_branches += 1
                    break  # Poda Beta
            
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in moves:
                new_game = game.copy()
                new_game.make_move(move[0], move[1])
                eval_score, _ = self.alpha_beta(new_game, depth - 1, alpha, beta, True)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    self.pruned_branches += 1
                    break  # Poda Alfa
            
            return min_eval, best_move
    
    def get_best_move(self, game: TicTacToe5x5) -> Tuple[int, int]:
        """Retorna a melhor jogada"""
        self.nodes_visited = 0
        self.pruned_branches = 0
        is_maximizing = (game.current_player == self.player)
        _, move = self.alpha_beta(game, self.max_depth, float('-inf'), 
                                   float('inf'), is_maximizing)
        return move


def simulate_game(agent1, agent2, verbose=False):
    """Simula uma partida entre dois agentes"""
    game = TicTacToe5x5()
    agents = {'X': agent1, 'O': agent2}
    
    move_count = 0
    total_time = {'X': 0, 'O': 0}
    total_nodes = {'X': 0, 'O': 0}
    
    while not game.is_terminal():
        current_agent = agents[game.current_player]
        
        start_time = time.time()
        move = current_agent.get_best_move(game)
        elapsed_time = time.time() - start_time
        
        total_time[game.current_player] += elapsed_time
        total_nodes[game.current_player] += current_agent.nodes_visited
        
        if verbose:
            print(f"\nJogador {game.current_player} - Jogada: {move}")
            print(f"Tempo: {elapsed_time:.4f}s, Nós visitados: {current_agent.nodes_visited}")
        
        game.make_move(move[0], move[1])
        move_count += 1
        
        if verbose:
            game.print_board()
    
    winner = game.check_winner()
    
    results = {
        'winner': winner if winner else 'Empate',
        'moves': move_count,
        'time_X': total_time['X'],
        'time_O': total_time['O'],
        'nodes_X': total_nodes['X'],
        'nodes_O': total_nodes['O']
    }
    
    return results


def run_experiments(num_games=10, depth=4):
    """Executa múltiplas partidas e coleta estatísticas"""
    print(f"\n{'='*60}")
    print(f"EXPERIMENTO: {num_games} partidas com profundidade {depth}")
    print(f"{'='*60}\n")
    
    results = {
        'minimax_vs_alphabeta': [],
        'alphabeta_vs_minimax': []
    }
    
    # Minimax (X) vs Alpha-Beta (O)
    print("Partidas: Minimax (X) vs Alpha-Beta (O)")
    for i in range(num_games):
        agent_minimax = MinimaxAgent('X', depth)
        agent_alphabeta = AlphaBetaAgent('O', depth)
        
        result = simulate_game(agent_minimax, agent_alphabeta, verbose=False)
        results['minimax_vs_alphabeta'].append(result)
        print(f"Partida {i+1}: Vencedor = {result['winner']}, "
              f"Jogadas = {result['moves']}, "
              f"Tempo X = {result['time_X']:.3f}s, "
              f"Tempo O = {result['time_O']:.3f}s")
    
    print("\n" + "-"*60 + "\n")
    
    # Alpha-Beta (X) vs Minimax (O)
    print("Partidas: Alpha-Beta (X) vs Minimax (O)")
    for i in range(num_games):
        agent_alphabeta = AlphaBetaAgent('X', depth)
        agent_minimax = MinimaxAgent('O', depth)
        
        result = simulate_game(agent_alphabeta, agent_minimax, verbose=False)
        results['alphabeta_vs_minimax'].append(result)
        print(f"Partida {i+1}: Vencedor = {result['winner']}, "
              f"Jogadas = {result['moves']}, "
              f"Tempo X = {result['time_X']:.3f}s, "
              f"Tempo O = {result['time_O']:.3f}s")
    
    return results


def analyze_results(results):
    """Analisa e imprime estatísticas dos resultados"""
    print("\n" + "="*60)
    print("ANÁLISE DOS RESULTADOS")
    print("="*60 + "\n")
    
    for config, games in results.items():
        print(f"\nConfiguração: {config}")
        print("-" * 40)
        
        wins = {'X': 0, 'O': 0, 'Empate': 0}
        total_time_x = 0
        total_time_o = 0
        total_nodes_x = 0
        total_nodes_o = 0
        
        for game in games:
            wins[game['winner']] += 1
            total_time_x += game['time_X']
            total_time_o += game['time_O']
            total_nodes_x += game['nodes_X']
            total_nodes_o += game['nodes_O']
        
        n = len(games)
        print(f"Vitórias X: {wins['X']} ({wins['X']/n*100:.1f}%)")
        print(f"Vitórias O: {wins['O']} ({wins['O']/n*100:.1f}%)")
        print(f"Empates: {wins['Empate']} ({wins['Empate']/n*100:.1f}%)")
        print(f"\nTempo médio X: {total_time_x/n:.4f}s")
        print(f"Tempo médio O: {total_time_o/n:.4f}s")
        print(f"Nós médios X: {total_nodes_x/n:.0f}")
        print(f"Nós médios O: {total_nodes_o/n:.0f}")
        
        if 'minimax' in config and 'alphabeta' in config:
            speedup = (total_time_x / total_time_o) if 'minimax_vs' in config else (total_time_o / total_time_x)
            efficiency = (total_nodes_x / total_nodes_o) if 'minimax_vs' in config else (total_nodes_o / total_nodes_x)
            print(f"\nSpeedup (Alfa-Beta): {speedup:.2f}x")
            print(f"Eficiência de nós (Alfa-Beta): {efficiency:.2f}x menos nós")


if __name__ == "__main__":
    # Exemplo de uso: uma partida interativa
    print("Demonstração: Uma partida entre Minimax e Alfa-Beta\n")
    
    game = TicTacToe5x5()
    agent_x = MinimaxAgent('X', max_depth=4)
    agent_o = AlphaBetaAgent('O', max_depth=4)
    
    print("Jogador X: Minimax")
    print("Jogador O: Alpha-Beta com Poda\n")
    
    game.print_board()
    
    while not game.is_terminal():
        if game.current_player == 'X':
            agent = agent_x
            print("\nTurno do Minimax (X)...")
        else:
            agent = agent_o
            print("\nTurno do Alpha-Beta (O)...")
        
        start = time.time()
        move = agent.get_best_move(game)
        elapsed = time.time() - start
        
        print(f"Jogada escolhida: {move}")
        print(f"Tempo: {elapsed:.4f}s")
        print(f"Nós visitados: {agent.nodes_visited}")
        if isinstance(agent, AlphaBetaAgent):
            print(f"Podas realizadas: {agent.pruned_branches}")
        
        game.make_move(move[0], move[1])
        game.print_board()
    
    winner = game.check_winner()
    if winner:
        print(f"\nVencedor: {winner}!")
    else:
        print("\nEmpate!")
    
    # Executar experimentos completos
    print("\n" + "="*60)
    print("INICIANDO EXPERIMENTOS COMPARATIVOS")
    print("="*60)
    
    results = run_experiments(num_games=5, depth=4)
    analyze_results(results)