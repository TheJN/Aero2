################################################################################################################
######################################## PROJET AÉRODYNAMIQUE LANCEURS #########################################
################################################################################################################

######################################## Importation des bibliothèques #########################################


import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math as mt
from scipy import interpolate


############################################ Constantes et entrées #############################################

### Boucle de calcul ###
mini = 1
maxi = 6630


### Listes de valeurs ###
t = np.linspace(0,6630,6630)
m = np.zeros(6630)
L = np.zeros(6630)
b = np.pi/(6630*10)
alti = np.linspace(0,200,6630)


### Conditions initiales ###
x = 0
z = 0
x0 = 0
z0 = 0
vx = 0
vz = 0
v0x = 0
v0z = 0
ax = 0
az = 0
trainee_x = 0
trainee_z = 0
poussee_x = 0
poussee_z = 0
Temps = 0
alt = 0


### Constantes ###
theta = 90*np.pi/180
rhoinf = 1.2
Tinf = 288
g0 = 9.80665
Rt = 6378000
delta_t = 1
dtheta = 5
D = 5.2
h = 5.9
d = 3.6
Pa = 101325
R = 8.314
Mm = 0.028965
r = R/Mm


### Listes mémoire ###
altitude2 =[]
rho0 = []
Temps3 = []
Ang_P2 = []
Temps5 = []
Vit2 = []
Liste_g = []
Liste_acceleration_x = []
Liste_acceleration_z = []
Liste_vitesse_x = []
Liste_vitesse_z = []
Liste_position_x = []
Liste_position_z = []
Liste_Mach = []
Liste_Cx = []
Liste_poids = []
Liste_poussee_x = []
Liste_poussee_z = []
Liste_trainee_x = []
Liste_trainee_z = []
Liste_theta = []
Liste_masse = []
Liste_L = []
Liste_S = []
Liste_Temps = []
Liste_Pinf = []
beta2 = []
Liste_vitesse = []
Liste_acceleration = []
Liste_poussee = []
Liste_trainee = []


############################################ Fonctions secondaires #############################################


### Longueur ###
def calcul_longueur(t):
    if (t < 158):
        L = 60
    else :
        L = 18.5
    return(L)


### Surface ###
def calcul_surface(t,D,h,d):
    if (t < 210) :
        S = np.pi*(D/2)*np.sqrt(pow(D/2,2)+pow(h/2,2))
    else :
        S = 2*np.pi*pow(d/2,2)
    return(S)


### Masse ###
def calcul_masse(t) :
    if (t <= 158) :
        m = 667710 - 3006.329114*t  
    elif ((t > 158) and (t <= 163)) :
        m = 130960  
    elif ((t > 163) and (t <= 210)) :
        m = 130960 - 279.297872*(t - 163)  
    elif ((t > 210) and (t <= 489)) :
        m = 116833 - 279.297872*(t - 210)      
    elif ((t > 489) and (t <= 1630)) :
        m = 38908     
    elif ((t > 1630) and (t <= 1675)) :
        m = 38908 - 279.311111*(t - 1630)  
    elif ((t > 1675) and (t <= 6600)) :
        m = 26339 
    elif (t > 6600) :
        m = 26339 - 279.300000*(t - 6600) 
    return(m) 


### Gravité ###
def calcul_gravite(z):
    g = g0*pow(Rt,2)/pow(Rt+z,2)
    return(g)


### Force du poids ###
def calcul_poids(m,g):
    poids = m*g
    return(poids)


### Coefficient de trainée ###
def calcul_Coeff_trainee(L,D):
    Cx = 0.00115*pow(L,2)/(np.pi*pow(D,2)/4)
    return(Cx)  


### Masse volumique ###
def calcul_visco():
    altitude = [0,5,10,15,20,25,30,35,40,45,50,75,100,125,150,175,200]
    rhoinf2 = [1.2,0.75,0.4,0.2,0.1,0.066,0.033,0.01,0,0,0,0,0,0,0,0,0]
    altitude2 = np.linspace(altitude[0],altitude[-1],6630)
    rho0 = interpolate.interp1d(altitude,rhoinf2,kind = 'cubic')
    return(altitude2,rho0(altitude2))


### Vitesse trainée ###
def calcul_Vit_Trainee():
    Temps4 = [0,105,156,257,340,398,440,472,488,1092,1620,1653,2167,2892,3378,3992,4725,6000,6630]
    Vit = [0,1011,2383,3000,4000,5000,6000,7000,7455,7423,7355,8383,8000,6792,6000,5200,4511,3986,4030]
    Temps5 = np.linspace(Temps4[0],Temps4[-1],6630)
    Vit2 = interpolate.interp1d(Temps4,Vit,kind = 'linear')
    return(Temps5,Vit2(Temps5))


### Force de traînée ###
def calcul_trainee(Vit2,Ang_P2,S,Cx,rho0):
    trainee_x = 0.5*rho0*S*Cx*pow(Vit2*np.cos(Ang_P2*np.pi/180),2)
    trainee_z = 0.5*rho0*S*Cx*pow(Vit2*np.sin(Ang_P2*np.pi/180),2)  
    return(trainee_x,trainee_z)


### Angle de Poussée ###
def calcul_Ang_Pousse():
    Temps2 = [0,21,40,64,90,117,178,253,385,400,600,900,1200,1500,1654,2177,3000,3500,4675,5255,6175,6630]
    Ang_P = [90,89,80,60,40,30,20,10,0,0,0,0,0,0,0,10,18,19.5,15,10,0,-4.5]
    Temps3 = np.linspace(Temps2[0],Temps2[-1],6630)
    Ang_P2 = interpolate.interp1d(Temps2,Ang_P,kind = 'cubic')
    return(Temps3,Ang_P2(Temps3))


