from HokuyoReader import HokuyoReader

import time
from rpi_hardware_pwm import HardwarePWM
import math

IP = '192.168.0.10'
PORT = 10940
CRASH_DIST = 135  #mm

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
    print("recule")
    time.sleep(0.4)
    set_vitesse_m_s(0)
    time.sleep(0.4)
    set_vitesse_m_s(-2)
    
    
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
    


def conduite_autonome2(rDistance):
        for angle in range(len(tableau_lidar_mm)) :
            # translation of the angle from the lidar to the angle of the table
            if angle > 135 and angle < 225:
                tableau_lidar_mm[angle] = float('nan')
            else:
                tableau_lidar_mm[angle] = lidar.rDistance[540 + (-angle * 4)]

        ####################################################
        ###################################################

        maxi = 0
        maxi_n = 0

        f=15

        for i in range(-45, 45):
            j = 0
            for n in range(i-f , i+f):
                j += tableau_lidar_mm[n]
            if j > maxi:
                maxi = j
                maxi_n = i
        print("maxi = ", maxi," n = ", maxi_n)


        proche = 20000

        V45 = 0
        n_V45 = 0
        for i in range(-45 , 45) :
            test_min = tableau_lidar_mm[i]
            if (test_min != 0):
                V45 += test_min
                n_V45 += 1
                if (test_min < proche):
                    proche = test_min
        V45 = V45/n_V45
        if (proche > 0) and (proche <= 180) :
            print(proche)
            vitesse = 0
            print("close")
            recule()
        else :
            vitesse = V45*0.002
            print("v = ",vitesse)
            vitesse = 2

        set_vitesse_m_s(vitesse)


        if vitesse >= 0.057 :
            try :
                angle_cible = (maxi_n/180)*math.pi
                val = (1.35*angle_cible)/vitesse
                print("val = ",val)
                angle = (math.atan(val)/math.pi)*180
            except :
                angle = 0
                print("pb angle")
        else :
            angle = 0
        print("angle = ",angle)
        set_direction_degre(angle)
        
def has_Crashed():
    small_index=[]
    small_dist=[]
    for index, angle in enumerate(lidar.rDistance):
        if angle < CRASH_DIST and angle != 0:
            small_index.append(index)
            small_dist.append(angle)
                
    if len(small_dist)>2:
        print(small_index,small_dist)
        return True
    else:
        return False
    

def drive():
    while True:
        if has_Crashed():
            recule()
            time.sleep(0.5)
        conduite_autonome2()

if __name__ == '__main__':
    #connexion et démarrage du lidar
    lidar = HokuyoReader(IP, PORT) 
    lidar.stop()
    lidar.startContinuous(0, 1080)


    tableau_lidar_mm = [0]*360 #création d'un tableau de 360 zéros

    time.sleep(1) #temps de démarrage du lidar
    try : 
        drive()
    except KeyboardInterrupt: #récupération du CTRL+C
        vitesse_m_s = 0
        set_vitesse_m_s(vitesse_m_s)
        print("fin des acquisitions")

    #arrêt et déconnexion du lidar et des moteurs
    lidar.stop()
    pwm_dir.stop()
    pwm_prop.start(pwm_stop_prop)