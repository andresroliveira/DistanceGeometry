#include <bits/stdc++.h>

using namespace std;

struct edge{ // edge (u, v), u < v
    int u, v;

    edge(){
        u = v = 0;
    }

    edge(int _u, int _v){
        u = min(_u, _v);
        v = max(_u, _v);
    }
};

vector<int> sym(vector<edge> prune_edges, int n){
    int w[n+1]; memset(w, 0, sizeof w);

    for(int k=0;k<prune_edges.size();k++){
        int u = prune_edges[k].u;
        int v = prune_edges[k].v;

        w[u] = max(w[u], v);
    }

    vector<edge> eps;

    for(int i=1;i<=n;i++){
        if(w[i] != 0){
            eps.push_back(edge(i, w[i]));
        }
    }

    int u_bar = eps[0].u;
    int v_bar = eps[0].v;
    vector<pair<int,int> > S_bar;

    for(int k=1;k<eps.size();k++){
        int u_k = eps[k].u;
        int v_k = eps[k].v;

        if(v_bar >= (u_k + 4)-1){
            v_bar = max(v_bar, v_k);
        }
        else{
            S_bar.push_back(make_pair(u_bar+4, v_bar));
            u_bar = u_k;
            v_bar = v_k;
        }
    }
    S_bar.push_back(make_pair(u_bar+4, v_bar));

    vector<int> S;
    S.push_back(4);

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
    int n, m; scanf("%d %d", &n, &m);

    vector<edge> prune_edges;

    for(int i=0;i<m;i++){
        // edge (a,b) with distance c
        int a, b; double c; scanf("%d %d %lf", &a, &b, &c);

        // if (a,b) is a prune edge
        if(a + 3 < b){
            edge e = edge(a, b);
            prune_edges.push_back(e);
        }
    }

    vector<int> s = sym(prune_edges, n);
    for(int i=0;i<s.size();i++){
        printf("%d\n", s[i]);
    }

    return 0;
}
