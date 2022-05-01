int val;
int tempPin = A0;
int ldrPin = A1;
int value;
int x;
int y;
int z;
char str[20];
void setup()
{
  Serial.begin(9600);
  pinMode(3, OUTPUT);

}
void loop()
{
  Serial.flush();
  val = analogRead(tempPin); // I have ZERO IDEA why, but if I delete this line the ADC gives wrong values
//  Serial.println(val);
  Serial.println( String(analogRead(ldrPin)) + "," + String(analogRead(tempPin)));
  Serial.flush();
//  Serial.println( analogRead(ldrPin));
//  Serial.flush();
//  Serial.println(analogRead(tempPin));

  if (Serial.available() > 0)
  {
    x = Serial.parseInt();
    y = Serial.parseInt();
    z = Serial.parseInt();
  }
  digitalWrite(3, x);
  digitalWrite(4, y);
  digitalWrite(5, z);
  delay(500);
  
}
