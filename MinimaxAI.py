# Andy Xu
# Date: 10/3/23

import chess
import math

class MinimaxAI():
    def __init__(self, depth, use_ids):
        self.depth = depth # maximum depth
        self.num_nodes = 0 # number of nodes visited
        self.use_ids = use_ids # boolean that determines whether to use iterative deepening

    def choose_move(self, board):
        if self.use_ids:
            return self.ids_choose_move(board)
        else:
            value, move = self.max_value(board, 0)
            print(self.num_nodes)
            print(self.depth)
            print("Minimax AI recommending move " + str(move))
            return move

    # Choose move function that implements iterative deepening
    def ids_choose_move(self, board):
        best_move = None
        best_value = -math.inf
        max_depth = self.depth

        # for loop to explore depths unti max depth
        for i in range(1, max_depth+1):
            self.depth = i
            value, move = self.max_value(board, 0)
            # update best move if current move is better
            if move and (value > best_value):
                best_move = move
                best_value = value

        print("IDS Minimax AI recommending move " + str(best_move))
        print(self.num_nodes)
        print(self.depth)
        return best_move

    # Max Value function as described by textbook
    def max_value(self, board, cur_depth):
        cur_depth += 1
        self.num_nodes += 1

        # check for terminal state
        if self.cutoff_test(board, cur_depth):
            if board.is_checkmate():
                return -math.inf, board.peek()
            return self.utility(board), board.peek()

        # get possible moves
        moves = list(board.legal_moves)

        # iterate through possible moves to find best possible move
        v = -math.inf
        best = None
        for m in moves:
            board.push(m)
            min_v, min_m = self.min_value(board, cur_depth)
            if min_v > v:
                best = m
                v = min_v
            board.pop()

        return v, best

    # Min Value function as described by textbook
    def min_value(self, board, cur_depth):
        cur_depth += 1
        self.num_nodes += 1

        # check for terminal state
        if self.cutoff_test(board, cur_depth):
            if board.is_checkmate():
                return math.inf, board.peek()
            return self.utility(board), board.peek()

        # get possible moves
        moves = list(board.legal_moves)

        # iterate through possible moves to get best possible move
        v = math.inf
        best = None
        for m in moves:
            board.push(m)
            max_v, max_m = self.max_value(board, cur_depth)
            if max_v < v:
                best = m
                v = max_v
            board.pop()

        return v, best

    # cutoff test for depth limited minimax search, returns True if terminal state
    # has been reached (win or draw) or if we have reached specified maximum depth
    def cutoff_test(self, board, cur_depth):
        return board.is_game_over() or cur_depth > self.depth

    # function to calculate utility of terminal state
    def utility(self, board):
        pts = 0
        piece_pts = {
            1: 1, #Pawn
            2: 3, #Knight
            3: 3, #Bishop
            4: 5, #Rook
            5: 9, #Queen
            6: 0  #King
        }
        pieces = board.piece_map()
        for piece in pieces.values():
            if piece.color:
                pts -= piece_pts[piece.piece_type]
            else:
                pts += piece_pts[piece.piece_type]

        return pts
