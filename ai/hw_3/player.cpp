#include <stdio.h>
#include <iostream>
#include <vector>
#include <set>
#include <float.h>

//#define DEBUG_SUCC
//#define DEBUG_EVAL

using namespace std;

// Hard coded board file name
#define BOARD_NAME "board.txt"

enum Piece {None, X, O};

// Which player I am
#ifndef ME
#define ME X
#endif

#define MAXNODES 5000

// Class to track how many nodes we've generated
class SerialNumber
{
public:
    SerialNumber(int maxNum) {
        myMax = maxNum; 
        myNum = 1;
    }

    bool atMax() {return myNum > myMax;}
    void inc() {
        myNum++;
    }

protected:
    int myNum;
    int myMax;
};

class Board 
{
public:
    Board(int xd, int yd, int nw) {
        xDim = xd;
        yDim = yd;
        numWin = nw;
        gameBoard = new Piece*[xd];
        for(int i=0; i<xd; i++)
            gameBoard[i] = new Piece[yd];
    }

    Board(Board &b) {
        xDim = b.xDim;
        yDim = b.yDim;
        numWin = b.numWin;
        gameBoard = new Piece*[xDim];
        for(int i=0; i<xDim; i++) {
            gameBoard[i] = new Piece[yDim];
            for(int j=0; j<yDim; j++) 
                gameBoard[i][j] = b.gameBoard[i][j];
        }
    }

    ~Board() {
        delete gameBoard;
    }

    Piece get(int x, int y) {
        return gameBoard[x][y];
    }

    void set(int x, int y, Piece p) {
        gameBoard[x][y] = p;
    }

    bool isWinning(Piece player) {
        std::set<Piece> p;
        p.insert(player);
        return numPossibles(p) > 0;
    }

    // Returns the number of possible winnings 
    // (n in a row consisting of the set of pieces)
    int numPossibles(std::set<Piece> &pieces) {
        int total = 0;
        for(int x=0; x<xDim; x++) {
            for(int y=0; y<yDim; y++) {
                if(inSet(gameBoard[x][y],pieces)) {
                    // Assume left and up combinations would 
                    // have been found earlier
                    // right
                    if(x+numWin <= xDim) {
                        bool win = true;
                        for(int i=1; i<numWin; i++)
                            win = win && inSet(gameBoard[x+i][y],pieces);
                        if(win) total++;
                    }
                    // down
                    if(y+numWin <= yDim) {
                        bool win = true;
                        for(int i=1; i<numWin; i++)
                            win = win && inSet(gameBoard[x][y+i],pieces);
                        if(win) total++;
                    }
                    // down right
                    if(x+numWin <= xDim && y+numWin <= yDim) {
                        bool win = true;
                        for(int i=1; i<numWin; i++)
                            win = win && inSet(gameBoard[x+i][y+i],pieces);
                        if(win) total++;
                    }
                    // down left
                    if(x-numWin+1 >= 0 && y+numWin <= yDim) {
                        bool win = true;
                        for(int i=1; i<numWin; i++)
                            win = win && inSet(gameBoard[x-i][y+i],pieces);
                        if(win) total++;
                    }
                }
            }
        }

        return total;
    }

    int xdim() {return xDim;}
    int ydim() {return yDim;}

protected:
    bool inSet(Piece p, std::set<Piece> &pieces) {
        return pieces.find(p) != pieces.end();
    }
    Piece **gameBoard;
    int xDim;
    int yDim;
    int numWin;
};

void printBoard(Board *b)
{
    for(int y=0; y<b->ydim(); y++) {
        for(int x=0; x<b->xdim(); x++) {
            switch(b->get(x,y)) {
                case X:
                    cout << 'X';
                    break;
                case O:
                    cout << 'O';
                    break;
                case None:
                    cout << '_';
                    break;
            }
        }
        cout << endl;
    }
}


vector<Board*> successor(Board *b, Piece player)
{
    vector<Board*> boards;

    for(int x=0; x<b->xdim(); x++) {
        for(int y=0; y<b->ydim(); y++) {
            if(b->get(x,y) == None) {
                Board *nb = new Board(*b);
                nb->set(x,y,player);
                boards.push_back(nb);
            }
        }
    }

    #ifdef DEBUG_SUCC
    cout << "succ: board:" << endl;
    printBoard(b);
    for(size_t i=0; i<boards.size(); i++) {
        cout << "      succ:" << endl;
        printBoard(boards[i]);
    }
    #endif

    return boards;
}

