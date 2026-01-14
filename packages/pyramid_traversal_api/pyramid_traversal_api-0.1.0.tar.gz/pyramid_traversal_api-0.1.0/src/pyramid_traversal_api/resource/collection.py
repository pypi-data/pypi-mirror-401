from pyramid_traversal_api.resource import Resource


class ResourceCollectionValidatorMeta(type):
    def __new__(cls, clsname, bases, attrs):
        if clsname != "ResourceCollection":
            if "child_resource_class" not in attrs:
                raise ValueError(
                    f"child_resource_class must be set for ResourceClass when creating {clsname}"
                )

        return super().__new__(cls, clsname, bases, attrs)


class ResourceCollection(Resource, metaclass=ResourceCollectionValidatorMeta):
    """A node that wraps a collection of a resource, usually fetched from a database or similar.
    Override the query_collection function with your own query logic"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        if self._determine_is_reserved_keyname(key):
            raise KeyError("A view exists by this name, so stopping traversal")

        instance = self.query_item(key)

        if not instance:
            raise KeyError("No object found")

        resource = self._mkchild(
            key, self.child_resource_class, **{self.__name__: instance}
        )

        return resource

    def query_item(self, key):
        """Function intended to be overloaded with your own query logic"""
        raise NotImplementedError("Remember to implement query_item")

    @classmethod
    def get_dynamic_openapi_info(cls):
        raise NotImplementedError("get_dynamic_openapi_info needs to be implemented")
