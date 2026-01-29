import os
import sys

from a2a_acl.utils.url import build_url

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

advisor_port = 9989
manager_port = 9981
validator_port = 9999

specification = "A function that says hello."
code = 'def hello(name): print("hello " + name + ".")'

