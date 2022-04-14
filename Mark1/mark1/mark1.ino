/*
Mark 1

The program tests capabilities of the Arduino Uno Ports.


*/

void updateOutput(int[] oPins, int[] state);
int[] separate(String s);


int led = 9;           // the PWM pin the LED is attached to
int brightness = 0;    // how bright the LED is
int fadeAmount = 5;    // how many points to fade the LED by
// initate an array of pins
int oPins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13};
int state[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
// the setup routine runs once when you press reset:
void setup() {
  // initiate the array of pins as outputs
  for (int i = 0; i < sizeof(oPins); i++) {
    pinMode(oPins[i], OUTPUT);
  }
  // initalize serial communication:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the serial port into binary state array
  state = separate(Serial.readString());
  // wait for 30 milliseconds to see the dimming effect
  delay(30);
}

// implement updateOutput so it updates array of pins output status
void updateOutput(int[] oPins, int[] state) {
  for (int i = 0; i < sizeof(oPins); i++) {
    if (state[i] == 1) {
      digitalWrite(oPins[i], HIGH);
    } else {
      digitalWrite(oPins[i], LOW);
    }
  }
}

// implement separate, to split string into array of integers
int[] separate(String s) {
  int[] a = new int[s.length()];
  for (int i = 0; i < s.length(); i++) {
    a[i] = s.charAt(i).toInt();
  }
  return a;
}
