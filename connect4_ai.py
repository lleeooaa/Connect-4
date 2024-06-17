import numpy as np

def count_score(tmp,player1_score,player2_score,player,round):
    score=[player1_score,player2_score]
    num=tmp.count(str(player))
    if str(3-player) not in tmp:
        if num==4:
            score[player-1]=np.inf
        elif num==3:
            score[player-1]+=8
        elif num==2:
            score[player-1]+=2
    else:
        if num==1:
            if tmp.count(str(3-player))==3:
                score[2-player]-=10
            elif tmp.count(str(3-player))==2:
                score[2-player]-=2
   
    return score[0],score[1]

def compute_score(gameboard, pos, player1_score, player2_score, player, round):
    lower_bound_x=max(0,pos[0]-3)
    upper_bound_x=min(3,pos[0])+1
    lower_bound_y=max(0,pos[1]-3)
    upper_bound_y=min(2,pos[1])+1
    for i in range(lower_bound_x,upper_bound_x):
        tmp=[gameboard[i*6+pos[1]],gameboard[(i+1)*6+pos[1]],gameboard[(i+2)*6+pos[1]],gameboard[(i+3)*6+pos[1]]]
        player1_score,player2_score=count_score(tmp,player1_score,player2_score,player,round)
        if player1_score==np.inf or player2_score==np.inf:
            return player1_score,player2_score
        
    for j in range(lower_bound_y,upper_bound_y):
        tmp=[gameboard[pos[0]*6+j],gameboard[pos[0]*6+j+1],gameboard[pos[0]*6+j+2],gameboard[pos[0]*6+j+3]]
        player1_score,player2_score=count_score(tmp,player1_score,player2_score,player,round)
        if player1_score==np.inf or player2_score==np.inf:
            return player1_score,player2_score 

    for i,j in zip(range(max(max(0,pos[0]-pos[1]),pos[0]-3),upper_bound_x), range(max(max(0,pos[1]-pos[0]),pos[1]-3),upper_bound_y)):
        tmp=[gameboard[i*6+j],gameboard[(i+1)*6+j+1],gameboard[(i+2)*6+j+2],gameboard[(i+3)*6+j+3]]
        player1_score,player2_score=count_score(tmp,player1_score,player2_score,player,round)
        if player1_score==np.inf or player2_score==np.inf:
            return player1_score,player2_score 

    for i,j in zip(range(max(max(0,pos[0]+pos[1]-5),pos[0]-3),min(pos[0]+pos[1],upper_bound_x)), range(min(pos[0]+pos[1],min(5,pos[1]+3)),max(max(0,pos[0]+pos[1]-6),pos[1]-3)+2,-1)):
        tmp=[gameboard[i*6+j],gameboard[(i+1)*6+j-1],gameboard[(i+2)*6+j-2],gameboard[(i+3)*6+j-3]]
        player1_score,player2_score=count_score(tmp,player1_score,player2_score,player,round)
        if player1_score==np.inf or player2_score==np.inf:
            return player1_score,player2_score
    
    if pos[1]%2==round%2:  #position weight
        if player==1:
            player1_score+=1
        else:
            player2_score+=1
    return player1_score,player2_score

def possible_move(gameboard):
    moves=[]

    for i in range(7):
        j=gameboard[i*6:i*6+6].find('0')
        if j==-1:
            continue
        moves.append((i,j))
        
    return moves

def place_piece(gameboard, pos, player):
    x,y=pos
    gameboard=list(gameboard)
    gameboard[x*6+y]=str(player)
    gameboard=''.join(gameboard)
    return gameboard

def evaluate(gameboard, player, depth, player1_score, player2_score, alpha, beta, col, round):
    if depth==0:
        return player1_score-player2_score, col
    moves=possible_move(gameboard)
    if player==1:
        max_val=(-np.inf,col)
        for move in moves:
            tmp=place_piece(gameboard, move, player)
            tmp1,tmp2=compute_score(tmp, move, player1_score, player2_score, player, round)
            if tmp1 == np.inf:
                return np.inf,col
            eval=evaluate(tmp, 3-player, depth-1, tmp1, tmp2, alpha, beta, col, round+1)
            if eval[0]>max_val[0]:
                max_val=eval
            if eval[0]>alpha[0]:
                alpha=eval
            if beta[0]<=alpha[0]:
                break
        return max_val

    else:
        min_val=(np.inf,col)
        for move in moves:
            tmp=place_piece(gameboard, move, player)
            tmp1,tmp2=compute_score(tmp, move, player1_score, player2_score, player, round)
            if tmp2 == np.inf:
                return -np.inf,col
            eval=evaluate(tmp, 3-player, depth-1, tmp1, tmp2, alpha, beta, col, round+1)
            if eval[0]<min_val[0]:
                min_val=eval
            if eval[0]<beta[0]:
                beta=eval
            if beta[0]<=alpha[0]:
                break
        return min_val

def evaluate_entry(gameboard, player, depth, player1_score, player2_score, round):
    moves=possible_move(gameboard)
    score_list=[]
    for move in moves:
        tmp=place_piece(gameboard, move, player)
        tmp1,tmp2=compute_score(tmp, move, player1_score, player2_score, player, round)
        if tmp1 == np.inf:
            score_list.append((np.inf,move[0]))
            continue
        score_list.append(evaluate(tmp, 3-player, depth-1, tmp1, tmp2, (-np.inf,move[0]), (np.inf,move[0]), move[0], round+1))
    print(score_list)
    tmp=sorted(score_list, key=lambda tup: tup[0], reverse=True)
    score=tmp[0]
    return score[0], score[1]
