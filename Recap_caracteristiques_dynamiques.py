################################################################################################################
####################################### PROJET AÉRODYNAMIQUE LANCEURS ##########################################
################################################################################################################

######################################## Importation des bibliothèques #########################################


import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math as mt
from scipy import interpolate
from scipy import interpolate


############################################ Constantes et entrées #############################################

### Valeurs constantes ###
Tinf = 288.15
rhoinf = 1.2
g0 = 9.80665
r = 287
ddelta = 2



### Liste mémoires ###
Liste_T0 = []
Liste_P0 = []
Liste_rho0 = []
Liste_Ti0 = []
Liste_Pi0 = []
Liste_rhoi0 = []
Liste_mu0 = []
Liste_gamma0 = []
Liste_Regime0 = []
Liste_T1 = []
Liste_P1 = []
Liste_rho1 = []
Liste_Ti1 = []
Liste_Pi1 = []
Liste_rhoi1 = []
Liste_mu1 = []
Liste_M1 = []
Liste_gamma1 = []
Liste_Regime1 = []
Liste_Angle_choc = []
Liste_Type_choc = []
Liste_Libre_parcourt = []


############################################### Choix du point #################################################

Point = ''
if (Point == 'Point 1'):
    z = 6750
    vz = 264
    vx = 107.4
    az = 12.72
    ax = 5.17
    Pinf = 24360
    M = 0.84
    theta = 67.86
    m = 502362
    L = 60
    S = 52.67
    g = 9.80664
    Cx = 0.195
    poids = 4926483
    trainee_z = 251135
    trainee_x = 102180
    poussee_z = 7527762
    poussee_x = 3062831
    temps = 55
elif (Point == 'Point 2'):
    z = 15000
    vz = 374.49
    vx = 353.52
    az = 16.19
    ax = 15.28
    Pinf = 32000
    M = 1.51
    theta = 46.65
    m = 427204
    L = 60
    S = 52.67
    g = 9.80660
    Cx = 0.195
    poids = 4189419
    trainee_z = 198084
    trainee_x = 186992
    poussee_z = 5909743
    poussee_x = 5578805
    temps = 80
elif (Point == 'Point 3'):
    z = 163000
    vz = 0
    vx = 6355
    az = -0.32
    ax = 33.83
    Pinf = 71000
    M = 18.69
    theta = -0.54
    m = 38908
    L = 18.5
    S = 20.36
    g = 9.80025
    Cx = 0.0185
    poids = 381308
    trainee_z = 0
    trainee_x = 0
    poussee_z = -8803
    poussee_x = 933959
    temps = 453
elif (Point == 'Point 4'):
    z = 162000
    vz = 0
    vx = 7400
    az = 0
    ax = 9.81
    Pinf = 22300
    M = 21.76
    theta = 0.035
    m = 38908
    L = 18.5
    S = 20.36
    g = 9.80025
    Cx = 0.0185
    poids = 381308
    trainee_z = 0
    trainee_x = 0
    poussee_z = 0
    poussee_x = 0
    temps = 504


############################################ Fonctions secondaires #############################################

### Température amont ###
def calcul_T0(z):
    if (z <= 11) :
        T0 = Tinf - 0.0065*z
    else :
        T0 = 216.66
    return(T0)

### Pression amont ###
def calcul_P0(z,T0):
    if (z <= 11000) :
        P0 = Pinf*np.exp(-(z-11000)/6341.6)
    else :
        P0 = Pinf*pow((T0/Tinf),5.2561)
    return(P0)

### Masse volumique amont ###
def calcul_rho0(z,T0):
    rho0 = rhoinf*np.exp(-z*g0/r/T0)
    return(rho0)

### Température génératrice amont ###
def calcul_Ti0(T0,gamma,M):
    Ti0 = T0*(1+(gamma-1)/2*pow(M,2))
    return(Ti0)

### Pression génératrice amont ###
def calcul_Pi0(P0,gamma):
    Pi0 = P0*pow((1+(gamma-1)/2*pow(M,2)),gamma/(gamma-1))
    return(Pi0)

### Masse volumique génératrice amont ###
def calcul_rhoi0(rho0,gamma):
    rhoi0 = rho0*pow((1+(gamma-1)/2*pow(M,2)),1/(gamma-1))
    return(rhoi0)

### Angle de choc ###
def calcul_Anglechoc():
    return()

