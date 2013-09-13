#include <iostream>
#include <map>
#include <vector>
#include <set>
#include <queue>

#include <math.h>

using namespace std;

// The empty square
#define EMPTY 0

// Number of squares in the puzzle
#define SIZE 9

// Various debug output flags
//#define SUCC_DEBUG
//#define GOAL_DEBUG
//#define IDS_DEBUG
//#define ASTAR_DEBUG
//#define MAN_DEBUG
//#define EUC_DEBUG

class PuzzEqual : public less<int*>
{
    public:
    bool operator()(const int *p1, const int *p2)
    {
        for(int i=0; i<SIZE; i++) {
            if(p1[i] != p2[i])
                return p1[i] < p2[i];
        }

        return false;
    }
};

struct Stats
{
    Stats()
    {
        statesVisited = 0;
        statesExpanded = 0;
        solutionLength = -1;
        maxDepth = 0;
        maxFringe = 0;
    }

    int statesVisited;
    int statesExpanded;
    int solutionLength;
    int maxDepth;
    int maxFringe;
};

// first argument of pair is depth
typedef multimap<double, pair<int, int*> > PuzzQueue;
typedef set<int*, PuzzEqual> PuzzSet;

void printPuzzle(int *puzzle)
{
    for(int i=0; i<SIZE; i++) {
        if(i == 0) cout << "[";
        cout << puzzle[i];
        if(i != SIZE-1) cout << " ";
        else cout << "]";
    }
}

void printStats(Stats &stats)
{
    cout << stats.statesVisited << " " << stats.statesExpanded << " " 
         << stats.solutionLength << " " << stats.maxDepth << " " 
         << stats.maxFringe << endl;
}

vector<int*> successor(int *puzzle)
{
    vector<int*> nextStates;

    // There are up to 4 moves we can make into the blank square
    int emptyloc = 0;
    for(int i=0; i<SIZE; i++) {
        if(puzzle[i] == 0) {
            emptyloc = i;
            break;
        }
    }

    #ifdef SUCC_DEBUG
    cout << "succ: orig: ";
    printPuzzle(puzzle);
    cout << endl;
    #endif

    // If the empty isn't at the top swap with square above
    if(emptyloc > 3) {
        int *newpuzzle = new int[SIZE];
        memcpy(newpuzzle, puzzle, SIZE * sizeof(int));
        newpuzzle[emptyloc] = puzzle[emptyloc-3];
        newpuzzle[emptyloc-3] = EMPTY;
        nextStates.push_back(newpuzzle);
        #ifdef SUCC_DEBUG
        cout << "      next: ";
        printPuzzle(newpuzzle);
        cout << endl;
        #endif
    }

    // If the empty isn't at the bottom swap with square below
    if(emptyloc < 6) {
        int *newpuzzle = new int[SIZE];
        memcpy(newpuzzle, puzzle, SIZE * sizeof(int));
        newpuzzle[emptyloc] = puzzle[emptyloc+3];
        newpuzzle[emptyloc+3] = EMPTY;
        nextStates.push_back(newpuzzle);
        #ifdef SUCC_DEBUG
        cout << "      next: ";
        printPuzzle(newpuzzle);
        cout << endl;
        #endif
    }

    // If the empty isn't at the left side swap with the left square
    if(emptyloc % 3 != 0) {
        int *newpuzzle = new int[SIZE];
        memcpy(newpuzzle, puzzle, SIZE * sizeof(int));
        newpuzzle[emptyloc] = puzzle[emptyloc-1];
        newpuzzle[emptyloc-1] = EMPTY;
        nextStates.push_back(newpuzzle);
        #ifdef SUCC_DEBUG
        cout << "      next: ";
        printPuzzle(newpuzzle);
        cout << endl;
        #endif
    }

    // If the empty isn't at the right side swap with the right square
    if((emptyloc+1) % 3 != 0) {
        int *newpuzzle = new int[SIZE];
        memcpy(newpuzzle, puzzle, SIZE * sizeof(int));
        newpuzzle[emptyloc] = puzzle[emptyloc+1];
        newpuzzle[emptyloc+1] = EMPTY;
        nextStates.push_back(newpuzzle);
        #ifdef SUCC_DEBUG
        cout << "      next: ";
        printPuzzle(newpuzzle);
        cout << endl;
        #endif
    }

    return nextStates;
}

