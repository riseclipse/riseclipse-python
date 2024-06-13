
from riseclipse_validator_scl import RiseClipseValidatorSCL

validator = RiseClipseValidatorSCL()
validator.set_use_color()
#validator.set_output_level("notice")
validator.set_java_command("/Users/marcadet/.sdkman/candidates/java/17.0.3-tem/bin/java")
validator.set_jar_file("/Users/marcadet/Documents/Eclipse/runtime-RiseClipse/fr.centralesupelec.riseclipse.models.iec61850.scl/RiseClipseValidatorSCL-1.2.7.jar")
validator.add_file("/Users/marcadet/Documents/Eclipse/runtime-RiseClipse/fr.centralesupelec.riseclipse.models.iec61850.scl/ICD_test.icd")
validator.add_file("/Users/marcadet/Documents/Eclipse/runtime-RiseClipse/fr.centralesupelec.riseclipse.models.iec61850.scl/NSD")
#validator.add_file("/Users/marcadet/Documents/Eclipse/runtime-RiseClipse/fr.centralesupelec.riseclipse.models.iec61850.scl/OCL")
#print(validator.compute_arguments())
out=validator.validate()
print(out.get_errors())