### Type de choc ###
def calcul_Typechoc(delta,ddelta):
    if (delta < -ddelta*np.pi/180) :
        choc = 'detente'
    elif ((delta >= -ddelta*np.pi/180) and (delta <= ddelta*np.pi/180)) :
        choc = 'plat'
    elif ((delta > ddelta*np.pi/180) and (delta <= 50*np.pi/180 - ddelta*np.pi/180)) :
        choc = 'oblique'
    elif ((delta > 50*np.pi/180 - ddelta*np.pi/180) and (delta < 90*np.pi/180 - ddelta*np.pi/180)) :
        choc = 'decolle'
    elif ((delta >= 90*np.pi/180 - ddelta*np.pi/180) and (delta <= 90*np.pi/180 + ddelta*np.pi/180)) :
        choc = 'droit'
    return(choc)

### Régime amont ###
def calcul_Regime0(M) :
    if (M < 0.8) :
        regime0 = 'Subsonique'
    elif ((M >= 0.8) and (M < 1.2)) :
        regime0 = 'Transsonique'
    elif ((M >= 1.2) and (M < 5)) :
        regime0 = 'Supersonique'
    else :
        regime0 = 'Hypersonique'
    return(regime0)

### Cone de Mach amont ###
def calcul_Mu0():
    mu0 = np.arcsin(1/M)
    return(mu0)

### Libre parcours moyen ###
def calcul_Libreparcours(z):
    zp = [0,50,100,300,700,3000]
    lp = [0.00001,0.01,10,100000,10000000,10000000000]
    l = interpolate.interp1d(zp,lp,kind='linear')
    return(l(z))

### Constante de l'air amont ###
def calcul_Gamma0(T0):
    gamma = -7.857142852*0.00001*T0+1.416666667
    return(gamma)

### Constante de l'air aval ###
def calcul_Gamma1(T1):
    gamma1 = -7.857142852*0.00001*T1+1.416666667
    return(gamma1)

### Mach en aval ###
def calcul_M1(regime0,choc,M0,mu0,gamma):
    if (regime0 == 'Subsonique') :
        M1 = M0
    if (regime0 == 'Transsonique') :
        M1 = M0
    if (regime0 == 'Hypersonique') :
        if (choc == 'plat') :
            M1 = M0
        elif (choc == 'oblique') :
            M1 = np.sqrt((gamma-1)/(2*gamma))
        elif (choc == 'decolle') :
            M1 = np.sqrt((gamma-1)/(2*gamma))
        elif (choc == 'droit') :
            M1 = np.sqrt((gamma-1)/(2*gamma))
        elif (choc == 'detente') :
            k = pow(mu0/(np.pi/2*(np.sqrt(6)-1)),2/3)
            M1 = (1+1.3604*k+0.0962*pow(k,2)-0.5127*pow(k,3))/(1-0.6722*k-0.3278*pow(k,2))
    if (regime0 == 'Supersonique') :
        if (choc == 'plat') :
            M1 = M0
        elif (choc == 'oblique') :
            M1 = np.sqrt((gamma-1)/(2*gamma))
        elif (choc == 'decolle') :
            M1 = np.sqrt((gamma-1)/(2*gamma))
        elif (choc == 'droit') :
            M1 = np.sqrt((1+(gamma-1)/2*pow(M0,2))/(gamma*pow(M0,2)-(gamma-1)/2))
        elif (choc == 'detente') :
            k = pow(mu0/(np.pi/2*(np.sqrt(6)-1)),2/3)
            M1 = (1+1.3604*k+0.0962*pow(k,2)-0.5127*pow(k,3))/(1-0.6722*k-0.3278*pow(k,2))
    return(M1)

### Température en aval ###
def calcul_T1(regime0,choc,M0,M1,gamma0,delta,T0,P0,P1,rho0,rho1):
    if (regime0 == 'Subsonique') :
        T1 = T0
    if (regime0 == 'Transsonique') :
        T1 = T0
    if (regime0 == 'Supersonique') :
        if (choc == 'plat') :
            T1 = T0
        elif (choc == 'oblique') :
            T1 = P1/P0*rho0/rho1
        elif (choc == 'decolle') :
            T1 = P1/P0*rho0/rho1
        elif (choc == 'droit') :
            T1 = T0*((2+(gamma0-1)*pow(M0,2))/((gamma0+1)*pow(M0,2)))*(1+2*gamma0/(gamma0+1)*(pow(M0,2)-1))
        elif (choc == 'detente') :
            T1 = T0*(1+(gamma0-1)/2*pow(M0,2))/(1+(gamma0-1)/2*pow(M1,2))
    if (regime0 == 'Hypersonique') :
        if (choc == 'droit') :
            T1 = T0*(2*gamma0*(gamma0-1)/pow(gamma0+1,2))*pow(M0,2)
        elif (choc == 'oblique') :
            T1 = T0*(2*gamma0*(gamma0-1)/pow(gamma0+1,2))*pow(M0,2)*pow(np.sin(delta),2)
        elif (choc == 'decolle') :
            T1 = T0*(2*gamma0*(gamma0-1)/pow(gamma0+1,2))*pow(M0,2)*pow(np.sin(delta),2)
        elif (choc == 'plat') :
            T1 = T0
        elif (choc == 'detente') :
            T1 = T0*((1+((gamma0-1)/2)*pow(M0,2)))/((1+((gamma0-1)/2)*pow(M1,2)))
    return(T1)

