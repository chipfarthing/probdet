#include "math.h"
#include "stdio.h"

double probdet(double N, double Yb, double K, double xdB)
{
  double x, T, a, Pd, f, term, k, lastterm, e, pi;
  double res, ims, mags, angs, mags1, angs1, magden, angden, reden, imden;
  
  e=1e-6;
  pi=3.14159265358979;
  x=pow(10,xdB/10);
  if((N==1) && (K==1))
     Pd=exp(-Yb/(1+x));
  if((N==1) && (K==2))
     Pd=(1-(pow(1/(1+x/2),2)-1/(1+x/2))*Yb)*exp(-Yb/(1+x/2));
  if(((N==1) && (K!=1) && (K!=2)) || (N!=1))
  {
  T=2*Yb;
  a=-log(e)/T;
  f=exp(a*Yb)/T*1/pow(a+1,N)/pow(1+a/(1+a)*N*x/K,K)/a;
  term=f;
  k=0;
  lastterm=1e9;
  while(fabs(term)>e || fabs(lastterm)>e)
  {
     k=k+1;
     lastterm=term;
     res=a;
     ims=k*pi/T;
     mags=sqrt(pow(res,2)+pow(ims,2));
     angs=atan2(ims,res);
     mags1=sqrt(pow(1+res,2)+pow(ims,2));
     angs1=atan2(ims,1+res);
     magden=mags/mags1*N*x/K;
     angden=angs-angs1;
     reden=1+magden*cos(angden);
     imden=magden*sin(angden);
     magden=pow(sqrt(pow(reden,2)+pow(imden,2)),-K)/mags/pow(mags1,N);
     angden=-atan2(imden,reden)*K-angs-angs1*N;
     term=2*exp(a*Yb)/T*magden*cos(angden)*cos(k*pi/T*Yb);
     f=f+term;
   };
   Pd=1-f; 
  }
  return Pd;
}

