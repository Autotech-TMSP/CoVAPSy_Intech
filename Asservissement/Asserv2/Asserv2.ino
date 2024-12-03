#include <Servo.h>

Servo moteur;
Servo direction;


//declaration des broches des differents composants
const int pinMoteur=10;
const int pinDirection=A0;
const int pinFourche=3;

//constantes utiles
const int nb_trous=16*2; //nb de trous dans la roue qui tourne devant la fourche optique
const int distanceUnTour=79; //distance parcourue par la voiture apres un tour de roue en mm

//variables
char command;
float Vcons=1000; //consigne
float vitesse=0; //vitesse de la voiture
float ecart=0;
float vieuxEcart=0;
float vieuxTemps=0; //variable utilisee pour mesurer le temps qui passe
float Kp=0.05; //correction prop
float Ki=0; //correction integrale
float Kd=0.; //correction derivee
float integral=0;//valeur de l'integrale dans le PID
float derivee=0; //valeur de la derivee dans le PID
volatile int count=0; //variable utilisee pour compter le nombre de fronts montants/descendants
volatile int vieuxCount=0; //stocke l'ancienne valeur de count pour ensuite faire la difference
volatile byte state=LOW;





float getSpeed(float dt){
  int N = count - vieuxCount; //nombre de fronts montant et descendands après chaque loop
  float V = ((float)N/(float)nb_trous)*distanceUnTour/(dt*1e-3); //16 increments -> 1 tour de la roue et 1 tour de roue = 79 mm 
  vieuxCount=count;
  vieuxTemps=millis();
  return V;
}

void blink(){ //on compte tous les fronts
  count++;
}


float PID(float cons,float V,float dt){
  float e = cons - V;
  float P = Kp*e;
  integral=constrain(integral + e*dt,-500,500); //on sature pour que l'integrale ne diverge pas
  float I= Ki*integral;
  derivee =(e-vieuxEcart)/dt;
  vieuxEcart=e;
  float D=Kd*derivee;
  return P + I + D;
}

void setup() {
  Serial.begin(115200);

  pinMode(pinMoteur,OUTPUT);
  moteur.attach(pinMoteur,0,2000);

  pinMode(pinDirection,OUTPUT);
  direction.attach(pinDirection,0,2000);
  pinMode(pinFourche,INPUT_PULLUP);

  moteur.writeMicroseconds(1500);
  delay(2000);

  delay(10);
  Serial.println("test");

  attachInterrupt(1,blink,CHANGE); //on regarde a chaque fois que le signal de la fourhce change (Montants et Descendants)

}




void loop() {
  
  command=Serial.read();
  switch (command){ //pour regler Vcons
    case 'a':
    Vcons+=100;
    break;
    case 'z':
    Vcons-=100;
    break;
    case 'q':
    Vcons=0;
    break;
  }
  int deltaT = millis()-vieuxTemps; //temps qui est passé pendant un loop (en millisecondes)
  vitesse=getSpeed(deltaT);

  int out = constrain(PID(Vcons,vitesse,deltaT) + 1500, 1500, 1650);
  moteur.writeMicroseconds(out);

  Serial.print("");
  Serial.print(Vcons);
  Serial.print(", ");
  Serial.print("");
  Serial.print(vitesse);
  Serial.print("out=");
  Serial.println(out);
  delay(5);
}
