import cv2
import numpy as np
import math
from grabscreen import screenshot
from time import sleep
import os
import chess
import pyautogui


def convertBoardToList(b):
    board=[[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    c=0
    for x in b.__str__():
        if not x.isspace():
            board[c//8][c-8*(c//8)]=" " if x=="." else x
            c+=1
    return board

def evaluate(board,white,move):
    endGameKingHeat=[[4, 3, 2, 2, 2, 2, 3, 4],
    [3, 3, 2, 2, 2, 2, 3, 3],
    [2, 2, 1, 1, 1, 1, 2, 2],
    [2, 2, 1, 0, 0, 1, 2, 2],
    [2, 2, 1, 0, 0, 1, 2, 2],
    [2, 2, 1, 1, 1, 1, 2, 2],
    [3, 3, 2, 2, 2, 2, 3, 3],
    [4, 3, 2, 2, 2, 2, 3, 4]]
    scores={"p":100,"n":300,"b":300,"r":500,"q":900,"k":9000}
    evaluation=0
    blacks=0
    whites=0
    blackKing=None
    b=convertBoardToList(board)
    for i in b:
        for j in i:
            if not j.isspace():
                evaluation+=(scores[j.lower()]*(1 if j.isupper() else -1))
            if j=='k':
                blackKing=(b.index(i),i.index(j))
            if j.islower() and j.isspace()==False:
                blacks+=1
            if j.isupper() and j.isspace()==False:
                whites+=1
    #evaluation+=((endGameKingHeat[blackKing[0]][blackKing[1]]*100)*(1/(1+math.e**(-0.3*(move-40)))))*3
    #evaluation+=(200*int(board.is_check()))
    return evaluation
    

def minmax(depth,white,board,m,alpha,beta):
    if depth==0 or len(list(board.legal_moves))==0:
        return evaluate(board,white,m), None
    
    if white:
        maxEval=float('-inf')
        best_move=None
        for move in board.legal_moves:
            b=board.copy()
            b.push(move)
            evaluation=minmax(depth-1,not white,b,m,alpha,beta)[0]
            maxEval=max(maxEval,evaluation)
            if maxEval==evaluation:
                best_move=move
            alpha=max(evaluation,alpha)
        return maxEval,best_move
    else:
        minEval=float('inf')
        best_move=None
        for move in board.legal_moves:
            b=board.copy()
            b.push(move)
            evaluation=minmax(depth-1,not white,b,m,alpha,beta)[0]
            minEval=min(minEval,evaluation)
            if minEval==evaluation:
                best_move=move
            beta=min(evaluation,beta)
        return minEval,best_move


global h
global w
global xxx
global yyy
global cell
standard_board=[['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], 
                ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], 
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
                ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]

black_board=[['r', 'n', 'b', 'k', 'q', 'b', 'n', 'r'], 
                ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], 
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
                ['R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R']]
global WHITE
WHITE=False
global pp
def initGrab():
    global pp
    global xxx
    global yyy
    global cell
    board_img=screenshot()
    #spits out the squares
    board_img_small=cv2.resize(board_img,(int(board_img.shape[1]/2),int(board_img.shape[0]/2))) #resize the image to 1/4th area to make it easy to see on screen
    bw_board=cv2.cvtColor(board_img_small,cv2.COLOR_BGR2GRAY)

    canny=cv2.Canny(bw_board,30,200) #find the edges in the screen
    contours, hierarchy = cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) #find the distinct shapes

    blank=np.zeros((int(board_img.shape[0]/2),int(board_img.shape[1]/2),3),dtype='uint8')
    cv2.drawContours(blank, contours, -1, (0, 255, 0), 3) #draw the distinct shapes on a blank image
    for c in contours:
        M = cv2.moments(c) #moments-> center of a distinct contour.
        if M['m00'] != 0.0 and cv2.contourArea(c)>10**5: #the chess board will have the largest area in the screen hence we can use this filter
            x1 = int(M['m10']/M['m00'])
            y1 = int(M['m01']/M['m00'])
            cv2.putText(blank, f'Area :{cv2.contourArea(c)}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            perimeter=cv2.arcLength(c,True)
            side=perimeter/4
            p2x,p2y=int(x1+side/2), int(y1+side/2) #bottom right point
            p1x,p1y=int(x1-side/2), int(y1-side/2) #top left point
            xxx=p1x
            yyy=p1y
            cell=(p2x-p1x)/8
            cv2.circle(blank, (p1x,p1y), 5, (0,0,255), 10)
            cv2.circle(blank, (p2x,p2y), 5, (0,0,255), 10)
            pp=(p1y*2+10,p2y*2,p1x*2+10,p2x*2)
            chess=board_img[pp[0]:pp[1],pp[2]:pp[3]] #cutout chess board from original image/ multiply by 2 to regain original coordinates
    return chess
initGrab()
def grabBoard():
    global pp
    board_img=screenshot()
    chess=board_img[pp[0]:pp[1],pp[2]:pp[3]] #cutout chess board from original image/ multiply by 2 to regain original coordinates
    return chess


def iterate_pieces(im):
    global h
    global w
    pieces=[]
    height,width=int(im.shape[0]/8),int(im.shape[1]/8)
    h=height
    w=width
    for yy in range(0,im.shape[0],height):
        if im.shape[0]-yy>0.5*height:
            for xx in range(0,im.shape[1],width):
                if im.shape[1]-xx>0.5*width:
                    i=im[yy:yy+height,xx:xx+width]
                    pieces.append(i)
                    cv2.imshow("piece",i)
                    cv2.waitKey(10)
    return pieces
global qq
qq=0         
def mask_piece(i):
    global qq
    global WHITE
    lower=np.array([210]*3)
    upper=np.array([255]*3)
    mask=cv2.inRange(i,lower,upper)
    mask=cv2.resize(mask,(100,100))
    col="white"
    if np.sum(mask==255)<200:
        col="black"
        lower=np.array([40]*3)
        upper=np.array([130]*3)
        mask=cv2.inRange(i,lower,upper)
        mask=cv2.resize(mask,(100,100))
        if qq==0:
            WHITE=True
    qq+=1
    return mask,col


print("INITIALISING")
blacks={}
whites={}
all_pieces=[mask_piece(x)[0] for x in iterate_pieces(grabBoard())]


c=0
if WHITE:
    bboard=standard_board
else:
    bboard=black_board
for i in range(0,len(bboard)):
    for j in range(0,len(bboard[i])):
        if bboard[i][j].islower():
            blacks[bboard[i][j]]=all_pieces[c]
        if bboard[i][j].isupper():
            whites[bboard[i][j]]=all_pieces[c]
        #cv2.imshow("mask",all_pieces[c])
        #cv2.waitKey(1)
        c+=1 

if not WHITE:
    blacks,whites=whites,blacks


def cell2pix(c):
    global xxx
    global yyy
    xxxx,yyyy=xxx*2,yyy*2#223,154
    global cell
    if cell<100:
        cell*=2
    l=[chr(i) for i in range(97,105)]
    y=8-int(c[1])
    x=l.index(c[0])
    xxxx+=(cell*x)
    xxxx+=(cell/2)
    yyyy+=(cell*y)
    yyyy+=(cell/2)
    return (int(xxxx),int(yyyy))


def MOUSE(move):
    p=move[:2]
    q=move[2:]
    pyautogui.click(cell2pix(p))
    sleep(1)
    pyautogui.click(cell2pix(q))

sleep(5)
move=-1
lm=None
last=None
depth=3
while True:
    text_board=[[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    board=grabBoard()
    pi=iterate_pieces(board)
    pi=[mask_piece(x) for x in pi]
    c=0
    if move%80==0 and move!=0:
        depth+=1
    for p in pi:
        if p[1]=="white":
            for key in whites:
                r=cv2.subtract(cv2.bitwise_or(p[0],whites[key]),cv2.bitwise_and(p[0],whites[key]))
                if np.sum(r==255)<300:
                    x_mult,y_mult=c-(8*(c//8)),(c//8)+1
                    text_board[y_mult-1][x_mult]=key
                    cv2.putText(board,f'{key}',(x_mult*w,y_mult*h),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1,cv2.LINE_AA)
        else:
            for key in blacks:
                r=cv2.subtract(cv2.bitwise_or(p[0],blacks[key]),cv2.bitwise_and(p[0],blacks[key]))
                if np.sum(r==255)<300:
                    x_mult,y_mult=c-(8*(c//8)),(c//8)+1
                    text_board[y_mult-1][x_mult]=key
                    cv2.putText(board,f'{key}',(x_mult*w,y_mult*h),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1,cv2.LINE_AA)
        c+=1
        if c==64:
            c=0
    bb=chess.Board()
    bb.clear_board()
    checktable={"p":1,"n":2,"b":3,"r":4,"q":5,"k":6}
    for i in range(0,len(text_board)):
        for j in range(0,len(text_board[i])):
            square2chess=8*(7-i)+j
            if not text_board[i][j].isspace():
                bb.set_piece_at(square2chess,chess.Piece(checktable[text_board[i][j].lower()],text_board[i][j].isupper()))
    if last!=text_board:
        move+=1
    if move%2==0:
        if lm!=move:
            mm=minmax(depth,True,bb,move,float('-inf'),float('inf'))
            MOUSE(mm[1].__str__())
    else:
        pass
    last=text_board
    lm=move


    last=text_board
    cv2.imshow("board",board)
    cv2.setWindowProperty("board", cv2.WND_PROP_TOPMOST, 1)
    cv2.waitKey(100)