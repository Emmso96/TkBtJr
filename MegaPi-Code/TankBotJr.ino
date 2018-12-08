#include "MeMegaPi.h"
#include "Wire.h"
MeEncoderOnBoard Encoder_1(SLOT1);
MeEncoderOnBoard Encoder_2(SLOT2);

MeMegaPiDCMotor motor1(PORT2B);
MeUltrasonicSensor ultraSensor(PORT_7); /* Ultrasonic module can ONLY be connected to port 3, 4, 6, 7, 8 of base shield. */
MeMegaPiDCMotor motor2(PORT1B);

uint8_t motorSpeed = 100;

void isr_process_encoder1(void)
{
  if (digitalRead(Encoder_1.getPortB()) == 0)
  {
    Encoder_1.pulsePosMinus();
  }
  else
  {
    Encoder_1.pulsePosPlus();;
  }
}

void isr_process_encoder2(void)
{
  if (digitalRead(Encoder_2.getPortB()) == 0)
  {
    Encoder_2.pulsePosMinus();
  }
  else
  {
    Encoder_2.pulsePosPlus();
  }
}

void Motor_Ctrl(char A)
{
  char a = A;
  switch (a)
  {
    case '0':
      Encoder_1.runSpeed(0);
      Encoder_2.runSpeed(0);
      break;
    case '1':
      // Slow FWD
      Encoder_1.runSpeed(100);
      Encoder_2.runSpeed(-100);
      break;
    case '2':
      // Fast FWD
      Encoder_1.runSpeed(200);
      Encoder_2.runSpeed(-200);
      break;
    case '3':
      // Right Turn
      Encoder_1.runSpeed(-200);
      Encoder_2.runSpeed(-200);
      break;
    case '4':
      // Slow BWD
      Encoder_1.runSpeed(-100);
      Encoder_2.runSpeed(100);
      break;
    case '5':
      //Fast BWD
      Encoder_1.runSpeed(-200);
      Encoder_2.runSpeed(200);
      break;
    case '6':
      // Left Turn
      Encoder_1.runSpeed(200);
      Encoder_2.runSpeed(200);
      break;
    default:
      // Stop
      Encoder_1.runSpeed(0);
      Encoder_2.runSpeed(0);
      break;
  }
}

void setup()
{
  attachInterrupt(Encoder_1.getIntNum(), isr_process_encoder1, RISING);
  attachInterrupt(Encoder_2.getIntNum(), isr_process_encoder2, RISING);
  Serial.begin(115200);

  //Set PWM 8KHz
  TCCR1A = _BV(WGM10);
  TCCR1B = _BV(CS11) | _BV(WGM12);

  TCCR2A = _BV(WGM21) | _BV(WGM20);
  TCCR2B = _BV(CS21);

  Encoder_1.setPulse(7);
  Encoder_2.setPulse(7);
  Encoder_1.setRatio(26.9);
  Encoder_2.setRatio(26.9);
  Encoder_1.setPosPid(1.8, 0, 0);
  Encoder_2.setPosPid(1.8, 0, 0);
  Encoder_1.setSpeedPid(1, 0, 0);
  Encoder_2.setSpeedPid(1, 0, 0);
}

void loop()
{
  motor1.run(motorSpeed); /* value: between -255 and 255. */
  motor2.run(-motorSpeed); /* value: between -255 and 255. */
  Encoder_1.loop();
  Encoder_2.loop();

  int Dist = ultraSensor.distanceCm();
  Serial.print("Distance : ");
  Serial.print(Dist);
  Serial.println(" cm");
  delay(100); /* the minimal measure interval is 100 milliseconds */
  
  if (abs(Dist) >= 100)
  {
    //fast fowrard
    Motor_Ctrl('2');
    Encoder_1.loop();
    Encoder_2.loop();
  }
  if (abs(Dist) >= 80)
  {
    //fast fowrard
    Motor_Ctrl('1');
    Encoder_1.loop();
    Encoder_2.loop();
  }
  if (Dist < 80 && Dist > 60)
  {
    //Happy Zone
    Motor_Ctrl('0');
    Encoder_1.loop();
    Encoder_2.loop();
  }
  if (Dist < 60 && Dist > 40)
  {
    //Back Slow
    Motor_Ctrl('4');
    Encoder_1.loop();
    Encoder_2.loop();
  }
    if (Dist < 40)
  {
    //Back Fast
    Motor_Ctrl('5');
    Encoder_1.loop();
    Encoder_2.loop();
  }
}
