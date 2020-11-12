// ---------------------------------------------------------------- //
// Arduino Ultrasoninc Sensor HC-SR04
// Re-writed by Arbi Abdul Jabbaar
// Using Arduino IDE 1.8.7
// Using HC-SR04 Module
// Tested on 17 September 2019
// ---------------------------------------------------------------- //

#define echoPin 2 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 3 //attach pin D3 Arduino to pin Trig of HC-SR04
#define xbeePin 4
#define statPin 13

// defines variables
long duration; // variable for the duration of sound wave travel
int distance;  // variable for the distance measurement

void setup()
{
    pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
    pinMode(echoPin, INPUT);  // Sets the echoPin as an INPUT
    pinMode(xbeePin, OUTPUT);
    pinMode(statPin, OUTPUT);
    Serial.begin(9600);                               // // Serial Communication is starting with 9600 of baudrate speed
    Serial.println("Ultrasonic Sensor HC-SR04 Test"); // print some text in Serial Monitor
    Serial.println("with Arduino UNO R3");

    
    Serial.println("Unparked");
    digitalWrite(xbeePin, 0);
    digitalWrite(statPin, 0);
}

int samples[100];
int count = 0;
int pointer = 0;

int secondsToPark = 5 * 1000;

int parkEntryTime = 0;
int parked = 0;


int getDistance()
{
    // Clears the trigPin condition
    digitalWrite(trigPin, LOW);
    delayMicroseconds(4);
    
    // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH);

    // Calculating the distance
    distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)

    return distance;
}

void loop()
{
    // Store in samples array
    samples[pointer] = getDistance();

    // Keep track of the number of items we are currently sampling
    if (count < 100)
    {
        count += 1;
    }

    // increment pointer in array, wrap to 0 once we go over 99
    pointer += 1;
    if (pointer > 100)
    {
        pointer = 0;
    }

    // Calculate the average
    float avg = 0;
    for (int i = 0; i < count; i++)
    {
        avg += samples[i];
    }
    avg = avg / count;

    if (avg > 30)
    {
        if (parked == 1 || parkEntryTime != 0)
        {
            // Reset variables
            parkEntryTime = 0;
            parked = 0;

            // Signal that we are no longer parked
            Serial.println("Unparked");
            digitalWrite(xbeePin, 0);
            digitalWrite(statPin, 0);
        }
    }
    else
    {
        if (parkEntryTime == 0)
        {
            Serial.println("Starting timer");
            parkEntryTime = millis();
        }
    }

    // We are waiting for duration to elapsed before we decide the car is parked
    if (parkEntryTime != 0 && parked == 0)
    {
        int currentTime = millis();
        if ((currentTime - parkEntryTime) >= secondsToPark)
        {
            parked = 1;
            Serial.println("Parked");
            digitalWrite(xbeePin, 1);
            digitalWrite(statPin, 1);
        }
    }
}
