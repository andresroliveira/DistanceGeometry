#include <bits/stdc++.h>
#define ii pair<int, int>

using namespace std;

vector<int> sym(vector<ii> prune_edges, int n, int K){
    int *b = (int*)malloc((n+1)*sizeof(int));
    for(int i=1;i<=n;i++) b[i] = 1;

    for(int i=0;i<prune_edges.size();i++){
        int u = prune_edges[i].first;
        int v = prune_edges[i].second;

        for(int j=u+K+1;j<=v;j++){
            b[j] = 0;
        }
    }

    vector<int> S;

    for(int i=K+1;i<=n;i++){
        if(b[i] == 1){
            S.push_back(i);
        }
    }

    return S;
}

int main(){
    // n vertices
    // m edges
    // K dim
    int n, m, K; scanf("%d %d %d", &n, &m, &K);

    vector< ii > prune_edges;

    for(int i=0;i<m;i++){
        // edge (a,b) 
        int a, b; scanf("%d %d", &a, &b);

        // if (a,b) is a prune edge
        if(a + K < b){
            ii e = make_pair(a, b);
            prune_edges.push_back(e);
        }
    }

    vector<int> s = sym(prune_edges, n, K);
    for(int i=0;i<s.size();i++){
        printf("%d\n", s[i]);
    }

    return 0;
}
