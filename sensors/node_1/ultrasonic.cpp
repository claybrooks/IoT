#include "ultrasonic.h"

#include <Arduino.h>

Ultrasonic::Ultrasonic(int XBEEPin, int trigger_pin, int echo_pin, int park_time, int detect_distance):
    m_xbee_pin(XBEEPin),
    m_trigger_pin(trigger_pin),
    m_echo_pin(echo_pin),
    m_detect_distance(detect_distance),
    m_park_time(park_time)
{
    pinMode(m_xbee_pin,     OUTPUT);
    pinMode(m_trigger_pin,  OUTPUT);
    pinMode(m_echo_pin,     INPUT);
}

void Ultrasonic::set_dummy(int timed_interval)
{
    m_dummy_timed_interval = timed_interval;
}

void Ultrasonic::process()
{
    if (m_dummy_timed_interval > 0)
    {
        process_dummy_interval();
    }
    else
    {
        process_ultrasonic();
    }
}

void Ultrasonic::process_dummy_interval()
{
    if (time_since_dummy_start == -1)
    {
        time_since_dummy_start = millis();
    }

    int now = millis();

    if ((now - time_since_dummy_start) > m_dummy_timed_interval)
    {
        m_detected = !m_detected;
        set_pins();
        time_since_dummy_start = millis();
    }
}

void Ultrasonic::process_ultrasonic()
{
    // Store in samples array
    m_samples[m_pointer] = get_distance();

    //Serial.print(m_xbee_pin);
    //Serial.print("=");
    //Serial.println(m_samples[m_pointer]);
    
    // Keep track of the number of items we are currently sampling
    if (m_count < 100)
    {
        m_count += 1;
    }

    // increment pointer in array, wrap to 0 once we go over 99
    m_pointer += 1;
    if (m_pointer >= 100)
    {
        m_pointer = 0;
    }

    // Calculate the average
    float avg = 0;
    for (int i = 0; i < m_count; i++)
    {
        avg += m_samples[i];
    }
    avg = avg / (float)m_count;

    if (avg > m_detect_distance)
    {
        if (m_detected == 1 || m_park_entry_time != 0)
        {
            // Reset variables
            m_park_entry_time = 0;
            m_detected = 0;

            // Signal that we are no longer parked
            Serial.println("Unparked");
            set_pins();
        }
    }
    else
    {
        if (m_park_entry_time == 0)
        {
            Serial.println("Starting timer");
            m_park_entry_time = millis();
        }
    }

    // We are waiting for duration to elapsed before we decide the car is parked
    if (m_park_entry_time != 0 && !m_detected)
    {
        int currentTime = millis();
        
        if ((currentTime - m_park_entry_time) >= m_park_time)
        {
            m_detected = 1;
            Serial.println("Parked");
            set_pins();
        }
    }
}

void Ultrasonic::set_stat_pin(int pin)
{
    m_stat_pin = pin;
    if (m_stat_pin != -1)
    {
        pinMode(m_stat_pin, OUTPUT);
    }
}

void  Ultrasonic::set_pins()
{
    Serial.print("XBEE ");
    Serial.print(m_xbee_pin);
    Serial.print("=");
    Serial.println(m_detected);

    digitalWrite(m_xbee_pin, !m_detected);
    if (m_stat_pin != -1)
    {
        digitalWrite(m_stat_pin, m_detected);
    }
}

int Ultrasonic::get_distance()
{
    // Clears the trigPin condition
    digitalWrite(m_trigger_pin, LOW);
    delayMicroseconds(4);

    // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
    digitalWrite(m_trigger_pin, HIGH);
    delayMicroseconds(10);
    digitalWrite(m_trigger_pin, LOW);

    // Reads the echoPin, returns the sound wave travel time in microseconds
    float duration = pulseIn(m_echo_pin, HIGH);

    // Calculating the distance
    float distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)

    //Serial.println(distance);
    return distance;
}

void Ultrasonic::set_random_interval(int time)
{
    m_dummy_timed_interval = time;
}

void Ultrasonic::set_park_time(int time)
{
    m_park_time = time * 1000;
}

int Ultrasonic::get_detected()
{
    return m_detected;
}
