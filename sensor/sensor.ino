// ---------------------------------------------------------------- //
// Arduino Ultrasoninc Sensor HC-SR04
// Re-writed by Arbi Abdul Jabbaar
// Using Arduino IDE 1.8.7
// Using HC-SR04 Module
// Tested on 17 September 2019
// ---------------------------------------------------------------- //

#include "ultrasonic.h"

#define NUM_U 2
#define STATUS_PIN 13

//xbee pin, trigger pin, echo pin, distance
Ultrasonic u1 = Ultrasonic(4, 2,  3);
Ultrasonic u2 = Ultrasonic(7, 6,  5);

Ultrasonic* u[NUM_U];

void setup()
{
    Serial.begin(9600);                               // // Serial Communication is starting with 9600 of baudrate speed
    Serial.println("Ultrasonic Sensor HC-SR04 Test"); // print some text in Serial Monitor
    Serial.println("with Arduino UNO R3");
    pinMode(STATUS_PIN, OUTPUT);

    int i = 0;
    u[i++] = &u1;
    u[i++] = &u2;
}

void loop()
{
    int parked = 0;
    for (int i = 0; i < NUM_U; ++i)
    {
        u[i]->process();
        parked |= u[i]->get_detected();
    }

    digitalWrite(STATUS_PIN, parked);
}
