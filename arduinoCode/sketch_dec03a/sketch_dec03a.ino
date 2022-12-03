#include "Servo.h"
Servo link1, link2;


void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);
  link1.attach(8);
  link2.attach(9);
  link1.write(90);
  link2.write(90);
}
String actions;
bool commandReceived = false;

void loop() {

   
  if(Serial.available()>0){
    commandReceived = true;
    actions = Serial.readString();
    Serial.flush();
  }
  
  if(commandReceived)
  {
    //delay(100);
    Serial.print(actions);
    commandReceived = false;
    split_string(actions);
    
  }
  
}


void split_string(String input)
{
  String pieces[10];
  uint8_t counter = 0;
  uint8_t last_index = 0;
  for (int i = 0; i < input.length(); i++) {
    // Loop through each character and check if it's a comma
    if (input.substring(i, i + 1) == ",") {
      // Grab the piece from the last index up to the current position and store it
      pieces[counter] = input.substring(last_index, i);
      // Update the last position and add 1, so it starts from the next character
      last_index = i + 1;
      // Increase the position in the array that we store into
      counter++;
    }
    // If we're at the end of the string (no more commas to stop us)
    if (i == input.length() - 1) {
      // Grab the last part of the string from the lastIndex to the end
      pieces[counter] = input.substring(last_index, i + 1);
      //counter++;
    }
  }

  int angle1 = pieces[0].toInt();
  link1.write(angle1);
  int angle2 = (180-pieces[1].toInt());
  link2.write(angle2);
}
