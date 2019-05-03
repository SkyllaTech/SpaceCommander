# SpaceCommander

Simplify robust serial communication, mainly to facillitate communication between computers and microcontrollers.
This is meant to replace the ad-hoc communication often used for sending commands from a computer to a microcontroller.

## Installation

SpaceCommander uses Python3 Mako templates for generating the code.

``` shell
pip3 install mako
```

If you plan to use any CRC messages, the CRC library used must also be installed:

``` shell
pip3 install crcmod
```
    
### Linux

Add <spacecommander>/bin to the system path

### Windows

<TODO>

## Usage

SpaceCommander reads in a specified commands file in the YAML format, and produces communication code for the specified master and slave types from the commands file.
These are placed in the `generated` folder in the directory SpaceCommander is run from.

## Protocol

See the [Protocol](PROTOCOL.md) document for an in depth description of the protocol used by SpaceCommander. 

## Commands Configuration

SpaceCommander uses a YAML format file to specify parameters for the connection, the master type, the slave type, and command list.
More details for the format of this document can be found [here](CONFIGURATION.md).

## Templates

Custom templates can be created for other languages and platforms. These templates are written using [Mako](http://www.makotemplates.org/). Templates should be named `<filename>.spcmd` and placed in `<spacecommand-dir>/templates/<platform>/<master|slave>`.

## Supported Features

Currently implemented masters:
  * Python3
  * Python2
  * Arduino

Currently implemented slaves:
  * Python3
  * Arduino

Currently implemented features:
  * Automatic CRC generation for messages
  * Timeout support 
  * Packet framing
  * Configuration hash checking

Planned features:
  * Background heartbeat messages
  * Packet sequence numbers
  * Fixed length array support
  * String support
