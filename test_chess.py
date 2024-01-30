# pip3 install python-chess


import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from AlphaBetaAIZobristEC import AlphaBetaAIZobristEC
from ChessGame import ChessGame


import sys


player1 = HumanPlayer()
player2 = RandomAI()
player3 = MinimaxAI(depth = 3, use_ids=False)
player4 = AlphaBetaAI(depth = 4)
player5 = AlphaBetaAIZobristEC(depth = 4)

#game = ChessGame(player1, player2)
#game = ChessGame(player1, player3)
game = ChessGame(player1, player4)
#game = ChessGame(player1, player5)

while not game.is_game_over():
    print(game)
    game.make_move()


#print(hash(str(game.board)))