double eval(Board *b)
{
    Piece notMe;
    if(ME == X) notMe = O;
    else notMe = X;

    double maxScore = b->xdim() * b->ydim();
    double score = 0;
    if(b->isWinning(ME))
        score = maxScore;
    else if(b->isWinning(notMe))
        score = -maxScore;
    else {
        std::set<Piece> os;
        std::set<Piece> xs;
        os.insert(O);
        os.insert(None);
        xs.insert(X);
        xs.insert(None);
        int oMatches = b->numPossibles(os);
        int xMatches = b->numPossibles(xs);
        if(ME == X)
            score = xMatches - oMatches;
        else
            score = oMatches - xMatches;
    }

    #ifdef DEBUG_EVAL
    cout << "eval: board: " << endl;
    printBoard(b);
    cout << endl;
    cout << "      score: " << score << endl;
    #endif

    return score;
}

pair<Board*,double> minimax(Board *b, Piece player, 
                            double alpha, double beta, SerialNumber *sn)
{
    // Terminal state (stop once someone has won)
    if(b->isWinning(X) || b->isWinning(O))
        return pair<Board*,double>(b, eval(b));

    // See if we've evaluated enough boards
    if(sn->atMax())
        return pair<Board*,double>(b, eval(b));
    
    vector<Board*> succs = successor(b, player);
    // Terminal state (no more legal moves)
    if(succs.size() == 0)
        return pair<Board*,double>(b, eval(b));
    
    Piece nextPlayer;
    if(player == X) {
        // Then we're at MAX step
        nextPlayer = O;
    } else if(player == O) {
        nextPlayer = X;
    }

    Board *bestBoard = NULL;
    // Each node we process will increment the serial number counter
    // We want to stop processing when we reach the maximum count
    for(size_t i=0; i<succs.size() && !sn->atMax(); i++, sn->inc()) {
        pair<Board*,double> temp = minimax(succs[i], nextPlayer, alpha, beta, sn);
        if(player == X && temp.second > alpha) {
            alpha = temp.second;
            bestBoard = succs[i];
        } else if(player == O && temp.second < beta) {
            beta = temp.second;
            bestBoard = succs[i];
        }

        // Check for return condition
        if(player == X && alpha >= beta)
            return pair<Board*,double>(bestBoard,beta);
        else if(player == O && beta <= alpha)
            return pair<Board*,double>(bestBoard,alpha);
    }

    if(player == X)
        return pair<Board*,double>(bestBoard,alpha);
    else
        return pair<Board*,double>(bestBoard,beta);
}

Board* readBoard() {
    int dx, dy, dw;
    cin >> dx >> dy >> dw;
    Board *b = new Board(dx, dy, dw);
    
    FILE *file = fopen(BOARD_NAME, "r");

    for(int y=0; y<dy; y++) {
        for(int x=0; x<dx; x++) {
            char c = fgetc(file);
            switch(c) {
                case 'X':
                    b->set(x, y, X);
                    break;
                case 'O':
                    b->set(x, y, O);
                    break;
                case '_':
                    b->set(x, y, None);
                    break;
                case EOF:
                    cerr << "specified board size is larger than input board"
                         << endl;
                    exit(10);
                    break;
                default:
                    // loop around again
                    x--;
                    break;
            }
        }
    }

    fclose(file);

    return b;
}

void writeBoard(Board *b)
{
    FILE *file = fopen(BOARD_NAME, "w");
    for(int y=0; y<b->ydim(); y++) {
        for(int x=0; x<b->xdim(); x++) {
            switch(b->get(x,y)) {
                case X:
                    fputc('X', file);
                    break;
                case O:
                    fputc('O', file);
                    break;
                case None:
                    fputc('_', file);
                    break;
            }
        }
    }
    
    fclose(file);
}

void printMove(Board *oldBoard, Board *newBoard)
{
    // Print the index of the first square that's different
    int indx = 0;
    for(int y=0; y<oldBoard->ydim(); y++) {
        for(int x=0; x<oldBoard->xdim(); x++) {
            if(oldBoard->get(x,y) != newBoard->get(x,y)) {
                cout << indx << endl;
                return;
            } else {
                indx++;
            }
        }
    }
}

int main(int argc, char **argv)
{
    Board *b = readBoard();
    SerialNumber sn(MAXNODES);
    pair<Board*,double> move = minimax(b, ME, -DBL_MAX, DBL_MAX, &sn);
    Board *nb = move.first;
    //writeBoard(nb);
    printMove(b, nb);
    return 0;
}