bool isGoal(int *puzzle, int *goal)
{
    bool goalState = true;
    for(int i=0; i<SIZE; i++) {
        if(puzzle[i] != goal[i]) {
            goalState = false;
            break;
        }
    }

    #ifdef GOAL_DEBUG
    cout << "goal: inpt: ";
    printPuzzle(puzzle);
    cout << endl;
    cout << "      goal: ";
    printPuzzle(goal);
    cout << endl;
    cout << "      bool: " << goalState << endl;
    #endif
    return goalState;
}

// Depth limited search
// If limit < 0 then no limit
bool dls(Stats &stats, int limit, int *puzzle, int *goal)
{
    queue<pair<int, int*> > queue;
    queue.push(pair<int,int*>(0, puzzle));

    bool foundGoal = false;
    while(!queue.empty() && !foundGoal) {
        int *puzz = queue.front().second;
        int depth = queue.front().first;
        queue.pop();

        stats.statesVisited++;
        stats.maxDepth = max(depth, stats.maxDepth);
        foundGoal = isGoal(puzz, goal);
        
        if(foundGoal) {
            stats.solutionLength = depth;
        } else if(depth<limit) {
            // Don't expand past the limit
            vector<int*> nextStates = successor(puzz);
            stats.statesExpanded += nextStates.size();
            for(size_t i=0; i<nextStates.size(); i++)
                queue.push(pair<int, int*>(depth+1, nextStates[i]));
        }
        
        if(puzz != puzzle)
            delete puzz;
        stats.maxFringe = max((int)queue.size(), stats.maxFringe);
    }

    // delete the rest of the queue
    while(!queue.empty()) {
        int *tmp = queue.front().second;
        if(tmp != puzzle)
            delete tmp;
        queue.pop();
    }

    return foundGoal;
}

// Iterative deepening search
bool ids(Stats &stats, int *puzzle, int *goal)
{
    int maxDepth = 0;
    while(true) {
        #ifdef IDS_DEBUG
        cout << " ids: mxdp: " << maxDepth << endl;
        #endif

        if(dls(stats, maxDepth, puzzle, goal))
            return true;
        maxDepth++;
    }
}

bool aStar(Stats &stats, int *puzzle, int *goal, double (*compf)(int*, int*))
{
    PuzzQueue queue;
    PuzzSet seen;

    queue.insert(pair<double, pair<int, int*> >(compf(puzzle, goal), 
                                                pair<int, int*>(0, puzzle)));
    bool foundGoal = false;
    while(!queue.empty() && !foundGoal) {
        PuzzQueue::iterator tmp = queue.begin();
        int depth = tmp->second.first;
        int *puzz = tmp->second.second;
        seen.insert(puzz);
        queue.erase(tmp);

        stats.statesVisited++;
        stats.maxDepth = max(depth, stats.maxDepth);

        foundGoal = isGoal(puzz, goal);

        #ifdef ASTAR_DEBUG
        cout << "astr: puzz: ";
        printPuzzle(puzz);
        cout << endl;
        cout << "      goal: ";
        printPuzzle(goal);
        cout << endl;
        cout << "      depth: " << depth << endl;
        cout << "      cost: " << tmp->first << endl;
        cout << "      done: " << foundGoal << endl;
        #endif


        if(foundGoal) {
            stats.solutionLength = depth;
        } else {
            // If we're not at the goal expand the node
            vector<int*> nextStates = successor(puzz);
            stats.statesExpanded += nextStates.size();
            for(size_t i=0; i<nextStates.size(); i++) {
                // Only insert states we haven't seen before
                if(seen.find(nextStates[i]) == seen.end()) {
                    pair<int, int*> pr(depth+1, nextStates[i]);
                    double cost = compf(nextStates[i], goal);
                    queue.insert(pair<double, pair<int, int*> >(cost, pr));
                } else {
                    delete nextStates[i];
                }
            }
        }

        stats.maxFringe = max((int)queue.size(), stats.maxFringe);
    }

    // Delete all the extra states
    for(PuzzSet::iterator itr=seen.begin(); itr!=seen.end(); ++itr) {
        if(*itr != puzzle)
            delete *itr;
    }
    for(PuzzQueue::iterator itr=queue.begin(); itr!=queue.end(); ++itr) {
        if(itr->second.second != puzzle)
            delete itr->second.second;
    }

    return foundGoal;
}

