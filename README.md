# SpaceCommander

Simplify communication between computers and microcontrollers.

Currently supported microcontrollers:

- Arduino series
 
Currently supported host languages:

 - Python3
 
View the `samples` directory for usage examples.

## Installation

Please [install Python3 first](https://www.python.org/downloads/).

crcmod

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
More details for the format of this document can be found [here](CONFIGURATION.md).

Files are generated to:
`<root>/generated/<platform>/`



## Templates

Custom templates can be created for other languages and platforms. These templates are written using [Mako](http://www.makotemplates.org/). Templates should be named `<filename>.spcmd` and placed in `<spacecommand-dir>/templates/<host_templates|device_templates>/<platform>`.

Available arguments for host templates:
 - `commands` : see the `commands` section in the `Structure` section.
 - `device_config` : see the `device` section in the `Structure` section.
 - `host_config` : see the `host` section in the `Structure` section.

Available arguments for device templates:
 - `commands` : see the `commands` section in the `Structure` section.
 - `device_config` : see the `device` section in the `Structure` section.


Add addressing scheme for connection type
Add callbacks before and after read/write to allow for RS485
Fix timeouts
Improve error handling, add CRC
Strings
Heartbeat
