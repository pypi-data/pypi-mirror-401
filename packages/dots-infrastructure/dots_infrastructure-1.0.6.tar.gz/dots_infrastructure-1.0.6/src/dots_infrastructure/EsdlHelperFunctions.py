from typing import List

class EsdlHelperFunctions:
    
    @staticmethod
    def get_all_esdl_objects_from_type(collection, type) -> List:
        """
        Get all esdl objs of a specific type from a collection.

        **Parameters**

        - **`collection`** - Collection of esdl objs.
        - **`type`** - Type of the esdl objs to find.
        """
        return [esdl_obj for esdl_obj in collection if isinstance(esdl_obj, type)]
    
    @staticmethod
    def get_esdl_object_with_id(collection, id) -> List:
        """
        Find an esdl obj in a collection by id.

        **Parameters**

        - **`collection`** - Collection of esdl objs.
        - **`id`** - id of the esdl obj.
        """
        return next((esdl_obj for esdl_obj in collection if hasattr(esdl_obj, "id") and esdl_obj.id == id), None)
