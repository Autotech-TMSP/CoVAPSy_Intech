#include <Servo.h>
#include <EnableInterrupt.h>


#define PIN_DIR 10
#define PIN_MOT 9
#define PIN_FOURCHE 14


Servo moteur;
Servo direction;



//declaration des broches des differents composants
const int pinMoteur=PIN_MOT;
const int pinDirection=PIN_DIR;
const int pinFourche=PIN_FOURCHE;

//constantes utiles
const int nb_trous=16*2; //nb de trous dans la roue qui tourne devant la fourche optique
const int distanceUnTour=79; //distance parcourue par la voiture apres un tour de roue en mm

//variables
char command;
float Vcons=0; //consigne
float vitesse=0; //vitesse de la voiture

//PID
float ecart=0;
float vieuxEcart=0;
float vieuxTemps=0; //variable utilisee pour mesurer le temps qui passe
float Kp=0.05; //correction prop
float Ki=0.1; //correction integrale
float Kd=0.; //correction derivee
float integral=0;//valeur de l'integrale dans le PID
float derivee=0; //valeur de la derivee dans le PID

//mesures
volatile int count=0; //variable utilisee pour compter le nombre de fronts montants/descendants
volatile int vieuxCount=0; //stocke l'ancienne valeur de count pour ensuite faire la difference
volatile byte state=LOW;
float mesures[10]; // tableau de mesures pour lisser

float getMeanSpeed(float dt){
  int length = sizeof(mesures)/sizeof(mesures[0]);
  //ajout d'une nouvelle mesure et suppression de l'ancienne
  for (int i=length-1;i>0;i--){
      mesures[i]=mesures[i-1];
  }
  mesures[0] = getSpeed(dt);

  //Calcul d'une moyenne pour lisser les mesures qui sont trop dipersées sinon
  float sum=0;
  for (int i=0;i<length;i++){
    sum+=mesures[i];
  }

  #if 0
  for(int i=0;i<length;i++){
    Serial.print(mesures[i]);
    Serial.print(" , ");
  }
  Serial.println(sum/length);
  #endif


  return sum/length;
}
float getSpeed(float dt){  
  int N = count - vieuxCount; //nombre de fronts montant et descendands après chaque loop
  float V = ((float)N/(float)nb_trous)*distanceUnTour/(dt*1e-3); //16 increments -> 1 tour de la roue et 1 tour de roue = 79 mm 
  vieuxCount=count;
  vieuxTemps=millis();
  /*Serial.print(count+" ");
  Serial.print(vieuxCount+" ");
  Serial.print(N+" ");
  Serial.println((int)V+" ");*/
  return V;
}
void blink(){ //on compte tous les fronts
  //Serial.print(count);
  count++;
}
float PID(float cons,float mes,float dt){
  float e = cons - mes;
  
  //Terme Proportionel
  float P = Kp*e;
  
  // Terme Intégral
  integral=integral + e*dt;
  float I= Ki*integral;
  
  #if 0
  //terme dérivé
  derivee =(e-vieuxEcart)/dt;
  vieuxEcart=e;
  float D=Kd*derivee;
  #endif

  return P + I;
}
void setup() {
  Serial.begin(115200);

  pinMode(pinMoteur,OUTPUT);
  moteur.attach(pinMoteur,0,2000);

  pinMode(pinDirection,OUTPUT);
  direction.attach(pinDirection,0,2000);
  
  pinMode(pinFourche,INPUT_PULLUP);
  enableInterrupt(PIN_FOURCHE, blink, CHANGE); //on regarde a chaque fois que le signal de la fourche change (Montants et Descendants)

  moteur.writeMicroseconds(1500);
  delay(2000);
  moteur.writeMicroseconds(1590);


  delay(10);
  Serial.println("init");
}
void loop() {
  // Commandes pour debugger
  command=Serial.read();
  switch (command){ //pour regler les parametres
    case 'a':
    Vcons+=200;
    break;
    case 'z':
    Vcons-=50;
    break;
    case 'q':
    Vcons=0;
    break;
    case 'i':
    Ki+=0.01;
    break;
    case 'k':
    Ki-=0.01;
    break;
    case 'u':
    Kp+=0.01;
    break;
    case 'j':
    Kp-=0.01;
    break;
  }
  int deltaT = millis()-vieuxTemps; //temps qui est passé pendant un loop (en millisecondes)
  vitesse=getMeanSpeed(deltaT); // on recup la vitesse lissée

  int out = PID(Vcons,vitesse,float(deltaT)/1e3);
  moteur.writeMicroseconds(constrain(1500 + out,1500,2000));

  //print debug
  #if 1
  Serial.print("");
  Serial.print(Vcons);
  Serial.print(", ");
  Serial.print(vitesse);
  Serial.print(", ");
  Serial.print(Ki);
  Serial.print(", ");
  Serial.print(Kp);
  Serial.print(", ");
  Serial.print("out=");
  Serial.println(out);
  #endif
  delay(10);
}
