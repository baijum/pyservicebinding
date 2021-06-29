import os
import sys

from pyservicebinding import binding

def test_get_binding(tmpdir):
    bindings_dir = tmpdir.mkdir("bindings")
    sb1 = tmpdir.join("bindings").mkdir("sb1")
    _type = sb1.join("type")
    _type.write("mysql")
    username = sb1.join("username")
    username.write("john")

    os.environ["SERVICE_BINDING_ROOT"] = str(bindings_dir)

    b = binding.get_binding("mysql")
    #assert b["username"] == "john"
    #b["password"] = "L&ia6W@n7epi18a"
    #b["url"] = "mysql://192.168.94.102:3306/school"

def test_all_bindings():
    pass
