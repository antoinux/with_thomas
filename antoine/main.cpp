#include <bits/stdc++.h>

using namespace std;

long long _();
int main() { _(); return 0; }
#define main _
#define int long long 

int N, M, V, n, B, T;

const int N_MAX = 10000;
const int V_MAX = 1000;

struct Ride
{
    int id;
    int a, b;
    int x, y;
    int t1, t2;
    
    Ride()
    {
        a = b = x = y = t1 = t2 = 0;
    }
    
    bool operator < (const Ride& ride) const
    {
        return t1 < ride.t1;
    }
};

Ride t[N_MAX];
vector<int> r[V_MAX];
int curTime[V_MAX];

int dist(int a, int b, int x, int y)
{
    return abs(a-x) + abs(b-y);
}

int dist(Ride& a, Ride& b)
{
    return abs(a.x-b.a) + abs(a.y-b.b);
}

int main()
{
    ios_base::sync_with_stdio(false);
    cin >> N >> M >> V >> n >> B >> T;
    for(int i=0; i<n; i++)
    {
        t[i].id = i;
        cin >> t[i].a >> t[i].b >> t[i].x >> t[i].y >> t[i].t1 >> t[i].t2;
    }
    sort(t, t+n);
    //faire gaffe aux tests une solution pour chaque peut être intéressant
    int score = 0;
    for(int i=0; i<n; i++)
    {
        Ride& newRide = t[i];
        //celui qui arrive le plus tard et qui a un bonus
        int bestJ = -1, bestArrival, nextBestArrival, bonus = 0;
        for(int j=0; j<V; j++)
        {
            Ride curRide;
            if(r[j].empty())
                curRide = Ride();
            else
                curRide = t[r[j].back()];
            int arrivalTime = curTime[j] + dist(curRide, newRide);
            int realArrivalTime = max(arrivalTime, newRide.t1);
            int nextArrivalTime = realArrivalTime + dist(newRide.a, newRide.b, newRide.x, newRide.y);    
            if(nextArrivalTime <= newRide.t2)
            {
                //cout << arrivalTime << " " << newRide.t1 << "," << newRide.t2 << endl;
                //si il y a bonus, je veux arriver le plus tard possible, mais avoir un bonus
                //s'il y a pas bonus, je veux arriver le plus tôt
                bool noSolution = bestJ == -1;
                bool wasBonus = bestArrival <= newRide.t1;
                bool bonusNow = arrivalTime <= newRide.t1;
                bool arriveBefore = arrivalTime <= bestArrival;
                if(noSolution
                || !wasBonus && arriveBefore
                || wasBonus && bonusNow && !arriveBefore)
                {
                    bestJ = j;
                    bestArrival = arrivalTime;
                    nextBestArrival = nextArrivalTime;
                }
            }
        }
        if(bestJ != -1)
        {
            r[bestJ].push_back(i);
            curTime[bestJ] = nextBestArrival;
            
            score += dist(newRide.a, newRide.b, newRide.x, newRide.y);
            if(bestArrival <= newRide.t1)
                score += B;
        }
    }
    bool debug = 0;
    if(debug)
        cout << score << endl;
    else
        for(int i=0; i<V; i++)
        {
            cout << r[i].size() << " ";
            for(int j : r[i])
                cout << t[j].id << " ";
            cout << endl;
        }
    return 0;
}