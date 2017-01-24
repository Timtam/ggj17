# this file will generate the build configuration files needed to build releases automatically
# it will for instance generate build files using the version number given in script.py, so that we just need to update the version on one single place
# run this file before committing the final one for a new version, meaning before you merge into stable
# and don't forget to commit the generated build files too!
from script import Script
import yaml

# keep it short and simple
# configure this dictionary for any changes, it will be converted into the yaml file later

this=Script()
appveyor_configuration={
  "version": this.Version + "-{build}",
  "build": "off",
  "install": [
    "%PYTHON%\\\\python.exe -m pip install -r requirements.txt"
  ],
  "environment": {
    "matrix": [
      {
        "PYTHON": "C:\\\\python27"
      }
    ]
  },
  "platform": ["x86"],
  "test_script": ["%PYTHON%\\\\python.exe setup.py -c -o=2"],
  "artifacts": {
    "path": this.Name+"-"+this.Version+".zip"
  },
  "skip_tags": True
}

# this will finally just drop a file with the given name, constructed from this stuff above
with open("appveyor.yml", "w") as f:
  yaml.dump(appveyor_configuration, f, default_flow_style=False, indent=2)