// Base cost for all moves is 1
int baseCost(int *puzzle, int *goal)
{
    return 1;
}

// Returns index of a number in a puzzle
int index(int *puzzle, int num)
{
    for(int i=0; i<SIZE; i++) {
        if(puzzle[i] == num)
            return i;
    }
    return -1;
}

// Manhattan distance
double manhattanDistCost(int *puzzle, int *goal) 
{
    double totalDist = 0;
    // Sum up all the offsets from the goal
    // Don't count the zero
    for(int i=0; i<SIZE; i++) {
        if(puzzle[i] != EMPTY) {
            int goali = index(goal, puzzle[i]);
            int dx = abs((int) floor(i / 3) - (int) floor(goali / 3));
            int dy = abs(i % 3 - goali % 3);
            totalDist += dx + dy;
        }
    }

    #ifdef MAN_DEBUG
    cout << "mand: puzz: ";
    printPuzzle(puzzle);
    cout << endl;
    cout << "      goal: ";
    printPuzzle(goal);
    cout << endl;
    cout << "      dist: " << totalDist << endl;
    #endif
    return totalDist;
}

double euclideanDistCost(int *puzzle, int *goal)
{
    double totalDist = 0;
    for(int i=0; i<SIZE; i++) {
        int goali = index(goal, puzzle[i]);
        int px = i % 3;
        int py = (int) floor(i / 3);
        int gx = goali % 3;
        int gy = (int) floor(goali / 3);

        double dx = px - gx;
        double dy = py - gy;

        totalDist += sqrt(dx*dx + dy*dy);
    }

    #ifdef EUC_DEBUG
    cout << "eucd: puzz: ";
    printPuzzle(puzzle);
    cout << endl;
    cout << "      goal: ";
    printPuzzle(goal);
    cout << endl;
    cout << "      dist: " << totalDist << endl;
    #endif
    return totalDist;
}

int main(int argc, char *argv[])
{
    if(argc != 3) {
        cerr << "puzzle <solver> <puzzle>" << endl;
        cerr << "<solver> can be:" << endl;
        cerr << "    i -> ids" << endl;
        cerr << "    m -> A* with manhattan distance" << endl;
        cerr << "    e -> A* with euclidean distance" << endl;
        cerr << "<puzzle> must be in 123456780 format" << endl;
        exit(1);
    }

    char solvetype = *argv[1];

    int puzzle[SIZE];

    for(int i=0; i<SIZE; i++) {
        char tmp[2] = {argv[2][i], '\0'};
        puzzle[i] = atoi(tmp);
    }

    Stats stats;
    int goal[] = {1,2,3,4,5,6,7,8,0};

    switch(solvetype) {
        case 'i': 
            ids(stats, puzzle, goal); 
            break;
        case 'm': 
            aStar(stats, puzzle, goal, manhattanDistCost); 
            break;
        case 'e': 
            aStar(stats, puzzle, goal, euclideanDistCost); 
            break;
        default:
            cerr << "invalid solver type" << endl;
            exit(1);
    }

    printStats(stats);

    return 0;
}

