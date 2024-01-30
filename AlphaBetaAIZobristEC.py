# Andy Xu
# Date: 10/3/23

import chess
import math
import random

class AlphaBetaAIZobristEC():
    def __init__(self, depth):
        self.depth = depth # maximum depth
        self.num_nodes = 0 # number of nodes
        self.zobrist_table = {} # zobrist table
        self.init_zobrist() # initialize zobrist table
        self.trans_table = {} # transposition table

    def choose_move(self, board):
        value, move = self.max_value(board, 0, -math.inf, math.inf)
        print(self.num_nodes)
        print("AlphaBeta AI recommending move " + str(move))
        return move

    # Max Value function as described by textbook
    def max_value(self, board, cur_depth, alpha, beta):
        cur_depth += 1
        self.num_nodes += 1

        # check for terminal state
        if self.cutoff_test(board, cur_depth):
            if board.is_checkmate():
                return -math.inf, board.peek()
            return self.utility(board), board.peek()

        # get possible moves
        moves = list(board.legal_moves)
        moves = sorted(moves, key = lambda m: self.move_sort(board, m))

        # iterate through possible moves to find best possible move
        v = -math.inf
        best = None
        for m in moves:
            board.push(m)
            min_v, min_m = self.min_value(board, cur_depth, alpha, beta)

            if min_v > v:
                best = m
                v = min_v

            board.pop()

            if min_v >= beta:
                return v, min_m

            alpha = max(alpha, v)

        return v, best

    # Min Value function as described by textbook
    def min_value(self, board, cur_depth, alpha, beta):
        cur_depth += 1
        self.num_nodes += 1

        # check for terminal state
        if self.cutoff_test(board, cur_depth):
            if board.is_checkmate():
                return math.inf, board.peek()
            return self.utility(board), board.peek()

        # get possible moves
        moves = list(board.legal_moves)
        moves = sorted(moves, key = lambda m: self.move_sort(board, m))

        # iterate through possible moves to get best possible move
        v = math.inf
        best = None
        for m in moves:
            board.push(m)
            max_v, max_m = self.max_value(board, cur_depth, alpha, beta)
            if max_v < v:
                best = m
                v = max_v

            board.pop()

            if v <= alpha:
                return v, best

            beta = min(beta, v)

        return v, best

    # cutoff test for depth limited minimax search, returns True if terminal state
    # has been reached (win or draw) or if we have reached specified maximum depth
    def cutoff_test(self, board, cur_depth):
        return board.is_game_over() or cur_depth > self.depth

    #heuristic function used for move ordering, returns utility value for given move
    def move_sort(self, board, move):
        board.push(move)
        pts = self.utility(board)
        board.pop()
        return pts

    # function to calculate utility of terminal state
    def utility(self, board):
        #check if state is already in transposition table
        if self.zobrist_hash(board) in self.trans_table.keys():
            return self.trans_table[self.zobrist_hash(board)]

        piece_pts = {
            1: 1, #Pawn
            2: 3, #Knight
            3: 3, #Bishop
            4: 5, #Rook
            5: 9, #Queen
            6: 0  #King
        }
        pts = 0
        pieces = board.piece_map()
        for piece in pieces.values():
            if piece.color:
                pts -= piece_pts[piece.piece_type]
            else:
                pts += piece_pts[piece.piece_type]

        #add state to transposition table
        self.trans_table[self.zobrist_hash(board)] = pts

        return pts

    # function to intialize zobrist table
    def init_zobrist(self):
        #generates random bitstring for all possible combinations of squares, pieces, and colors
        #and stores values in zobrist_table
        for s in chess.SQUARES:
            for p in chess.PIECE_TYPES:
                for c in chess.COLORS:
                    key = (s, p, c)
                    self.zobrist_table[key] = random.getrandbits(64)

    # function to get appropriate zobrist hash using zobrist table given a current state of the board
    def zobrist_hash(self, board):
        hash_key = 0
        #iterates through squares on board
        for s in chess.SQUARES:
            p = board.piece_at(s)
            if p: #if there is a piece
                #get color and type of piece
                color = p.color
                piece_type = p.piece_type

                #get appropriate key to get corresponding value from zobrist table
                key = (s, piece_type, color)

                #XOR with parent hash
                hash_key ^= self.zobrist_table[key]

        return hash_key