### Pression en aval ###
def calcul_P1(regime0,choc,gamma0,P0,M0,delta,M1):
    if (regime0 == 'Subsonique') :
        P1 = P0
    if (regime0 == 'Transsonique') :
        P1 = P0
    if (regime0 == 'Supersonique') :
        if (choc == 'plat') :
            P1 = P0
        elif (choc == 'oblique') :
            P1 = P0*(1+2*gamma0/(gamma0+1)*(pow(M0*np.sin(delta),2)-1))
        elif (choc == 'decolle') :
            P1 = P0*(1+2*gamma0/(gamma0+1)*(pow(M0*np.sin(delta),2)-1))
        elif (choc == 'droit') :
            P1 = P0*(1+2*gamma0/(gamma0+1)*(pow(M0,2)-1))
        elif (choc == 'detente') :
            P1 = P0*pow((1+(gamma0-1)/2*pow(M0,2))/(1+(gamma0-1)/2*pow(M1,2)),gamma0/(gamma0-1))
    if (regime0 == 'Hypersonique') :
        if (choc == 'droit') :
            P1 = P0*(2*gamma0/(gamma0+1))*pow(M0,2)
        elif (choc == 'oblique') :
            P1 = P0*(2*gamma0/(gamma0+1))*pow(M0,2)*pow(np.sin(delta),2)
        elif (choc == 'decolle') :
            P1 = P0*(2*gamma0/(gamma0+1))*pow(M0,2)*pow(np.sin(delta),2)
        elif (choc == 'plat') :
            P1 = P0
        elif (choc == 'detente') :
            P1 = P0*pow(((1+((gamma0-1)/2)*pow(M0,2)))/((1+((gamma0-1)/2)*pow(M1,2))),(gamma0/(gamma0-1)))
    return(P1)

### Masse volumique en aval ###
def calcul_rho1(regime0,choc,rho0,M0,gamma0,delta):
    if (regime0 == 'Subsonique') :
        rho1 = rho0
    if (regime0 == 'Transsonique') :
        rho1 = rho0
    if (regime0 == 'Supersonique') :
        if (choc == 'plat') :
            rho1 = rho0
        elif (choc == 'oblique') :
            rho1 = rho0*(gamma0+1)*pow(M0*np.sin(delta),2)/((gamma0-1)*(pow(M0*np.sin(delta),2)+2))
        elif (choc == 'decolle') :
            rho1 = rho0*(gamma0+1)*pow(M0*np.sin(delta),2)/((gamma0-1)*(pow(M0*np.sin(delta),2)+2))
        elif (choc == 'droit') :
            rho1 = rho0*(2*gamma0/(2/(gamma0+1))*pow(M0,2)+(gamma0-1)/(gamma0+1))
        elif (choc == 'detente') :
            rho1 = rho0*pow((1+(gamma0-1)/2*pow(M0,2))/(1+(gamma0-1)/2*pow(M1,2)),1/(gamma0-1))
    if (regime0 == 'Hypersonique') :
        if (choc == 'droit') :
            rho1 = rho0*(gamma0+1)/(gamma0-1)
        elif (choc == 'oblique') :
            rho1 = rho0*(gamma0+1)/(gamma0-1)
        elif (choc == 'decolle') :
            rho1 = rho0*(gamma0+1)/(gamma0-1)
        elif (choc == 'plat') :
            rho1 = rho0
        elif (choc == 'detente') :
            rho1 = rho0*pow(((1+((gamma0-1)/2)*pow(M0,2)))/((1+((gamma0-1)/2)*pow(M1,2))), (1/(gamma0-1)))
    return(rho1)

