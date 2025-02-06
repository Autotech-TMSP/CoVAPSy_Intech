from HokuyoReader import HokuyoReader

import time
from rpi_hardware_pwm import HardwarePWM

IP = '192.168.0.10'
PORT = 10940

#paramètres de la fonction vitesse_m_s
direction_prop = 1 # -1 pour les variateurs inversés ou un petit rapport correspond à une marche avant
pwm_stop_prop = 7.53
point_mort_prop = 0.5
delta_pwm_max_prop = 1.1 #pwm à laquelle on atteint la vitesse maximale

vitesse_max_m_s_hard = 8 #vitesse que peut atteindre la voiture
vitesse_max_m_s_soft = 2 #vitesse maximale que l'on souhaite atteindre


#paramètres de la fonction set_direction_degre
direction = 1 #1 pour angle_pwm_min a gauche, -1 pour angle_pwm_min à droite
angle_pwm_min = 6.91 #min
angle_pwm_max = 10.7   #max
angle_pwm_centre= 8.805

angle_degre_max = +18 #vers la gauche
angle_degre=0

pwm_prop = HardwarePWM(pwm_channel=0, hz=50, chip=2) #use chip 2 on pi 5 in accordance with the documentation
pwm_prop.start(pwm_stop_prop)

def set_vitesse_m_s(vitesse_m_s):
    if vitesse_m_s > vitesse_max_m_s_soft :
        vitesse_m_s = vitesse_max_m_s_soft
    elif vitesse_m_s < -vitesse_max_m_s_hard :
        vitesse_m_s = -vitesse_max_m_s_hard
    if vitesse_m_s == 0 :
        pwm_prop.change_duty_cycle(pwm_stop_prop)
    elif vitesse_m_s > 0 :
        vitesse = vitesse_m_s * (delta_pwm_max_prop)/vitesse_max_m_s_hard
        pwm_prop.change_duty_cycle(pwm_stop_prop + direction_prop*(point_mort_prop + vitesse ))
    elif vitesse_m_s < 0 :
        vitesse = vitesse_m_s * (delta_pwm_max_prop)/vitesse_max_m_s_hard
        pwm_prop.change_duty_cycle(pwm_stop_prop - direction_prop*(point_mort_prop - vitesse ))
        
def recule():
    set_vitesse_m_s(-vitesse_max_m_s_hard)
    time.sleep(0.2)
    set_vitesse_m_s(0)
    time.sleep(0.2)
    set_vitesse_m_s(-1)
    
pwm_dir = HardwarePWM(pwm_channel=1,hz=50,chip=2) #use chip 2 on pi 5 in accordance with the documentation 
pwm_dir.start(angle_pwm_centre)

def set_direction_degre(angle_degre) :
    global angle_pwm_min
    global angle_pwm_max
    global angle_pwm_centre
    angle_pwm = angle_pwm_centre + direction * (angle_pwm_max - angle_pwm_min) * angle_degre /(2 * angle_degre_max )
    if angle_pwm > angle_pwm_max : 
        angle_pwm = angle_pwm_max
    if angle_pwm < angle_pwm_min :
        angle_pwm = angle_pwm_min
    pwm_dir.change_duty_cycle(angle_pwm)
    
#connexion et démarrage du lidar
lidar = HokuyoReader(IP, PORT) 
lidar.stop()
lidar.startContinuous(0, 1080)


tableau_lidar_mm = [0]*360 #création d'un tableau de 360 zéros

time.sleep(1) #temps de démarrage du lidar

try : 
    while True :
        for angle in range(len(tableau_lidar_mm)) :
            # translation of the angle from the lidar to the angle of the table
            if angle > 135 and angle < 225:
                tableau_lidar_mm[angle] = float('nan')
            else:
                tableau_lidar_mm[angle] = lidar.rDistance[540 + (-angle * 4)]
        #l'angle de la direction est la différence entre les mesures  
        #des rayons du lidar à -60 et +60°  
        small_index=[]
        small_dist=[]
        for index, angle in enumerate(lidar.rDistance):
            if angle < 50 and angle != 0:
                small_index.append(index)
                small_dist.append(angle)    
        print(small_index,small_dist)
        angle_degre = 0.02*(tableau_lidar_mm[60]-tableau_lidar_mm[-60])
        #print(tableau_lidar_mm[60], tableau_lidar_mm[-60], angle_degre)
        set_direction_degre(angle_degre)
        vitesse_m_s = 0.05
        set_vitesse_m_s(vitesse_m_s)    
        time.sleep(0.1)
        ##############################################
except KeyboardInterrupt: #récupération du CTRL+C
    vitesse_m_s = 0
    set_vitesse_m_s(vitesse_m_s)
    print("fin des acquisitions")

#arrêt et déconnexion du lidar et des moteurs
lidar.stop()
pwm_dir.stop()
pwm_prop.start(pwm_stop_prop)