### Poussée ###
def calcul_poussee(Temps,Ang_P2):
    if (Temps < 158):
        poussee_z = 8127000*np.sin(Ang_P2*np.pi/180)
        poussee_x = 8127000*np.cos(Ang_P2*np.pi/180)
    elif((Temps >= 200) and (Temps < 489)):
        poussee_z = 934000*np.sin(Ang_P2*np.pi/180) 
        poussee_x = 934000*np.cos(Ang_P2*np.pi/180) 
    elif((Temps >= 1630) and (Temps < 1675)):
        poussee_z = 934000*np.sin(Ang_P2*np.pi/180)
        poussee_x = 934000*np.cos(Ang_P2*np.pi/180) 
    elif((Temps >= 6600) and (Temps < 6630)):
        poussee_z = 934000*np.sin(Ang_P2*np.pi/180)
        poussee_x = 934000*np.cos(Ang_P2*np.pi/180)
    else :
        poussee_x = 0
        poussee_z = 0    
    return(poussee_x,poussee_z) 


### Accélération ###
def calcul_acceleration(poids,trainee_x,trainee_z,poussee_x,poussee_z,m):
    ax = (- trainee_x + poussee_x)/m
    az = (- poids - trainee_z + poussee_z)/m 
    return(ax,az)


### Vitesse ###
def calcul_vitesse(ax,az,v0z,v0x):
    vx = ax*delta_t + v0x
    vz = az*delta_t + v0z
    return(vx,vz)


### Position ###
def calcul_position(x0,z0,ax,az,vx0,vz0):
    x = 0.5*ax*pow(delta_t,2) + vx0*delta_t + x0
    z = 0.5*az*pow(delta_t,2) + vz0*delta_t + z0
    return(x,z)


## Mach ###
def calcul_Mach(vz,vx):
    M = np.sqrt(pow(vx,2) + pow(vz,2))/340
    return(M)


### Angle ###
def calcul_theta(x0,z0,x,z):
    theta = mt.atan2((z-z0),(x-x0))
    return(theta)

### Pression dynamique ###
def calcul_press_dyn(rho,v):
    Pinf = 0.5*rho*pow(v,2)
    return(Pinf)



############################################## Fonction principale ##############################################

### Grandeurs de calcul ###
[Temps5,Vit2] = calcul_Vit_Trainee()
[Temps3,Ang_P2] = calcul_Ang_Pousse()
[altitude2,rho0] = calcul_visco()


### Boucle de calcul ###
for i in range(mini,maxi):

    # Nouvelles conditions initiales #
    x0 = x
    z0 = z
    v0x = vx
    v0z = vz

    # Longueur #
    L = calcul_longueur(i)
    Liste_L.append(L)

    # Surface #
    S = calcul_surface(i,D,h,d)
    Liste_S.append(S)

    # Masse #
    m = calcul_masse(i)
    Liste_masse.append(m)

    # Gravité #
    g = calcul_gravite(200000*i/6630)
    Liste_g.append(g)

    # Force de poids #
    poids = calcul_poids(m,g)
    Liste_poids.append(poids)

    # Coefficient de trainée #
    Cx = calcul_Coeff_trainee(L,D)
    Liste_Cx.append(Cx)

    # Force de trainée #
    [trainee_x,trainee_z] = calcul_trainee(Vit2[i],Ang_P2[i],S,Cx,rho0[i])
    Liste_trainee_x.append(trainee_x)
    Liste_trainee_z.append(trainee_z)
    Liste_trainee.append(np.sqrt(pow(trainee_x,2) + pow(trainee_z,2)))

    # Force de poussée #
    [poussee_x,poussee_z] = calcul_poussee(i,Ang_P2[i])
    Liste_poussee_x.append(poussee_x)
    Liste_poussee_z.append(poussee_z)
    Liste_poussee.append(np.sqrt(pow(poussee_x,2) + pow(poussee_z,2)))

    # Accélération #
    [ax,az] = calcul_acceleration(poids,trainee_x,trainee_z,poussee_x,poussee_z,m)
    Liste_acceleration_x.append(ax/g0)
    Liste_acceleration_z.append(az/g0)
    Liste_acceleration.append(np.sqrt(pow(ax,2) + pow(az,2))/g0)

    # Vitesse #
    [vx,vz] = calcul_vitesse(ax,az,v0z,v0x)
    Liste_vitesse_x.append(vx)
    Liste_vitesse_z.append(vz)
    Liste_vitesse.append(np.sqrt(pow(vx,2) + pow(vz,2)))

    # Position #
    [x,z] = calcul_position(x0,z0,ax,az,v0x,v0z)
    Liste_position_x.append(x)
    Liste_position_z.append(z)

    # Inclinaison #
    theta = calcul_theta(x0,z0,x,z)
    Liste_theta.append(theta*180/np.pi)

    # Mach #
    M = calcul_Mach(vz,vx)
    Liste_Mach.append(M)

    # Pression dynamique #
    Pinf = calcul_press_dyn(rho0[i],Vit2[i])
    Liste_Pinf.append(Pinf)

    # Temps #
    Liste_Temps.append(Temps)
    t = t + delta_t
    Temps = Temps + delta_t



################################################################################################################
######################################## PROJET AÉRODYNAMIQUE LANCEURS #########################################
################################################################################################################


plt.plot(Liste_Temps,Liste_S)
plt.xlabel('Temps (s)')
plt.ylabel('Surface mouillée (m²)')
plt.title("Variation de la surface mouillée au cours du vol")
plt.grid(True)
plt.show()
