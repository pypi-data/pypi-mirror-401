#ifndef PECON_H
#define PECON_H

typedef struct Corr_Res {
    double coef;
    double pvalue;
} Corr_Res;


double pecon_add(double a, double b);
double pecon_sub(double a, double b);
Corr_Res pecon_corr(double *x, double *y, int n);

#endif
