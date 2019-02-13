
#include "generated/slave_arduino/spacecommands.hpp"

uint8_t bbb = 0;

namespace spcmd_slave {

send_byte_out send_byte_cb() {
  auto out = send_byte_out{bbb};
  return out;
}

recv_byte_out recv_byte_cb(uint8_t b) {
  bbb = b;
  return recv_byte_out{};
}

echo_out echo_cb(char recv_string) {
  auto out = echo_out{recv_string};
  return out;
}

void pre_write_cb() {}

void post_write_cb() {}

void pre_read_cb() {}

void post_read_cb() {}

void read_size_fail_cb() {}

void read_crc_fail_cb() {}
}


using namespace spcmd_slave;

//Slave<Uart> commander;
Slave<HardwareSerial> commander;

void setup() {
  //commander = Slave<Uart>(Serial);
  commander = Slave<HardwareSerial>(Serial);
  commander.begin();
}

void loop() {
  commander.update();
}
