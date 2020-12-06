
class Ultrasonic
{

public:

    Ultrasonic(int XBEEPin, int trigger_pin, int echo_pin, int detect_distance=30);

    void process();
    int  get_distance();
    void set_random_interval(int time);
    void set_park_time(int time);
    void set_stat_pin(int pin);
    void set_dummy(int timed_interval);

private:
    void process_dummy_interval();
    void process_ultrasonic();
    void set_pins();

    int m_xbee_pin;
    int m_stat_pin = -1;

    int m_trigger_pin;
    int m_echo_pin;
    int m_dummy_timed_interval = -1;
    int time_since_last_dummy_flip = -1;
    int time_since_dummy_start = -1;

    int m_park_time = 1 * 1000;

    int  m_samples[100];
    int  m_count = 0;
    int  m_pointer = 0;
    bool m_detected = false;
    int  m_park_entry_time = -1;
    int  m_detect_distance = 30;
};
