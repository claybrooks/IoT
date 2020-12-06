// ---------------------------------------------------------------- //
// Arduino Ultrasoninc Sensor HC-SR04
// Re-writed by Arbi Abdul Jabbaar
// Using Arduino IDE 1.8.7
// Using HC-SR04 Module
// Tested on 17 September 2019
// ---------------------------------------------------------------- //

#include "ultrasonic.h"

#define NUM_U 4

//xbee pin, trigger pin, echo pin, distance
Ultrasonic u1 = Ultrasonic(4, 3, 2, 30);
Ultrasonic u2 = Ultrasonic(4, 3, 2, 40);
Ultrasonic u3 = Ultrasonic(4, 3, 2, 50);
Ultrasonic u4 = Ultrasonic(4, 3, 2, 60);

Ultrasonic u[NUM_U];

void setup()
{
    Serial.begin(9600);                               // // Serial Communication is starting with 9600 of baudrate speed
    Serial.println("Ultrasonic Sensor HC-SR04 Test"); // print some text in Serial Monitor
    Serial.println("with Arduino UNO R3");

    int i = 0;
    u[i++] = &u1;
    u[i++] = &u2;
    u[i++] = &u3;
    u[i++] = &u4;

    u1.set_stat_pin(13);
}

void loop()
{
    for (int i = 0; i < NUM_U; ++i)
    {
        u[i].process();
    }

    delay(1000);
}
