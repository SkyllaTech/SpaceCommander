
#include "generated/master_c++11/spacecommands.hpp"
#include "generated/slave_c++11/spacecommands.hpp"
#include <iostream>

void spcmd_master::version_error(uint64_t received_hash) {
  std::cout << "Received wrong hash: " << received_hash << std::endl;
}

namespace spcmd_slave {
  send_byte_out send_byte_cb() {
    std::cout << "Send" << std::endl;
    auto out = send_byte_out{'c'};
    return out;
  }
  recv_byte_out recv_byte_cb(uint8_t b) {
    std::cout << "Recv" << std::endl;
    std::cout << int(b) << std::endl;
    return recv_byte_out{};
  }
  echo_out echo_cb(uint32_t recv) {
    std::cout << "Echo" << std::endl;
    std::cout << int(recv) << std::endl;
    auto out = echo_out{recv};
    return out;
  }
  bigtest_out bigtest_cb(uint32_t b3) {
    std::cout << "Big" << std::endl;
    return bigtest_out{};
  }
}
int main(int argc, char* argv[]) {
  spcmd_master::Master<int> test{};
  test.test_hash();
  test.send_byte('c');
  auto out = test.recv_byte();
  std::cout << out.b << std::endl;
  uint32_t a = 0;
  a |= 192ul << 24;
  a |= 168ul << 16;
  a |= 10ul << 8;
  a |= 1ul;
  auto out2 = test.echo(a);
  std::cout << out2.recv << std::endl;
  auto out3 = test.bigtest(a, 0);
  std::cout << out3.b3 << std::endl;
  std::cout << "Finished Master!" << std::endl;

  spcmd_slave::Slave<int> slave{};
  for (int i=0; i < 6; ++i) {
    std::cout << "Update " << i << std::endl;
    slave.update();
  }
  std::cout << "Finished Slave!" << std::endl;
}
