typedef struct {
    int pinNum;
    int pinVal;
} pinInit_t;

pinInit_t oPins[] {
    {2, LOW},
    {3, LOW},
    {4, LOW},
    {5, LOW},
    {6, LOW},
    {7, LOW},
    {8, LOW},
    {9, LOW},
    {10, LOW},
    {11, LOW},
    {12, LOW},
    {13, LOW}
};
void initPins(pinInit_t *pins, int numPins) {
    for (int i = 0; i < numPins; i++) {
        pinMode(pins[i].pinNum, OUTPUT);
        digitalWrite(pins[i].pinNum, pins[i].pinVal);
    }
}
pinInit_t* separator(String s) {
    pinInit_t* a = new pinInit_t[s.length()];
    for (int i = 0; i < s.length(); i++) {
        a[i].pinNum = s.charAt(i);
        a[i].pinVal = s.charAt(i);
    }
    return a;
}

void setup() {
  // initiate the array of pins as outputs
  uint8_t i;
  initPins(oPins, sizeof(oPins));
  // initalize serial communication:
  Serial.begin(9600);
}

void loop() {
    // read the serial port into binary state array
    uint8_t i;
    pinInit_t* a = (pinInit_t) malloc(sizeof(oPins));
    a = separator(Serial.readString());
    pinInit_t[] x;
    // send back a message
    Serial.print("Received: ");
    Serial.println(sizeof(oPins));
    Serial.println(sizeof(x));
    Serial.println(sizeof(int));
    for( i = 0; i < sizeof(a)/sizeof(pinInit_t); ++i ){
        Serial.print(a[i].pinNum);
        Serial.print(a[i].pinVal);
    }
    // wait for 30 milliseconds to see the dimming effect
    delay(30);
}
