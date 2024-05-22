import numpy as np

def count_score(tmp,player1_score,player2_score,player):
    score=[player1_score,player2_score]
    num=tmp.count(str(player))
    if str(3-player) not in tmp:
        if num==4:
            score[player-1]=np.inf
        elif num==3:
            score[player-1]+=2
        else:
            score[player-1]+=1
    else:
        if num==1:
            if tmp.count(str(3-player))==3:
                score[2-player]-=4
            else:
                score[2-player]-=tmp.count(str(3-player))
   
    return score[0],score[1]

def compute_score(gameboard, pos, player1_score, player2_score, player):
    lower_bound_x=max(0,pos[0]-3)
    upper_bound_x=min(3,pos[0])+1
    lower_bound_y=max(0,pos[1]-3)
    upper_bound_y=min(2,pos[1])+1
    for i in range(lower_bound_x,upper_bound_x):
        tmp=[gameboard[i*6+pos[1]],gameboard[(i+1)*6+pos[1]],gameboard[(i+2)*6+pos[1]],gameboard[(i+3)*6+pos[1]]]
        player1_score,player2_score=count_score(tmp,player1_score,player2_score,player)
        if player1_score==np.inf or player2_score==np.inf:
            return player1_score,player2_score
        
    for j in range(lower_bound_y,upper_bound_y):
        tmp=[gameboard[pos[0]*6+j],gameboard[pos[0]*6+j+1],gameboard[pos[0]*6+j+2],gameboard[pos[0]*6+j+3]]
        player1_score,player2_score=count_score(tmp,player1_score,player2_score,player)
        if player1_score==np.inf or player2_score==np.inf:
            return player1_score,player2_score 

    for i,j in zip(range(max(max(0,pos[0]-pos[1]),pos[0]-3),upper_bound_x), range(max(max(0,pos[1]-pos[0]),pos[1]-3),upper_bound_y)):
        tmp=[gameboard[i*6+j],gameboard[(i+1)*6+j+1],gameboard[(i+2)*6+j+2],gameboard[(i+3)*6+j+3]]
        player1_score,player2_score=count_score(tmp,player1_score,player2_score,player)
        if player1_score==np.inf or player2_score==np.inf:
            return player1_score,player2_score 

    for i,j in zip(range(max(max(0,pos[0]+pos[1]-5),pos[0]-3),min(pos[0]+pos[1],upper_bound_x)), range(min(pos[0]+pos[1],min(5,pos[1]+3)),max(max(0,pos[0]+pos[1]-6),pos[1]-3)+2,-1)):
        tmp=[gameboard[i*6+j],gameboard[(i+1)*6+j-1],gameboard[(i+2)*6+j-2],gameboard[(i+3)*6+j-3]]
        player1_score,player2_score=count_score(tmp,player1_score,player2_score,player)
        if player1_score==np.inf or player2_score==np.inf:
            return player1_score,player2_score
        
    return player1_score,player2_score

def possible_move(gameboard):
    moves=[]

    for i in range(7):
        j=gameboard[i*6:i*6+6].find('0')
        moves.append((i,j))
        
    return moves

def place_piece(gameboard, pos, player):
    x,y=pos
    gameboard=list(gameboard)
    gameboard[x*6+y]=str(player)
    gameboard=''.join(gameboard)
    return gameboard

def evaluate(gameboard, player, depth, player1_score, player2_score, col):
    if depth==0:
        if player==1:
            return player2_score-player1_score, col 
        return player1_score-player2_score, col
    moves=possible_move(gameboard)
    score_list=[]
    for move in moves:
        if move[1]==-1:
            score_list.append((0.1,None))
            continue
        tmp=place_piece(gameboard, move, player)
        tmp1,tmp2=compute_score(tmp, move, player1_score, player2_score, player)
        if tmp1 == np.inf or tmp2 == np.inf:
            score_list.append((np.inf,None))
            continue
        score_list.append(evaluate(tmp, 3-player, depth-1, tmp1, tmp2, move[0]))
    tmp=sorted(score_list, key=lambda tup: tup[0], reverse=True)
    score=None
    for i in tmp:
        if i[0]==0.1:
            continue
        score=i
        break
    if not score:
        return 0, 0
    if depth==6:
        print(score_list)
    col=score_list.index(score)
    return -score[0], col
    
    
        
