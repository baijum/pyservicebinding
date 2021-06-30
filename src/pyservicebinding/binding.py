import os
import typing

class ServiceBindingRootMissingError(KeyError):
    pass

class DuplicateEntryError(KeyError):
    pass

def all_bindings() -> list[dict[str, str]]:
    """Get all bindings as a list of dictionaries

    - return empty list if no bindings found
    - raise ServiceBindingRootMissingError if SERVICE_BINDING_ROOT env var not set
    """

    try:
        root = os.environ["SERVICE_BINDING_ROOT"]
    except KeyError as msg:
        raise ServiceBindingRootMissingError(msg)

    l = []
    for dirname in os.listdir(root):
        b = {}
        for filename in os.listdir(os.path.join(root, dirname)):
            b[filename] = open(os.path.join(root, dirname, filename)).read().strip()

        l.append(b)

    return l

def get_binding(_type: str, provider: typing.Optional[str] = None) -> dict[str, str]:
    """Get binding as a dictionary for a given type and optional provider

    - return empty dictionary if no binding found
    - raise DuplicateEntryError if duplicate entry found
    - raise ServiceBindingRootMissingError if SERVICE_BINDING_ROOT env var not set
    """

    try:
        root = os.environ["SERVICE_BINDING_ROOT"]
    except KeyError as msg:
        raise ServiceBindingRootMissingError(msg)

    b = {}
    dupcheck = []
    if provider:
        for dirname in os.listdir(root):
            typepath = os.path.join(root, dirname, "type")
            providerpath = os.path.join(root, dirname, "provider")
            if os.path.exists(typepath):
                typevalue = open(typepath).read().strip()
                if typevalue != _type:
                    continue
                if os.path.exists(providerpath):
                    providervalue = open(providerpath).read().strip()
                    if providervalue != provider:
                        continue
                    dupcheck.append(typevalue + ":" + providervalue)

                    for filename in os.listdir(os.path.join(root, dirname)):
                        b[filename] = open(os.path.join(root, dirname, filename)).read().strip()
    else:
        for dirname in os.listdir(root):
            typepath = os.path.join(root, dirname, "type")
            if os.path.exists(typepath):
                typevalue = open(typepath).read().strip()
                if typevalue != _type:
                    continue
                dupcheck.append(typevalue)

                for filename in os.listdir(os.path.join(root, dirname)):
                    b[filename] = open(os.path.join(root, dirname, filename)).read().strip()

    if len(dupcheck) > 1 and all(x==dupcheck[0] for x in dupcheck):
        raise DuplicateEntryError(dupcheck)

    return b
