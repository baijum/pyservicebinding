import pytest

from pyservicebinding import binding

def test_get_binding(tmpdir, monkeypatch):
    bindings_dir = tmpdir.mkdir("bindings")
    sb1 = tmpdir.join("bindings").mkdir("sb1")
    _type = sb1.join("type")
    _type.write("mysql")
    username = sb1.join("username")
    username.write("john")
    password = sb1.join("password")
    password.write("L&ia6W@n7epi18a")
    url = sb1.join("url")
    url.write("mysql://192.168.94.102:3306/school")

    sb2 = tmpdir.join("bindings").mkdir("sb2")
    _type = sb2.join("type")
    _type.write("neo4j")
    username = sb2.join("username")
    username.write("jane")
    password = sb2.join("password")
    password.write("o4%bGt#D8v2i0ja")
    uri = sb2.join("uri")
    uri.write("neo4j://192.168.94.103:7687/cr")

    monkeypatch.setenv("SERVICE_BINDING_ROOT", str(bindings_dir))

    b = binding.get_binding("mysql")
    assert b["username"] == "john"
    assert b["password"] == "L&ia6W@n7epi18a"
    assert b["url"] == "mysql://192.168.94.102:3306/school"

    b = binding.get_binding("neo4j")
    assert b["username"] == "jane"
    assert b["password"] == "o4%bGt#D8v2i0ja"
    assert b["uri"] == "neo4j://192.168.94.103:7687/cr"

def test_get_binding_with_duplicate_entry_error(tmpdir, monkeypatch):
    bindings_dir = tmpdir.mkdir("bindings")
    sb1 = tmpdir.join("bindings").mkdir("sb1")
    _type = sb1.join("type")
    _type.write("mysql")
    username = sb1.join("username")
    username.write("john")

    sb2 = tmpdir.join("bindings").mkdir("sb2")
    _type = sb2.join("type")
    _type.write("mysql")
    username = sb2.join("username")
    username.write("jane")

    monkeypatch.setenv("SERVICE_BINDING_ROOT", str(bindings_dir))

    with pytest.raises(binding.DuplicateEntryError):
        binding.get_binding("mysql")

def test_get_binding_with_duplicate_entry_error_different_provider(tmpdir, monkeypatch):
    bindings_dir = tmpdir.mkdir("bindings")
    sb1 = tmpdir.join("bindings").mkdir("sb1")
    _type = sb1.join("type")
    _type.write("mysql")
    username = sb1.join("username")
    username.write("john")

    sb2 = tmpdir.join("bindings").mkdir("sb2")
    _type = sb2.join("type")
    _type.write("mysql")
    provider = sb2.join("provider")
    provider.write("mariadb")
    username = sb2.join("username")
    username.write("jane")

    monkeypatch.setenv("SERVICE_BINDING_ROOT", str(bindings_dir))

    with pytest.raises(binding.DuplicateEntryError):
        binding.get_binding("mysql")

def test_get_binding_without_duplicate_entry_error_different_provider(tmpdir, monkeypatch):
    bindings_dir = tmpdir.mkdir("bindings")
    sb1 = tmpdir.join("bindings").mkdir("sb1")
    _type = sb1.join("type")
    _type.write("mysql")
    username = sb1.join("username")
    username.write("john")

    sb2 = tmpdir.join("bindings").mkdir("sb2")
    _type = sb2.join("type")
    _type.write("mysql")
    provider = sb2.join("provider")
    provider.write("mariadb")
    username = sb2.join("username")
    username.write("jane")

    monkeypatch.setenv("SERVICE_BINDING_ROOT", str(bindings_dir))

    b = binding.get_binding("mysql", "mariadb")
    assert b["username"] == "jane"


def test_get_binding_with_duplicate_entry_error_same_provider(tmpdir, monkeypatch):
    bindings_dir = tmpdir.mkdir("bindings")
    sb1 = tmpdir.join("bindings").mkdir("sb1")
    _type = sb1.join("type")
    _type.write("mysql")
    provider = sb1.join("provider")
    provider.write("mariadb")
    username = sb1.join("username")
    username.write("john")

    sb2 = tmpdir.join("bindings").mkdir("sb2")
    _type = sb2.join("type")
    _type.write("mysql")
    provider = sb2.join("provider")
    provider.write("mariadb")
    username = sb2.join("username")
    username.write("jane")

    monkeypatch.setenv("SERVICE_BINDING_ROOT", str(bindings_dir))

    with pytest.raises(binding.DuplicateEntryError):
        binding.get_binding("mysql")


def test_get_binding_missing_service_binding_root(tmpdir):
    sb1 = tmpdir.mkdir("bindings").mkdir("sb1")
    _type = sb1.join("type")
    _type.write("mysql")
    username = sb1.join("username")
    username.write("john")

    with pytest.raises(binding.ServiceBindingRootMissingError):
        binding.get_binding("mysql")


def test_all_bindings(tmpdir, monkeypatch):
    bindings_dir = tmpdir.mkdir("bindings")
    sb1 = tmpdir.join("bindings").mkdir("sb1")
    _type = sb1.join("type")
    _type.write("mysql")
    username = sb1.join("username")
    username.write("john")
    password = sb1.join("password")
    password.write("L&ia6W@n7epi18a")
    url = sb1.join("url")
    url.write("mysql://192.168.94.102:3306/school")

    sb2 = tmpdir.join("bindings").mkdir("sb2")
    _type = sb2.join("type")
    _type.write("neo4j")
    username = sb2.join("username")
    username.write("jane")
    password = sb2.join("password")
    password.write("o4%bGt#D8v2i0ja")
    uri = sb2.join("uri")
    uri.write("neo4j://192.168.94.103:7687/cr")

    monkeypatch.setenv("SERVICE_BINDING_ROOT", str(bindings_dir))

    l = binding.all_bindings()
    assert len(l) == 2
    count = 0
    for b in l:
        if b["type"] == "mysql":
            count = count + 1
            assert b["username"] == "john"
            assert b["password"] == "L&ia6W@n7epi18a"
            assert b["url"] == "mysql://192.168.94.102:3306/school"

        if b["type"] == "neo4j":
            count = count + 1
            assert b["username"] == "jane"
            assert b["password"] == "o4%bGt#D8v2i0ja"
            assert b["uri"] == "neo4j://192.168.94.103:7687/cr"

    assert len(l) == 2

def test_all_bindings_missing_service_binding_root(tmpdir):
    sb1 = tmpdir.mkdir("bindings").mkdir("sb1")
    _type = sb1.join("type")
    _type.write("mysql")
    username = sb1.join("username")
    username.write("john")

    with pytest.raises(binding.ServiceBindingRootMissingError):
        binding.all_bindings()
