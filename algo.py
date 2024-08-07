import chess
b=chess.Board()


def convertBoardToList(b):
    board=[[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    c=0
    for x in b.__str__():
        if not x.isspace():
            board[c//8][c-8*(c//8)]=" " if x=="." else x
            c+=1
    return board

def evaluate(board,white):
    scores={"p":100,"n":300,"b":300,"r":500,"q":900,"k":10**12}
    evaluation=0
    b=convertBoardToList(board)
    for i in b:
        for j in i:
            if not j.isspace():
                evaluation+=(scores[j.lower()]*(1 if j.isupper() else -1))
    return evaluation*(1 if white else -1)
    

def minmax(depth,white,board):
    if depth==0 or len(list(board.legal_moves))==0:
        return evaluate(board,white), None
    
    if white:
        maxEval=float('-inf')
        best_move=None
        for move in board.legal_moves:
            b=board.copy()
            b.push(move)
            evaluation=minmax(depth-1,not white,b)[0]
            maxEval=max(maxEval,evaluation)
            if maxEval==evaluation:
                best_move=move
        return maxEval,best_move
    else:
        minEval=float('inf')
        best_move=None
        for move in board.legal_moves:
            b=board.copy()
            b.push(move)
            evaluation=minmax(depth-1,not white,b)[0]
            minEval=min(minEval,evaluation)
            if minEval==evaluation:
                best_move=move
        return minEval,best_move
