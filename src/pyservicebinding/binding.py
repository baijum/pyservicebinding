import os
import typing

class ServiceBindingRootMissingError(Exception):
    pass


class ServiceBinding:

    def __init__(self):
        try:
            self.root = os.environ["SERVICE_BINDING_ROOT"]
        except KeyError as msg:
            raise ServiceBindingRootMissingError(msg)


    def all_bindings(self) -> list[dict[str, str]]:
        """Get all bindings as a list of dictionaries

        - return empty list if no bindings found
        """
        root = self.root
        l = []
        for dirname in os.listdir(root):
            b = {}
            for filename in os.listdir(os.path.join(root, dirname)):
                b[filename] = open(os.path.join(root, dirname, filename)).read().strip()

            l.append(b)

        return l

    def bindings(self, _type: str, provider: typing.Optional[str] = None) -> list[dict[str, str]]:
        """Get filtered bindings as a list of dictionaries

        - return empty dictionary if no binding found
        - filter the result with the given _type input
        - if provider input is given, filter bindings using the given type and provider
        """
        root = self.root
        l = []
        b = {}
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

                        for filename in os.listdir(os.path.join(root, dirname)):
                            b[filename] = open(os.path.join(root, dirname, filename)).read().strip()

                        l.append(b)
        else:
            for dirname in os.listdir(root):
                typepath = os.path.join(root, dirname, "type")
                if os.path.exists(typepath):
                    typevalue = open(typepath).read().strip()
                    if typevalue != _type:
                        continue

                    for filename in os.listdir(os.path.join(root, dirname)):
                        b[filename] = open(os.path.join(root, dirname, filename)).read().strip()

                    l.append(b)

        return l
