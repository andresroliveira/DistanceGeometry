#include <bits/stdc++.h>
#define ii pair<int, int>

using namespace std;

vector<int> sym(vector<ii> prune_edges, int n, int K){
    int *w = (int*)calloc(n+1, sizeof(int));

    if(w == NULL){
        exit(0);
    }

    for(int i=0;i<prune_edges.size();i++){
        int u = prune_edges[i].first;
        int v = prune_edges[i].second;

        w[u] = max(w[u], v);
    }

    vector<ii> eps;

    for(int i=1;i<=n;i++){
        if(w[i] != 0){
            eps.push_back(make_pair(i, w[i]));
        }
    }

    free(w);

    int u_bar = eps[0].first;
    int v_bar = eps[0].second;
    vector< ii > S_bar;

    for(int i=1;i<eps.size();i++){
        int u_i = eps[i].first;
        int v_i = eps[i].second;

        if(v_bar >= u_i + K){
            v_bar = max(v_bar, v_i);
        }
        else{
            S_bar.push_back(make_pair(u_bar+K+1, v_bar));
            u_bar = u_i;
            v_bar = v_i;
        }
    }
    S_bar.push_back(make_pair(u_bar+K+1, v_bar));

    vector<int> S;
    S.push_back(K+1);

    for(int v=5,i=0;v<=n;v++){
        int u_bar = S_bar[i].first;
        int v_bar = S_bar[i].second;

        // if v \not\in [u_bar, v_bar]_i
        if(!(u_bar <= v && v <= v_bar)){
            S.push_back(v);
        }

        if(v == v_bar && i < S_bar.size() - 1){
            i++;
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
