#include <bits/stdc++.h>
#ifndef point_pair
#define point_pair pair< point, point >
#endif
#ifndef EPS
#define EPS 1e-6
#endif

using namespace std;

struct point{
	long double x, y, z;

    point(long double _a, long double _b, long double _c){
        x = _a;
        y = _b;
        z = _c;

        if(abs(x) < EPS) x = 0;
        if(abs(y) < EPS) y = 0;
        if(abs(z) < EPS) z = 0;
    }

    point(){
        x = y = z = 0;
    }

    void print(){
        cout << fixed;
        cout << setprecision(10);
        cout << x << ' ' << y << ' ' << z << '\n';
    }
};

struct sphere{
    point center;
    long double radius;

    sphere(){
        center = point();
        radius = 0;
    }

    sphere(point p, long double r){
        center = p;
        radius = r;
    }

    void print(){
        cout << fixed;
        cout << setprecision(10);
        cout << "S[(" << center.x << "," << center.y << "," << center.z << "), " << radius << "]\n";
    }
};

point_pair inter_spheres(long double a1, long double a2, long double a3, long double ra, long double b1, long double b2, long double b3, long double rb, long double c1, long double c2, long double c3, long double rc) {
    long double Sa[6], Sb[6], Sc[6];

    Sa[1] = a1; // e1
    Sa[2] = a2; // e2
    Sa[3] = a3; // e3
    Sa[4] = -0.5 * ra * ra + (a3 * a3) / 2.0 + (a2 * a2) / 2.0 + (a1 * a1) / 2.0; // einf
    Sa[5] = 1.0; // e0

    Sb[1] = b1; // e1
    Sb[2] = b2; // e2
    Sb[3] = b3; // e3
    Sb[4] = -0.5 * rb * rb + (b3 * b3) / 2.0 + (b2 * b2) / 2.0 + (b1 * b1) / 2.0; // einf
    Sb[5] = 1.0; // e0

    Sc[1] = c1; // e1
    Sc[2] = c2; // e2
    Sc[3] = c3; // e3
    Sc[4] = -0.5 * rc * rc + (c3 * c3) / 2.0 + (c2 * c2) / 2.0 + (c1 * c1) / 2.0; // einf
    Sc[5] = 1.0; // e0

    long double Pp[32];

    Pp[16] = (Sa[1] * Sb[2] - Sa[2] * Sb[1]) * Sc[3] + (Sa[3] * Sb[1] - Sa[1] * Sb[3]) * Sc[2] + (Sa[2] * Sb[3] - Sa[3] * Sb[2]) * Sc[1]; // e1 ^ (e2 ^ e3)
    Pp[17] = (Sa[1] * Sb[2] - Sa[2] * Sb[1]) * Sc[4] + (Sa[4] * Sb[1] - Sa[1] * Sb[4]) * Sc[2] + (Sa[2] * Sb[4] - Sa[4] * Sb[2]) * Sc[1]; // e1 ^ (e2 ^ einf)
    Pp[18] = (Sb[1] - Sa[1]) * Sc[2] + (Sa[2] - Sb[2]) * Sc[1] + Sa[1] * Sb[2] - Sa[2] * Sb[1]; // e1 ^ (e2 ^ e0)
    Pp[19] = (Sa[1] * Sb[3] - Sa[3] * Sb[1]) * Sc[4] + (Sa[4] * Sb[1] - Sa[1] * Sb[4]) * Sc[3] + (Sa[3] * Sb[4] - Sa[4] * Sb[3]) * Sc[1]; // e1 ^ (e3 ^ einf)
    Pp[20] = (Sb[1] - Sa[1]) * Sc[3] + (Sa[3] - Sb[3]) * Sc[1] + Sa[1] * Sb[3] - Sa[3] * Sb[1]; // e1 ^ (e3 ^ e0)
    Pp[21] = (Sb[1] - Sa[1]) * Sc[4] + (Sa[4] - Sb[4]) * Sc[1] + Sa[1] * Sb[4] - Sa[4] * Sb[1]; // e1 ^ (einf ^ e0)
    Pp[22] = (Sa[2] * Sb[3] - Sa[3] * Sb[2]) * Sc[4] + (Sa[4] * Sb[2] - Sa[2] * Sb[4]) * Sc[3] + (Sa[3] * Sb[4] - Sa[4] * Sb[3]) * Sc[2]; // e2 ^ (e3 ^ einf)
    Pp[23] = (Sb[2] - Sa[2]) * Sc[3] + (Sa[3] - Sb[3]) * Sc[2] + Sa[2] * Sb[3] - Sa[3] * Sb[2]; // e2 ^ (e3 ^ e0)
    Pp[24] = (Sb[2] - Sa[2]) * Sc[4] + (Sa[4] - Sb[4]) * Sc[2] + Sa[2] * Sb[4] - Sa[4] * Sb[2]; // e2 ^ (einf ^ e0)
    Pp[25] = (Sb[3] - Sa[3]) * Sc[4] + (Sa[4] - Sb[4]) * Sc[3] + Sa[3] * Sb[4] - Sa[4] * Sb[3]; // e3 ^ (einf ^ e0)

    long double u = (Pp[23] * Pp[23] + Pp[20] * Pp[20] + Pp[18] * Pp[18]);
    long double v = sqrt(abs(Pp[25] * Pp[25] + Pp[24] * Pp[24] + 2.0 * Pp[22] * Pp[23] + Pp[21] * Pp[21] + 2.0 * Pp[19] * Pp[20] + 2.0 * Pp[17] * Pp[18] - Pp[16] * Pp[16]));

    long double x1[4];
    x1[1] = (-(Pp[23] * v + Pp[20] * Pp[25] + Pp[18] * Pp[24] - Pp[16] * Pp[23])) / u ; // e1
    x1[2] =   (Pp[20] * v - Pp[23] * Pp[25] + Pp[18] * Pp[21] - Pp[16] * Pp[20])  / u ; // e2
    x1[3] = (-(Pp[18] * v - Pp[23] * Pp[24] - Pp[20] * Pp[21] - Pp[16] * Pp[18])) / u ; // e3

    long double x2[4];
    x2[1] =   (Pp[23] * v - Pp[20] * Pp[25] - Pp[18] * Pp[24] + Pp[16] * Pp[23])  / u ; // e1
    x2[2] = (-(Pp[20] * v + Pp[23] * Pp[25] - Pp[18] * Pp[21] + Pp[16] * Pp[20])) / u ; // e2
    x2[3] =   (Pp[18] * v + Pp[23] * Pp[24] + Pp[20] * Pp[21] + Pp[16] * Pp[18])  / u ; // e3

    return make_pair(point(x1[1], x1[2], x1[3]), point(x2[1], x2[2], x2[3]));
}

point_pair inter_spheres(point a, long double ra, point b, long double rb, point c, long double rc){
    return inter_spheres(a.x, a.y, a.z, ra, b.x, b.y, b.z, rb, c.x, c.y, c.z, rc);
}

point_pair inter_spheres(sphere a, sphere b, sphere c){
    return inter_spheres(a.center, a.radius, b.center, b.radius, c.center, c.radius);
}

int main(int argc, char const *argv[]){
	point p;	
	p = point(1,2,3);
	p.print();

	sphere sp = sphere(point(), 1);
	sp.print();

	sphere a = sphere(point(1,0,0),1);
	sphere b = sphere(point(0,1,0),1);
	sphere c = sphere(point(0,0,1),1);

	point_pair pp = inter_spheres(a, b, c);

	pp.first.print();
	pp.second.print();
	return 0;
}