#include <bits/stdc++.h>
#define NMAX 1000010
#define MOD 100000007
#define ll long long
#define ii pair<int,int>
#define iii pair<int, ii >
#define dd pair<double,double>
#define vi vector< int >
#define vii vector< ii >
#define vvi vector< vi >
#define vvii vector< vii >
#define len(s) (int)(s).length()
#define sz(a) (int)(a).size()
#define cstr(s) (s).c_str()
#define all(a) (a).begin(), (a).end()
#define ok(a) cerr << "OK " << a << '\n';
#define db(x) cerr << #x << " = " << x << '\n';
#define db2(x, y) cerr << #x << " = " << x << " || " << #y << " = " << y << '\n';
#define db3(x, y, z) cerr << #x << " = " << x << " || " << #y << " = " << y << " || " << #z << " = " << z << '\n';
#define db4(x, y, z, w) cerr << #x << " = " << x << " || " << #y << " = " << y << " || " << #z << " = " << z << " || " << #w << " = " << w << '\n';
#define toRad(a) (a)*PI/180.0
#define myabs(a) ((a) < 0 ? -(a) : (a))
#define mdc __gcd
#define edge pair<int, pair<int, double> >


using namespace std;

const long double EPS = 1e-9;
const long double PI = acos(-1);

struct point{
    double a, b, c;

    point(double _a, double _b, double _c){
        a = _a;
        b = _b;
        c = _c;
    }

    point(){
        a = b = c = 0;
    }

    void print(){
        cout << a << ' ' << b << ' ' << c << '\n';
    }
};

void PrintMatrix(double B[4][4]){
    for(int i=0;i<4;i++){
        for(int j=0;j<4;j++){
            cout << B[i][j] << " ";
        }
        putchar('\n');
    }
}

void copy(double B[4][4], double C[4][4]){
    for(int i=0;i<4;i++){
        for(int j=0;j<4;j++){
            B[i][j] = C[i][j];
        }
    }
}

void multiply(double A[4][4], double B[4][4], double C[4][4]){ // C = A * B // https://ideone.com/sko0PR
    for(int i=0; i<4; i++){
        for(int j=0; j<4; j++){
            double aux = 0.0;
            for(int k=0; k<4; k++){
                aux += A[i][k]*B[k][j];
            }
            C[i][j] = aux;
        }
    }
}

point PosicaoAtomo(double B[4][4]){
    return point(B[0][3], B[1][3], B[2][3]);
}

vector<point> X;

void PosicaoPontos(double d[], double t[], double w[], int n){
    for(int i=0;i<=n;i++) X.push_back(point());

    double ct = cos(t[3]);
    double st = sin(t[3]);

    X[2] = point(-d[2], 0, 0);
    X[3] = point(-d[2] + d[3]*ct, d[3]*st , 0);

    // double B1[4][4] = {{1, 0, 0, 0}, {0, 1, 0, 0}, {0, 0, 1, 0}, {0, 0, 0, 1}};
    double B2[4][4] = {{-1, 0, 0, -d[2]}, {0, 1, 0, 0}, {0, 0, -1, 0}, {0, 0, 0, 1}};
    // puts("B2: "); PrintMatrix(B2);
    double di = d[3];
    double B3[4][4] = {{-ct, -st, 0, -di*ct}, {st, -ct, 0, di*st}, {0, 0, 1, 0}, {0, 0, 0, 1}};
    // puts("B3: "); PrintMatrix(B3);
    double B[4][4];

    multiply(B2, B3, B); // B = B2 * B3
    // puts("B: "); PrintMatrix(B);

    for(int i=4;i<=n;i++){
        di = d[i];

        ct = cos(t[i]);
        st = sin(t[i]);

        double cw = cos(w[i]);
        double sw = sin(w[i]);

        // db4(ct, st, cw, sw);db(di);

        double A[4][4] = {{-ct, -st, 0, -di*ct}, {st*cw, -ct*cw, -sw, di*st*cw}, {st*sw, -ct*sw, cw, di*st*sw}, {0, 0, 0, 1}};
        // puts("A: "); PrintMatrix(A);
        double C[4][4];
        multiply(B, A, C); // B = B * A
        // puts("C: "); PrintMatrix(C);
        X[i] = PosicaoAtomo(C);
        copy(B, C);
    }
}

double distance(point P, point Q){
    return (P.a - Q.a)*(P.a - Q.a) + (P.b - Q.b)*(P.b - Q.b) + (P.c - Q.c)*(P.c - Q.c);
}

double realRand(double a, double b){
    double r;

    do{
         r = ((double) rand() / RAND_MAX);
    }while(abs(r) < EPS || abs(1 - r) < EPS);

    return a + (b - a)*r;
}

double d[NMAX+1]; 
double t[NMAX+1]; 
double w[NMAX+1]; 

void fisherYatesShuffle(int vet[], int n){
    for(int i=0;i<n;i++) vet[i] = i;

    for(int i=n-1;i>0;i--){
        int index = rand()%(i+1);

        int t = vet[i];
        vet[i] = vet[index];
        vet[index] = t;
    }
}

int pos[30*NMAX];

int main(){

    cerr << "Entre com um caso: "; int caso; cin >> caso; for(int i=1;i<=caso;i++) rand();
    cerr << "Entre com o numero de atomos: ";
    int n; cin >> n;

    for(int i=1;i<=n;i++) d[i] = 1.526; d[1] = 0;
    for(int i=1;i<=n;i++) t[i] = 1.91; t[1] = t[2] = 0;
    for(int i=4;i<=n;i++) {
        double omega = realRand(0, PI)*(pow(-1,rand()%4));
        w[i] = omega;
    }
    w[1] = w[2] = w[3] = 0;
    
    PosicaoPontos(d, t, w, n); 
    vector<edge> vet;

    for(int i=1;i<=n;i++){
        for(int j=i+1;j<=min(i+3, n);j++){
            double d = distance(X[i], X[j]);
			edge e = make_pair(i,make_pair(j,sqrt(d)));
            vet.push_back(e);
        }
    }

    cerr << "Entre com a quantidade de simetrias: ";
    int sym; cin >> sym;

    vi shuf; for(int i=5;i<=n;i++) shuf.push_back(i);
    random_shuffle(all(shuf));

    vi S; S.push_back(4);
    for(int j=0;j<sym-1;j++){
        S.push_back(shuf[j]);
    }

    S.push_back(n+1);

    sort(all(S));
    for(int j=0;j<sz(S)-1;j++) cerr << S[j] << ' '; cerr << "\n\n";

    double r = 25.0; 

    for(int k=1;k<sz(S);k++){
        int a = S[k-1];
        int b = S[k];

        for(int j=a+1;j<b;j++){
            for(int i=a-3;i+3<j;i++){
                double d = distance(X[i], X[j]);

                if(d < r) {
                    edge e = make_pair(i,make_pair(j,sqrt(d)));
                    vet.push_back(e);
                }
            }
        }
    }

    int m = sz(vet);

    printf("%d %d\n", n, m);

    fisherYatesShuffle(pos, m);

    for(int i=0;i<m;i++){
        edge atu = vet[pos[i]];
        
        int u = atu.first;
        int v = atu.second.first;
        double d = atu.second.second;
        printf("%5d %5d %.10lf\n", u, v, d);
    }

    return 0;
}
