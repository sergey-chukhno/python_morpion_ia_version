from player import AiPlayer, HumanPlayer, ComputerPlayer

class TicTacToe:
  def __init__(self):
    self.board = [" " for _ in range(9)] # on crée une liste pour représenter notre échiquier 3x3
    self.current_winner = None # pour tenir compte si actuellement il y a un gagnant
#La fonction pour imprimer notre échiquier
  def print_board(self):
    # pour définir une ligne
    for row in [self.board[i*3:(i+1)*3] for i  in range(3)]:
      print('| ' + ' | '.join(row) + ' I')
  
  @staticmethod #quand on n'utilise pas 'self'
  def print_board_nums():
    #la fonction définit quel nombre correspond à quel casier
    number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
    for row in number_board:
      print('| ' + ' | '.join(row) + ' I')
  
  #La fonction qui définit quel sont les casiers dispo après qu'on ait fait un coup
  def available_moves(self):
    #return []
    moves = []
    for (i, spot) in  enumerate(self.board):
      # on utilise 'enumerate' pour assigner l'index à nos lettres 'x' ou 'o': par exemple, pour ['x', 'x', 'o'] ==> [(0, x), (1, x), (2, o)]
      if spot == ' ': #si spot est un espace libre, on le rajoute à notre liste de moves disponibles
        moves.append(i)
    return moves # Retourne la liste de cases disponibles
  
  def empty_squares(self):
    return ' ' in self.board
  
  def num_empty_squares(self):
    return self.board.count(' ')
  
  def make_move(self, square, letter):
    #si le coup joué est valide, on assigne une case libre à une lettre 'x' ou 'o'
    #si le coup est joué, on retourne 'True", si le coup n'est pas joué, on retourne "False"
    if self.board[square] == ' ':
      self.board[square] = letter
      if self.winner(square, letter):
        self.current_winner= letter
      return True
    else:
      return False
    
  def winner(self, square, letter):
    # la fonction qui définit le gagnant 
    # on sait qu'un joueur gagne s'il arrive à mettre trois lettres en colonne ou en diagonale

    # on vérifie s'il y a trois mêmes lettres en ligne
    row_ind = square // 3
    row = self.board[row_ind * 3: (row_ind + 1)*3]
    if all([spot == letter for spot in row]):
      return True
    
    # on vérifie s'il y a trois cases avec la même lettre en colonne:
    col_ind = square % 3
    column = [self.board[col_ind + i*3] for i in range(3)]
    if all([spot == letter for spot in column]):
      return True
    
    # on vérifie s'il y a trois cases avec la même lettre en diagonel (les cases de diagonale étant 0, 2, 4, 6)
    if square % 2 == 0:
      diagonal1 = [self.board[i] for i in [0, 4, 8]] #la diagonale de gauche à droite
      if all([spot == letter for spot in diagonal1]):
        return True
      diagonal2 = [self.board[i] for i in [2, 4, 6]] #la diagonale de droite à gauche
      if all([spot == letter for spot in diagonal2]):
        return True
      
    else:
      return False



def play(game, x_player, o_player, print_game = True): #La fonction qui détermine le déroulement du jeu. Elle prend en compte l'echiquier, les joueurs x et o
  if print_game: 
    game.print_board_nums()

  letter = 'X'
  #continuer tant que le game a des cases libres
  while game.empty_squares(): #tant qu'il y a des cases libres, on veut qu'un de nos joueurs joue son tour
    if letter == 'O': #si la lettre est égale à O, on veut que le joueur 'o' fasse son tour
      square = o_player.get_move(game) 
    else: #sinon c'est le joueur 'x' qui joue
      square = x_player.get_move(game)

    #on crée la fonction pour jouer un tour
    if game.make_move(square, letter): 
      if print_game:
        print(letter + f'makes a move to {square}')
        game.print_board()

      if game.current_winner: 
        if print_game: 
          print(letter + ' wins!🥳🥳🥳')
          return letter


      #après qu'un joueur ait joué son tour, on doit alterner les lettres - c'est le tour d'un autre joueur de jouer
      if letter == 'X':
        letter = 'O'
      else: 
        letter = 'X'
      
  if print_game:
      print('It\'s a tie😳😳😳')

if __name__ == '__main__':
  x_player = HumanPlayer('X')
  o_player = AiPlayer('O')
  ttc = TicTacToe()
  play(ttc, x_player, o_player, print_game=True)
