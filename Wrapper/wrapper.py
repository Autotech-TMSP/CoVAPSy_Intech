from Lidar.HokuyoReader import HokuyoReader
import time
from rpi_hardware_pwm import HardwarePWM

class Wrapper():

    def __init__(self):
        
        self.IP = '192.168.0.10'
        self.PORT = 10940

        # Paramètres de la fonction vitesse_m_s
        self.direction_prop = 1                                                             # -1 pour les variateurs inversés ou un petit rapport correspond à une marche avant
        self.pwm_stop_prop = 7.53
        self.point_mort_prop = 0.5
        self.delta_pwm_max_prop = 1.1                                                       # pwm à laquelle on atteint la vitesse maximale

        self.vitesse_max_m_s_hard = 8                                                       # vitesse que peut atteindre la voiture
        self.vitesse_max_m_s_soft = 2                                                       # vitesse maximale que l'on souhaite atteindre


        # Paramètres de la fonction set_direction_degre
        self.direction = 1                                                                  #1 pour angle_pwm_min a gauche, -1 pour angle_pwm_min à droite
        self.angle_pwm_min = 6.91                                                           # min
        self.angle_pwm_max = 10.7                                                           # max
        self.angle_pwm_centre= 8.805

        self.angle_degre_max = +18                                                          # vers la gauche
        self.angle_degre=0

        # Initialisation des pwm

        self.pwm_prop = HardwarePWM(pwm_channel=0, hz=50, chip=2)                           # Utilisation du chip 2 sur la pi 5 pour correspondre à la documentation
        self.pwm_prop.start(self.pwm_stop_prop)

        self.pwm_dir = HardwarePWM(pwm_channel=1,hz=50,chip=2)                              # Utilisation du chip 2 sur la pi 5 pour correspondre à la documentation
        self.pwm_dir.start(self.angle_pwm_centre)

        # Initialisation du lidar

        self.lidar = HokuyoReader(self.IP, self.PORT) 
        self.lidar.stop()
        self.lidar.startContinuous(0, 1080)

    def set_vitesse_m_s(self, vitesse_m_s):
        if vitesse_m_s > self.vitesse_max_m_s_soft :
            vitesse_m_s = self.vitesse_max_m_s_soft
        elif vitesse_m_s < -self.vitesse_max_m_s_hard :
            vitesse_m_s = -self.vitesse_max_m_s_hard
        if vitesse_m_s == 0 :
            self.pwm_prop.change_duty_cycle(self.pwm_stop_prop)
        elif vitesse_m_s > 0 :
            vitesse = vitesse_m_s * (self.delta_pwm_max_prop)/self.vitesse_max_m_s_hard
            self.pwm_prop.change_duty_cycle(self.pwm_stop_prop + self.direction_prop*(self.point_mort_prop + vitesse ))
        elif vitesse_m_s < 0 :
            vitesse = vitesse_m_s * (self.delta_pwm_max_prop)/self.vitesse_max_m_s_hard
            self.pwm_prop.change_duty_cycle(self.pwm_stop_prop - self.direction_prop*(self.point_mort_prop - vitesse ))
            
    def recule(self):
        self.set_vitesse_m_s(-self.vitesse_max_m_s_hard)
        time.sleep(0.2)
        self.set_vitesse_m_s(0)
        time.sleep(0.2)
        self.set_vitesse_m_s(-1)

    def set_direction_degre(self,angle_degre) :
        angle_pwm = self.angle_pwm_centre + self.direction * (self.angle_pwm_max - self.angle_pwm_min) * angle_degre /(2 * self.angle_degre_max )
        if angle_pwm > self.angle_pwm_max : 
            angle_pwm = self.angle_pwm_max
        if angle_pwm < self.angle_pwm_min :
            angle_pwm = self.angle_pwm_min
        self.pwm_dir.change_duty_cycle(angle_pwm)

    def stop(self):
        self.pwm_dir.stop()
        self.pwm_prop.start(self.pwm_stop_prop) 
        print("Arrêt du moteur")
        self.lidar.stop_motor()
        self.lidar.stop()
        time.sleep(1)
        self.lidar.disconnect()
        quit()
    
    def main(self):
        print("Depart")
        try : 
            while True :
                #apelle model(lidar.rDistance)
                #update 
        except KeyboardInterrupt: #récupération du CTRL+C
            vitesse_m_s = 0
            self.set_vitesse_m_s(vitesse_m_s)
            print("Fin des acquisitions")
        finally:
            self.lidar.stop()
            self.pwm_dir.stop()
            self.pwm_prop.start(self.pwm_stop_prop)            

if __name__ == '__main__' :
    try:
        wrapper = Wrapper()
        if input("Appuyez sur D pour démarrer ou tout autre touche pour quitter") in ("D","d"):
            wrapper.main()
        else:
            raise KeyboardInterrupt
        
    except KeyboardInterrupt:
        wrapper.stop()
        print("Programme arrêté par l'utilisateur")
        pass