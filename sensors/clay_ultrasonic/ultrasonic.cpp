#include "ultrasonic.h"

Ultrasonic::Ultrasonic(int XBEEPin, int trigger_pin, int echo_pin, int detect_distance):
    m_xbee_pin(XBEEPin),
    m_trigger_pin(trigger_pin),
    m_echo_pin(echo_pin)
    m_detect_distance(detect_distance)
{
    pinMode(m_xbee_pin,     OUTPUT);
    pinMode(m_trigger_pin,  OUTPUT);
    pinMode(m_echo_pin,     INPUT);

    set_pins();
}

Ultrasonic::set_dummy(int timed_interval)
{
    m_dummy_timed_interval = timed_interval;
}

Ultrasonic::process()
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

Ultrasonic::process_dummy_interval()
{
    if (time_since_dummy_start == -1)
    {
        time_since_dummy_start = millis();
    }

    now = millis();

    if ((now - time_since_dummy_start) > m_dummy_timed_interval)
    {
        m_detected = !m_detected;
        set_pins();
        time_since_dummy_start = millis();
    }
}

Ultrasonic::process_ultrasonic()
{
    // Store in samples array
    m_samples[m_pointer] = getDistance();

    // Keep track of the number of items we are currently sampling
    if (m_count < 100)
    {
        m_count += 1;
    }

    // increment pointer in array, wrap to 0 once we go over 99
    m_pointer += 1;
    if (m_pointer > 100)
    {
        m_pointer = 0;
    }

    // Calculate the average
    float avg = 0;
    for (int i = 0; i < count; i++)
    {
        avg += samples[i];
    }
    avg = avg / count;

    if (avg > m_detect_distance)
    {
        if (m_detected == 1 || m_park_entry_time != 0)
        {
            // Reset variables
            m_park_entry_time = 0;
            m_detected = 0;

            // Signal that we are no longer parked
            Serial.println("Unparked");
            digitalWrite(m_xbee_pin, 1);
            if (m_stat_pin != -1)
            {
                digitalWrite(statPin, 0);
            }
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
    if (m_park_entry_time != 0 && m_detected == 0)
    {
        int currentTime = millis();
        if ((currentTime - m_park_entry_time) >= m_park_time)
        {
            m_detected = 1;
            Serial.println("Parked");
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

void  Ultrasonic::set_pins(bool parked)
{
    digitalWrite(m_xbee_pin, !parked);
    if (m_stat_pin != -1)
    {
        digitalWrite(m_stat_pin, parked);
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
    duration = pulseIn(m_echo_pin, HIGH);

    // Calculating the distance
    distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)

    //Serial.println(distance);
    return distance;
}

Ultrasonic::set_random_interval(int time)
{
    m_random_interval = time;
}

Ultrasonic::set_park_time(int time)
{
    m_park_time = time * 1000;
}