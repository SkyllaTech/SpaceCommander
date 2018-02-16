#include "generated/arduino-uno/spacecommands.hpp"

int led_pin = 13;
bool led_pin_state = false;

namespace spcmds {

void echo_callback(char in_letter, char& out_letter, char& out_double_char) {
  led_pin_state = !led_pin_state;
  digitalWrite(led_pin, led_pin_state);
  out_letter = in_letter;
  out_double_char = in_letter + 1;
}

void times2_callback(long in_x, long& out_x2) {
  out_x2 = in_x * 2;
}

void sqrt_callback(float in_x, float& out_sq_x) {
  out_sq_x = sqrt(in_x);
}

}

void setup() {
  pinMode(led_pin, OUTPUT);
  spcmds::init();
}

void loop() {
  spcmds::process_commands();
}
