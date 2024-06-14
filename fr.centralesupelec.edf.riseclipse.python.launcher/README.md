# RiseClipse
## RiseClipse summary
**RiseClipse** is an umbrella name for tools based on Model Driven Engineering (MDE) technologies and dedicated to [IEC](http://www.iec.ch/) standards. Open source **RiseClipse** components are availble under the [Eclipse Public License version 2.0](https://www.eclipse.org/org/documents/epl-2.0/EPL-2.0.html). More information on **RiseClipse** is available [here](https://riseclipse.github.io/).

## riseclipse-python-launcher
[![License](https://img.shields.io/badge/License-EPL_2.0-blue.svg)](https://opensource.org/licenses/EPL-2.0)

The scripts in this folder offer a Python API that can be used to launch validations programmatically.

For the moment, only the SCL validator is available. The corresponding script is `riseclipse_validator_scl.py`.

Here is an example of what can be done:
```
from riseclipse_validator_scl import RiseClipseValidatorSCL

validator = RiseClipseValidatorSCL()
validator.add_file("ICD_test.icd")
validator.add_file("NSD")
validator.add_file("OCL")

validator.validate_to_stdout() # The result is displayed on stdout

validator.set_output_level("notice")
out=validator.validate()      # The result is stored in an object having its own API
print(out.get_errors())
print(out.get_only_warnings())

```

The validator jar file is needed. The script can be used to install it:
```
% python3 riseclipse_validator_scl.py
It seems that the validator is missing.
You can download one using '--download latest' command line option (or use a specific version instead of latest).
% python3 riseclipse_validator_scl.py --download 1.2.6
% python3 riseclipse_validator_scl.py
Your version is: 1.2.6
A new version is available: 1.2.7
You can download it using '--download latest' command line option
% python3 riseclipse_validator_scl.py --download latest
Latest version is  1.2.7
% python3 riseclipse_validator_scl.py
Your version is: 1.2.7
Your version is the latest one
```

Another way is to use the API to specify the path of the validator jar (```set_jar_file()```).


The API documentation is available [here](https://riseclipse.github.io/riseclipse-python/python-launcher-docs/index.html).

