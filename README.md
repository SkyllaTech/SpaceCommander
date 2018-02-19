# SpaceCommander

Simplify communication between computers and microcontrollers.

Currently supported microcontrollers:

- Arduino series
 
Currently supported host languages:

 - Python3

## Installation

Please [install Python3 first](https://www.python.org/downloads/).

Then, run

    pip install mako
    
### Linux

Add <spacecommander>/bin to the system path

### Windows

<TODO>

## Usage

Run `spacecommander` in a project folder. The directory must have a `commands.yaml` file to be valid.

## commands.yaml Configuration

A `commands.yaml` file must exist in the parent directory of where the generated files should be located.

Files are generated to:
`<root>/generated/<platform>/`

### Structure

The following is the general structure of a `commands.yaml` file. Proper indentation is important, along with the space between a parameter and the value. Ie, use `name: echo` instead of `name:echo`. The dash (`-`) is used for elements in an array. Please see the [YAML spec](http://www.yaml.org/spec/1.2/spec.html#id2797382) for more details.

```yaml
device: # required
  type: <device-type>  # required
  baudrate: <integer>  # required
  
host: # optional
  type: <host-language>  # required
  timeout: <float>  # optional
  
commands: # required
  - name: <command-name>  # required
    host: <command-host>  # required
    description: <command-description>  # optional
    inputs:  # optional
      - name: <arg-name>  # required
        type: <arg-type>  # required
        description: <arg-description>  # optional
        ...
      - name: <arg-name>  # required
        type: <arg-type>  # required
        description: <arg-description>  # optional
    outputs:  # optional
      - name: <arg-name>  # required
        type: <arg-type>  # required
        description: <arg-description>  # optional
    ...
  - name: <command-name>
    host: <command-host>
      ...
```

---

#### device
> Required

Used for configuring the target device.

##### type <device-type>
> Required

Currently available options:
 - `arduino-uno` : used for Arduino platforms.

##### baudrate
> Required

Use a baudrate available on your platform. Typical values are: 9600, 19200, 38400, 57600, 115200. Please review the datasheet for your device to determine an appropriate value.

---

#### host
> Optional

Used for configuring the host language (ie the computer that the microcontroller is plugged into).

 
##### type <host-language>
> Required

Currently available options:
 - `python` : generates Python3 code
 
##### timeout
> Required

Timeout for commands from microcontroller. These are application specific. If microcontroller code takes a longer duration to execute, then this value may need to be increased. However, generally speaking, device callbacks should be short to prevent lockups.

---

#### commands
> Required

Array of commands which are to be generated. There must be at least one command.

Each command contains:

##### name <command-name>
> Required

Name of the command

##### host <command-host>
> Required

The host of the command. Currently, `device` is the only option that is supported.

##### description
> Optional

Human readable documentation of the command.

##### inputs/outputs
> Optional

Input and output arguments for the command.

###### name <arg-name>
> Required

name of the argument

###### type <arg-type>
> Required

The type of the parameter.

Currently supported options are:

| Type     | Description             | c++ equivalent                                             | python equivalent |
|----------|-------------------------|------------------------------------------------------------|-------------------    |
| `char`   | character               | `char`                                                     | `char`            |
| `int8`   | 8 bit signed integer    | `int8_t`, `char`                                           | `int`             |
| `uint8`  | 8 bit unsigned integer  | `uint8_t`, `unsigned char`                                 | `int`             |
| `int32`  | 32 bit signed integer   | `int32_t`, `int` (x86_64), `long` (avr)                    | `int`             |
| `uint32` | 32 bit unsigned integer | `uint32_t`, `unsigned int` (x86_64), `unsigned long` (avr) | `int`             |
| `float`  | 32 bit float            | `float`                                                    | `float`           |

## Templates

Custom templates can be created for other languages and platforms. These templates are written using [Mako](http://www.makotemplates.org/). Templates should be named `<filename>.spcmd` and placed in `<spacecommand-dir>/templates/<host_templates|device_templates>/<platform>`.

Available arguments for host templates:
 - `commands` : see the `commands` section in the `Structure` section.
 - `device_config` : see the `device` section in the `Structure` section.
 - `host_config` : see the `host` section in the `Structure` section.

Available arguments for device templates:
 - `commands` : see the `commands` section in the `Structure` section.
 - `device_config` : see the `device` section in the `Structure` section.
