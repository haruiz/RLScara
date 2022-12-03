#include "Servo.h"

const int MAX_NUM_COMMANDS = 10;
String commands[MAX_NUM_COMMANDS];

Servo link1, link2;

String commandText;
bool commandReceived = false;


void setup() {
  // setup servos
  Serial.begin(9600);
  Serial.setTimeout(100);
  link1.attach(8);
  link2.attach(9);
  link1.write(90);
  link2.write(90);
}

void loop() {

  // read data send to the arduino using Serial Port
  if(Serial.available()){
    commandReceived = true;
    commandText = Serial.readString();
  }
  
  // process command and update ar, location based on the angles
  if(commandReceived){
    Serial.flush();
    Serial.print(commandText);
    commandReceived = false;
    
    split(commandText, ',');
    
    int angle1 = commands[0].toInt();
    int angle2 = (180-commands[1].toInt());
    setArmCoordinates(angle1,angle2);
  }

}

void setArmCoordinates(int angle1, int angle2){
  link1.write(angle1);
  link2.write(angle2);
}


void split(String inputStr, char sep)
{
  uint8_t currSubStrIdx = 0;
  uint8_t lastSubStrIdx = 0;
  for (int i = 0; i < inputStr.length(); i++) {
    // Loop through each character and check for
    if (inputStr.charAt(i) == sep) {
      // Grab the piece from the last index up to the current position and store it
      commands[currSubStrIdx] = inputStr.substring(lastSubStrIdx, i);
      // Update the last position and add 1, so it starts from the next character
      lastSubStrIdx = i + 1;
      // Increase the position in the array that we store into
      currSubStrIdx++;
    }
    // If we're at the end of the string (no more commas to stop us)
    if (i == inputStr.length() - 1) {
      // Grab the last part of the string from the lastIndex to the end
      commands[currSubStrIdx] = inputStr.substring(lastSubStrIdx, i + 1);
    }
  }
}
