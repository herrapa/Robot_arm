#include <Servo.h> 
 
Servo servoBase;
Servo servoShoulder;
Servo servoElbow;

typedef struct ServoData_t{
  uint16_t base;
  uint16_t shoulder;
  uint16_t elbow;
};

typedef union ServoPacket_t{
  ServoData_t servoData;
  uint8_t dataPacket[sizeof(ServoData_t)];
};

ServoPacket_t servoPacket;
 
void setup() 
{ 
  servoBase.attach(9, 800, 2000);
  servoShoulder.attach(10, 820, 2150);
  servoElbow.attach(11, 830, 2200);

  servoPacket.servoData.base = 1370;
  servoPacket.servoData.shoulder = 1500;
  servoPacket.servoData.elbow = 1200;
  
  Serial.begin(115200);
} 
 
void loop() 
{ 
  if (Serial.available() >= sizeof(ServoData_t))
  {
    for (int i = 0; i < sizeof(ServoData_t); ++i)
    {
      servoPacket.dataPacket[i] = Serial.read();
    }
  }
  
  servoBase.writeMicroseconds(servoPacket.servoData.base); // center ~1370
  servoShoulder.writeMicroseconds(servoPacket.servoData.shoulder);
  servoElbow.writeMicroseconds(servoPacket.servoData.elbow);
} 

