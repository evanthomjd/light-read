int enablePin = 13;   
int in1Pin = 11;  
int in2Pin = 10;
int potPin = 0;
float pos = 0;

int minPos = 0;
int maxPos = 240;

void setup() {
    pinMode(in1Pin, OUTPUT);
    pinMode(in2Pin, OUTPUT);
    pinMode(enablePin, OUTPUT);
    Serial.begin(9600);
    
    //Reposition at the start 
    hitTarget(0);
    //Wait for serial connection
    while(!Serial){}
}

void loop() {

  if(Serial.available()>0){
    int x = Serial.parseInt();
    
    int target = pos+x;
    if(target < maxPos){
      hitTarget(target);
      Serial.println((String)(maxPos - pos));
    }else {
      Serial.println("cannot move that far!");
    }

  }
}
//Drives the motor toward goal and stops when close enough.
void hitTarget(int target) {
    int threshold = 1;
    readPos();
    while (abs(pos-target)>threshold) {
        if (target > pos ) { setMotor(1, 1); }
        if (target < pos ) { setMotor(1, 0); }
        readPos();
    }
    setMotor(0,1);
}

//Takes a smoothed reading. Works ok w/o smoothing too.
void readPos() {
    float readWeight = 0.7;
    pos = (1-readWeight)*pos + readWeight*analogRead(potPin)/4;
}

void setMotor(boolean on, boolean reverse) {
    digitalWrite(enablePin, on);
    digitalWrite(in1Pin, !reverse);
    digitalWrite(in2Pin, reverse);
}
