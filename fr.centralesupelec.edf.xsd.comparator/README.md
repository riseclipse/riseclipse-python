# RiseClipse
## RiseClipse summary
**RiseClipse** is an umbrella name for tools based on Model Driven Engineering (MDE) technologies and dedicated to [IEC](http://www.iec.ch/) standards. Open source **RiseClipse** components are availble under the [Eclipse Public License version 2.0](https://www.eclipse.org/org/documents/epl-2.0/EPL-2.0.html). More information on **RiseClipse** is available [here](https://riseclipse.github.io/).

## XML Schema Comparator
[![License](https://img.shields.io/badge/License-EPL_2.0-blue.svg)](https://opensource.org/licenses/EPL-2.0)

This repository contains a Python tool for comparing two XML Schemas, for example two versions of the XSDs of SCL.

## Usage

To use the Python code, we recommend that you create a dedicated python3 environment, containing the dependencies indicated in `requirements.txt`.

To compare two XSD files, run the command
```bash
python3 src/main.py path/to/xsd1.xsd path/to/xsd2.xsd
```
The command line output will display the result of the comparison.

Options:
```
usage: main.py [-h] [-a] [-r ROOT_ELEMENT] [-v VERBOSE_LEVEL] [-c CONFIG]
               XSD_1 XSD_2

positional arguments:
  XSD_1                 File path for XSD 1.
  XSD_2                 File path for XSD 2.

options:
  -h, --help            show this help message and exit
  -a, --all-root-elements
                        Compare XSD taking all root elements in account.
  -r ROOT_ELEMENT, --root-element ROOT_ELEMENT
                        Compare XSD taking only this root element in account.
  -v VERBOSE_LEVEL, --verbose-level VERBOSE_LEVEL
                        Select how verbose the results are, from 0 to 2.
                        Default is 1
  -c CONFIG, --config CONFIG
                        Path to configuration file.
```

A configuration file allows you to specify which configuration attributes you wish to ignore.
Any attribute not specified in the config file will have a default value, which is described in `src/normalizer/config_builder.py`. To ignore an attribute, add the line `myattribute=false` in the appropriate section of the configuration file.

The default configuration file is `default_config.conf`.

Here's the list of all the attributes taken into account, and which can therefore be ignored.
```
[schema]
id=true
attributeFormDefault=false
elementFormDefault=false
blockDefault=false
finalDefault=false
targetNamespace=true
version=true
xmlns=true

[element]
abstract=true
block=true
default=true
final=true
fixed=true
form=true
id=true
minOccurs=true
maxOccurs=true
name=true
nillable=true
type=true
index_in_sequence=true

[any element]
id=true
minOccurs=true
maxOccurs=true
namespace=true
process_contents=true
index_in_sequence=true

[attribute]
default=true
fixed=true
form=true
id=true
name=true
type=true
use=true

[any attribute]
id=true
namespace=true
process_contents=true
```
