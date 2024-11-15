import math 
import random


class Player:
  def __init__(self, letter):
    # la lettre x ou o choisi par un joueur
    self.letter = letter

  #le coup de chacun des joueurs
  def get_move(self, game): 
    pass

class ComputerPlayer(Player):
  def __init__(self, letter):
    super().__init__(letter)
  
  def get_move(self, game):
    square = random.choice(game.available_moves()) #On utilise random.choice pour que l'ordinateur choisie au hasard un case disponible
    return square  

class HumanPlayer(Player):
  def __init__(self, letter):
    super().__init__(letter)
  
  def get_move(self, game):
    valid_square = False
    val = None
    while not valid_square: 
      square = input(self.letter + '\s turn. Input move (0-8):')
      # On va s'assurer que la valeur introduite par le joueur est un int et que la case choisie est libre
      try: 
        val=int(square)
        if val not in game.available_moves():
          raise ValueError
        valid_square = True
      except ValueError:
        print('Invalid square. Please try again.')
    return val

class AiPlayer(Player):
  def __init__(self, letter):
    super().__init__(letter)
  
  def get_move(self, game):
    # Début du jeu quad toutes les cases sont libres: on dit au joueur de choisir n'importe quelle case: 
    if len(game.available_moves()) == 9:
      square = random.choice(game.available_moves())
    else: 
      # le joueur doit choisir une case selon l'algorithme minimax:
      square = self.minimax(game, self.letter)['position']
    return square
  
  #Définition de l'algorithme minimax
  def minimax(self, state, player): # Par 'state' on comprend l'état du jeu, c-a-d les options du jeu qui existent à un moment (à chaque étape) du jeu
    max_player = self.letter # C'est le joueur qui cherche à maximiser son utilité (obtenir le plus grand score possible) pour gagner le jeu
    other_player = 'O' if player == 'X' else 'X' #l'autre joueur, qu'on peut aussi nommer min_player cherche à minimer l'utilité du max_player, donc à minimiser son score et ses chances de gagner, en bloquant les pistes victorieuses et en chrchant à prendre contrôle sur le jeu. De cette manière, on s'assure que tous les deux joueurs sont rationnels : ils cherchent à maximiser ses chances de victoires tout en tenant compte des choix et du comportement de l'adversaire.

    # d'abord, on vérifie si le coup précédant n'a pas donné du gagnant
    if state.current_winner == other_player:
      # on doit retourner la position du joueur et le score, car la fonction minimax cherce à maximier l'utilité, donc on doit tenir compte du score pour que l'algorithme minimax puisse fonctionner. On calcule l'utilité selon le formule: a * b, où a est égale à 1 en cas de victoire, 0 en cas de match nul et -1 en cas de défaite; b est égale au nombre de cases libres restants; 
      return {
        'position': None, 
        'score': 1 * (state.num_empty_squares()+1) if other_player == max_player else -1 * (state.num_empty_squares()+1)
        } # on retourne donc un dictionnaire que contient la position et le score calculé selon la formule décrite ci-dessus
    elif not state.empty_squares(): #s'il n'y a pas de gagnant et il ne reste plus de cases libres
      return {
        'position': None, 
        'score': 0
      }
    
    if player == max_player:
      best = {
        'position': None, 
        'score': -math.inf
      } # on cherche la meilleur solution, en comparant les scores possibles. On veut commencer par le score le plus petit possible (d'où on le met égale à l'infinité négative qui est plus petit que n'importe quel nombre réel existant)
    else: 
      best = {
        'position': None, 
        'score': math.inf
      } #si le joueur n'est pas 'max player', on cherche à minimser son score, donc on initialize son score avec le plus score possible
    
    for possible_move in state.available_moves():
      # étape 1: on essaie une case
      state.make_move(possible_move, player)
      # étape 2: on fait l'usage recursif de notre algorithme minimax pour simuler les options qui apparaissent après qu'on ait fait un coup 
      simulated_score = self.minimax(state, other_player) # à cette étape, on alterne de joueurs
      # étape 3: on fait un pas en arrière pour essayer un autre coup (une autre case)
      state.board[possible_move] = ' '
      state.current_winner = None
      simulated_score['position'] = possible_move
      # étape 4: on met à jour notre disctionnaire 
      if player == max_player: 
        if simulated_score['score'] > best['score']:
          best = simulated_score
      else: 
        if simulated_score['score'] < best['score']:
          best = simulated_score
    return best


  
 
