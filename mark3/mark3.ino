// init array of int representing pin states
int oPins[12] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13};
int state[12] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};


void initPins(int* oPins){
    for (int i = 0; i < sizeof(oPins); i++) {
        pinMode(oPins[i], OUTPUT);
        digitalWrite(oPins[i], LOW);
    }
}
void serialState(){
    for (int i = 0; i < 12; i++) {
        Serial.print(state[i]);
    }
    Serial.println();
}

void setOutput(){
    for (int i = 0; i < 12; i++) {
        if (state[i] == '0') {
            digitalWrite(oPins[i], 0);
        } else {
            digitalWrite(oPins[i], 1);
        }
    }
}

void setup(){
    // call initPins to set all pins to output and set all pins to LOW
    initPins(oPins);
    // init serial communication
    Serial.begin(9600);
}

void loop(){
    // send back the state of the pins as a whole
    serialState();
    Serial.flush();
    Serial.println(Serial.parseInt());
    // read the serial port into binary state array
    String s = (String)Serial.parseInt();
    for (int i = 0; i < 12; i++) {
        state[i] = s.charAt(i);
    }
    Serial.println(sizeof(state));
    Serial.println(1);
    // update the state of the pins
    setOutput();
    // wait for 30 milliseconds to see the dimming effect
    delay(30);
}
