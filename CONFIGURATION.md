# Configuration Details

The following is a description of the `commands.yaml` file. It is important to have a space between a parameter and the value, i.e. use `name: echo` instead of `name:echo`. The dash (`-`) is used for elements in an array. Please see the [YAML spec](http://www.yaml.org/spec/1.2/spec.html#id2797382) for more details.

## connection:
> Required

### type: \<connection-type\>
> Required

Available options:
 - `serial` : used for Serial UART connections.

### speed: \<connection-speed\>
> Required

Use a baudrate available on your platform. Typical values are: 9600, 19200, 38400, 57600, 115200. Please review the datasheet for your devices to determine an appropriate value.

### parity: \<connection-parity\>
> Optional

The parity to be used for byte level parity checking within UART.

Available options:
  - `none`: No parity bit.
  - `even`: Even parity bit.
  - `odd`: Odd parity bit.

### crc: \<connection-crc\>
> Optional

CRC checking to be done on the full received packet. Note, CRC calculations are not very cheap, and could cause bottlenecks on low power embedded systems. CRC calculations also use external libraries for calculations, these are automatically included with SpaceCommander if the CRC option is used.

Available options:
  - `none`: No CRC performed.
  - `crc-8`: 8 bits (1 byte) CRC.
  - `crc-16`: 16 bits (2 byte) CRC.
  - `crc-32`: 32 bits (4 byte) CRC.

CRC Libraries:
  - 'arduino-*': [FastCRC](https://github.com/FrankBoesing/FastCRC)
  - 'python3': [crcmod](https://pypi.org/project/crcmod/)

## heartbeat: 
> Optional

Optional setting to have the master send heartbeat packets to the slave. This increments a counter on the master and slave, and can be used to detect a loss of connection to the slave.

### interval: \<heartbeat-interval\>
> Required

Interval on which to send heartbeat packets, in milliseconds.

### count: \<heartbeat-count\> 
> Required

Number of heartbeat packets that can be missed before an error is raised.

### size: \<heartbeat-size\>
> Required

Size of the counter for heartbeat packets before it resets.

Available options:
  - `uint8`: 8 bit counter
  - `uint16`: 16 bit counter
  - `uint32`: 32 bit counter
  - `uint64`: 64 bit counter

## master:
> Required
 
### type: \<master-type\>
> Required

Currently available options:
 - `arduino-arm` : For ARM based Arduino master devices.
 - `arduino-avr` : For AVR based Arduino master devices.
 - `python` : For Python3 based master devices.
 
### timeout: \<master-timeout\>
> Optional

Connection timeout for the master in milliseconds. If a slave device does not respond to the master within the timeout period, the master will assume that an error has occurred, and can react appropriately.

## slave:
> Required

At least one slave device for the connection is required, but multiple can be specified to generate slave code for multiple types of device.

_Array_

### type: \<slave-type\>
> Required

Currently available options:
 - `arduino-arm` : For ARM based Arduino slave devices.
 - `arduino-avr` : For AVR based Arduino slave devices.
 - `python` : For Python3 based slave devices.

### timeout: \<slave-timeout\>
> Required

Connection timeout for slave in milliseconds. If the slave device expects to be receiving data but does not for the length of the timeout, it quits attempting to read from the connection and raises an error.

## commands:
> Required


Commands which are to be generated. There must be at least one command.

_Array_

### name: \<command-name\>
> Required

Name of the command

### description: \<command-description\>
> Optional

Human readable documentation of the command.

### inputs:
> Optional

Input arguments for the command.

_Array_

##### name: \<input-name\>
> Required

Name of the input argument.

##### type: \<input-type\>
> Required

Type of the input argument.

##### description: \<input-description\>
> Optional

Description of the input argument.

### outputs:
> Optional

Output arguments for the command.

_Array_

##### name: \<output-name\>
> Required

Name of the output argument.

##### type: \<output-type\>
> Required

Type of the output argument.

##### description: \<output-description\>
> Optional

Description of the output argument.

## Data Types

Types can have different meaning in different languages and on different platforms, so unified names for distinct data types are provided for specifying the type in SpaceCommander.

Currently supported options are:

| Type     | Description             | C++ (x86_64)                                | C++ (AVR)                                    | C++ (ARM 32-Bit)                            | Python3 equivalent |
|----------|-------------------------|---------------------------------------------|----------------------------------------------|---------------------------------------------|--------------------|
| `char`   | 8 bit character         | `char`                                      | `char`                                       | `char`                                      | `char`             |
| `int8`   | 8 bit signed integer    | `int8_t`, `char`                            | `int8_t`, `char`                             | `int8_t`, `signed char`                     | `int`              |
| `uint8`  | 8 bit unsigned integer  | `uint8_t`, `unsigned char`                  | `uint8_t`, `unsigned char`                   | `uint8_t`, `char`                           | `int`              |
| `int16`  | 16 bit signed integer   | `int16_t`, `short`                          | `int16_t`, `short`, `int`                    | `int16_t`, `short`                          | `int`              |
| `uint16` | 16 bit unsigned integer | `uint16_t`, `unsigned short`                | `uint16_t`, `unsigned short`, `unsigned int` | `uint16_t`, `unsigned short`                | `int`              |
| `int32`  | 32 bit signed integer   | `int32_t`, `int`, `long`                    | `int32_t`, `long`                            | `int32_t`, `int`, `long`                    | `int`              |
| `uint32` | 32 bit unsigned integer | `uint32_t`, `unsigned int`, `unsigned long` | `uint32_t`, `unsigned long`                  | `uint32_t`, `unsigned int`, `unsigned long` | `int`              |
| `int64`  | 64 bit signed integer   | `int64_t`, `long long`                      | `int64_t`, `long long`                       | `int64_t`, `long long`                      | `int`              |
| `uint64` | 64 bit unsigned integer | `uint64_t`, `unsigned long long`            | `uint64_t`, `unsigned long long`             | `uint64_t`, `unsigned long long`            | `int`              |
| `float`  | 32 bit float            | `float`                                     | `float`                                      | `float`                                     | `float`            |
| `string` | string                  | string                                      | string                                       | string                                      | string             |

### Example Configuration


The following is an example configuration that uses a serial UART connection from a python3 host computer to an arduino-avr slave device. It sends a heartbeat message to the slave once a second, and will raise an error if 5 heartbeat messages fail. 

```yaml
connection:
    type: serial
    speed: 9600

heartbeat:
    interval: 1000
    count: 5

master:
    type: python3
    timeout: 1000

slave:
    type: arduino-avr
    timeout: 1000

commands:
    - name: send_byte
      description: Send a byte to the slave
      inputs:
          - name: b
            type: uint8_t
            description: Byte to be sent
    - name: recv_byte
      description: Receive a byte from the slave
      outputs:
          - name: b
            type: uint8_t
            description: Received byte
    - name: echo
      description: Send string to slave and read it back
      inputs:
          - name: send_string
            type: string
      outputs:
          - name: recv_string
            type: string
```
