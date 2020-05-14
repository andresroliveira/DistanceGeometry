#include <stdio.h>
#include <stdlib.h>

bool *graph;

int main(){
    // n vertices
    // m edges
    int n, m; scanf("%d %d", &n, &m);

    // try alocate matrix
    graph = (bool*)calloc((n+1)*(n+1), sizeof(bool));
    if(graph == NULL) exit(1);

    for(int i=0;i<m;i++){
        // edge (a,b) with distance c
        int a, b; double c; scanf("%d %d %lf", &a, &b, &c);

        // set (a,b) and (b,a) as 1
        graph[a*(n+1) + b] = graph[a + b*(n+1)] = 1;
    }

    bool sym[n+1];
    sym[4] = 1; printf("4\n");

    for(int k=5;k<=n;k++){
        sym[k] = 1;

        for(int i=1;i<=k-4;i++){
            for(int j=k;j<=n;j++){
                if(graph[i*(n+1) + j] == 1){
                    sym[k] = 0;
                }
            }
        }

        if(sym[k] == 1){
            printf("%d\n", k);
        }
    }

    free(graph);
    return 0;
}