### Température génératrice en aval ###
def calcul_Ti1(T1,gamma1,M1):
    Ti1 = T1*(1+(gamma1-1)/2*pow(M1,2))
    return(Ti1)

### Pression génératrice en aval ###
def calcul_Pi1(P1,gamma1,M1):
    Pi1 = P1*pow((1+(gamma1-1)/2*pow(M1,2)),gamma1/(gamma1-1))
    return(Pi1)

### Masse volumique génératrice en aval ###
def calcul_rhoi1(rho1,gamma1,M1):
    rhoi1 = rho1*pow((1+(gamma1-1)/2*pow(M1,2)),1/(gamma1-1))
    return(rhoi1)

### Angle de Mach en aval ###
def calcul_Mu1(M1):
    if (M1 >= 1):
        mu1 = np.arcsin(1/M1)*180/np.pi
    else :
        mu1 = 0
    return(mu1)

### Type de régime en aval ###
def calcul_Regime1(M1):
    if (M1 < 0.8) :
        regime1 = 'Subsonique'
    elif ((M1 >= 0.8) and (M1 < 1.2)) :
        regime1 = 'Transsonique'
    elif ((M1 >= 1.2) and (M1 < 5)) :
        regime1 = 'Supersonique'
    else :
        regime1 = 'Hypersonique'
    return(regime1)


############################################ Fonctions principales #############################################

### Géométrie du lanceur ###
zz = [-1.8,-1.8,-2.6,-2.6,-2.1,-1.4,-.65,0,.65,1.4,2.1,2.6,2.6,1.8,1.8,-1.8]
xx = [0,55.6,57,65.5,67,68.5,69.5,70,69.5,68.5,67,65.5,57,55.6,0,0]
geo_x = np.linspace(0,70,140)
geo_z = interpolate.interp1d(xx,zz,kind='linear')


### Boucle de calcul ###

for i in range(1,len(geo_x)) :

    ### Valeurs en amont du choc ###
    T0 = calcul_T0(z)
    Liste_T0.append(T0)

    P0 = calcul_P0(z,T0)
    Liste_P0.append(P0)

    rho0 = calcul_rho0(z,T0)
    Liste_rho0.append(rho0)

    gamma0 = calcul_Gamma0(T0)
    Liste_gamma0.append(gamma0)

    Ti0 = calcul_Ti0(T0,gamma0,M)
    Liste_Ti0.append(Ti0)

    Pi0 = calcul_Pi0(P0,gamma0)
    Liste_Pi0.append(Pi0)

    rhoi0 = calcul_rhoi0(rho0,gamma0)
    Liste_rhoi0.append(rhoi0)

    Mu0 = calcul_Mu0()
    Liste_mu0.append(Mu0)

    regime0 = calcul_Regime0(M)
    Liste_Regime0.append(regime0)


    ### Valeurs au choc ###
    delta = calcul_Anglechoc()
    Liste_Angle_choc.append(delta)

    choc = calcul_Typechoc(delta,ddelta)
    Liste_Type_choc.append(choc)

    lib = calcul_Libreparcours(z)
    Liste_Libre_parcourt.append(lib)


    ### Valeurs en aval du choc ###
    M1 = calcul_M1(regime0,choc,M,Mu0,gamma0)
    Liste_M1.append(M1)

    P1 = calcul_P1(regime0,choc,gamma0,P0,M,delta,M1)
    Liste_P1.append(P1)

    rho1 = calcul_rho1(regime0,choc,rho0,M,gamma0,delta)
    Liste_rho1.append(rho1)

    T1 = calcul_T1(regime0,choc,M,M1,gamma0,delta,T0,T0,P1,rho0,rho1)
    Liste_T1.append(T1)

    gamma1 = calcul_Gamma1(T1)
    Liste_gamma1.append(gamma1)

    Ti1 = calcul_Ti1(T1,gamma1,M1)
    Liste_Ti1.append(Ti1)

    Pi1 = calcul_Pi1(P1,gamma1,M1)
    Liste_Pi1.append(Pi1)

    rhoi1 = calcul_rhoi1(rho1,gamma1,M1)
    Liste_rhoi1.append(rhoi1)

    Mu1 = calcul_Mu1(M1)
    Liste_mu1.append(Mu1)

    regime1 = calcul_Regime1(M1)
    Liste_Regime1.append(regime1)


################################################################################################################
####################################### PROJET AÉRODYNAMIQUE LANCEURS ##########################################
################################################################################################################