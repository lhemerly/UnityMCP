import requests
import re


class UnityMCP:
    """
    Python client for communicating with a Unity MCP server.
    Provides function-level abstractions for each major MCP operation.
    """

    def __init__(self, host: str = "http://127.0.0.1:8080"):
        """
        :param host: The base URL of the MCP server.
                     Example: "http://127.0.0.1:8080"
        """
        self.host = host.rstrip("/")  # remove trailing slash if any

    def create_gameobject(self, object_name: str, parent_name: str = None) -> dict:
        """
        Create a new GameObject in the currently active Unity scene.
        :param object_name: The name for the new GameObject.
        :param parent_name: Optional name of a parent GameObject to set as the parent.
        :return: A dict with the server's response data.
        """
        payload = {
            "command": "create_gameobject",
            "parameters": {
                "objectName": object_name
            }
        }
        
        # Add parent_name to parameters if provided
        if parent_name:
            payload["parameters"]["parentName"] = parent_name
            
        return self._send_request(payload)

    def get_all_scenes(self) -> dict:
        """
        Ask the server for a list of all scenes in the project.
        :return: A dict with scene paths, or an error if something went wrong.
        """
        payload = {
            "command": "get_all_scenes",
            "parameters": {}
        }
        return self._send_request(payload)

    def get_all_prefabs(self) -> dict:
        """
        Get a list of all prefabs in the project.
        :return: A dict with prefab names and their paths.
        """
        payload = {
            "command": "get_all_prefabs",
            "parameters": {}
        }
        return self._send_request(payload)

    def get_all_gameobjects_in_scene(self) -> dict:
        """
        Get a list of all GameObjects in the currently active scene.
        :return: A dict with { "success": true, "gameObjects": [ ... ] }
        """
        payload = {
            "command": "get_all_gameobjects_in_scene",
            "parameters": {}
        }
        return self._send_request(payload)

    def add_component_to_gameobject(self, gameobject_name: str, component_type_name: str) -> dict:
        """
        Add a built-in component (e.g. "Rigidbody") to a named GameObject.
        :param gameobject_name: Name of the target GameObject.
        :param component_type_name: The type name. Can be:
                                  - Regular components: "Rigidbody", "BoxCollider", etc.
                                  - Special mesh types: "CubeMesh", "SphereMesh", "CylinderMesh", "CapsuleMesh", "PlaneMesh"
                                  For mesh types, this will automatically add MeshFilter and MeshRenderer components.
        :return: Response data
        """
        # Handle special mesh type components
        if component_type_name.endswith("Mesh"):
            # First add MeshFilter
            result = self._send_request({
                "command": "add_component",
                "parameters": {
                    "gameObjectName": gameobject_name,
                    "componentTypeName": "MeshFilter"
                }
            })
            if not result.get('success'):
                return result

            # Then add MeshRenderer
            result = self._send_request({
                "command": "add_component",
                "parameters": {
                    "gameObjectName": gameobject_name,
                    "componentTypeName": "MeshRenderer"
                }
            })
            if not result.get('success'):
                return result

            # Set the primitive mesh type
            mesh_type = component_type_name[:-4].lower()  # Remove "Mesh" and lowercase
            return self.set_component_property(
                gameobject_name,
                "MeshFilter",
                "mesh",
                f"UnityEngine.Mesh, UnityEngine.CoreModule:UnityEngine.{mesh_type}"
            )

        # Regular component handling
        payload = {
            "command": "add_component",
            "parameters": {
                "gameObjectName": gameobject_name,
                "componentTypeName": component_type_name
            }
        }
        return self._send_request(payload)

    def create_script_asset(self, script_name: str, script_content: str, folder_path: str = None) -> dict:
        """
        Dynamically create a C# script in Unity.
        :param script_name: Name of the new script file (no .cs extension).
        :param script_content: The entire script content as a string.
        :param folder_path: Optional folder path where script will be created, defaults to "Assets/MCP/Scripts".
        :return: A dict with a success/failure message
        """
        params = {
            "scriptName": script_name,
            "scriptContent": script_content
        }
        
        if folder_path:
            params["folderPath"] = folder_path
            
        payload = {
            "command": "create_script_asset",
            "parameters": params
        }
        return self._send_request(payload)

    def _format_vector3(self, value) -> str:
        """
        Format a value as a Vector3 string in the format "x,y,z" expected by Unity.
        
        :param value: Value to format, can be tuple, list, string, etc.
        :return: Formatted string like "x,y,z"
        """
        # If already a string in correct format, return it
        if isinstance(value, str):
            # If already in x,y,z format, return as is
            if re.match(r'^-?\d*\.?\d*,-?\d*\.?\d*,-?\d*\.?\d*$', value):
                return value
                
            # Extract numbers from string formats like "(10, 1, 10)" or "Vector3(10,1,10)"
            matches = re.findall(r'-?\d+\.?\d*', value)
            if len(matches) >= 3:
                return f"{matches[0]},{matches[1]},{matches[2]}"
                
        # If tuple or list with at least 3 elements
        elif isinstance(value, (tuple, list)) and len(value) >= 3:
            return f"{value[0]},{value[1]},{value[2]}"
            
        # If couldn't parse, return original value and let server handle error
        return str(value)
            
    def set_component_property(self, gameobject_name: str, component_type: str, property_name: str, value) -> dict:
        """
        Set a property on a component attached to a specific GameObject.
        For example, property: 'mass' on a 'Rigidbody' component.
        
        :param gameobject_name: Name of the GameObject.
        :param component_type: Name of the component type, e.g. "Rigidbody".
        :param property_name: The property to set, e.g. "mass".
        :param value: The value to set. For Vector3 properties (like Transform.position or scale):
                      - Pass as tuple/list: (x, y, z)
                      - Pass as string in format: "x,y,z" 
                      - Or formats like "(x, y, z)" will be automatically converted
        :return: A dict with the operation result.
        """
        # Map "scale" to "localScale" for Transform component
        if component_type == "Transform" and property_name.lower() == "scale":
            property_name = "localScale"
        
        # Special handling for Vector3 values if this is likely a Vector3 property
        formatted_value = value
        if component_type == "Transform" and property_name.lower() in ["position", "localscale", "rotation", "eulerAngles"]:
            formatted_value = self._format_vector3(value)
        elif isinstance(value, (tuple, list)) and len(value) == 3:
            # If we have a tuple/list of 3 values, it's likely a Vector3
            formatted_value = self._format_vector3(value)
            
        payload = {
            "command": "set_component_property",
            "parameters": {
                "gameObjectName": gameobject_name,
                "componentType": component_type,
                "propertyName": property_name,
                "value": formatted_value
            }
        }
        return self._send_request(payload)
        
    def instantiate_prefab(self, prefab_path: str) -> dict:
        """
        Instantiate a prefab in the current scene.
        :param prefab_path: Path to the prefab asset in the project.
        :return: A dict with the instantiated GameObject information.
        """
        payload = {
            "command": "instantiate_prefab",
            "parameters": {
                "prefabPath": prefab_path
            }
        }
        return self._send_request(payload)
        
    def find_gameobjects_by_tag(self, tag: str) -> dict:
        """
        Find all GameObjects with the specified tag.
        :param tag: The tag to search for.
        :return: A dict with a list of GameObjects with that tag.
        """
        payload = {
            "command": "find_gameobjects_by_tag",
            "parameters": {
                "tag": tag
            }
        }
        return self._send_request(payload)
        
    def get_all_components(self, gameobject_name: str) -> dict:
        """
        Get all components attached to the specified GameObject.
        :param gameobject_name: The name of the GameObject.
        :return: A dict with a list of component names.
        """
        payload = {
            "command": "get_all_components",
            "parameters": {
                "gameObjectName": gameobject_name
            }
        }
        return self._send_request(payload)
        
    def remove_component(self, gameobject_name: str, component_name: str) -> dict:
        """
        Remove a component from a GameObject.
        :param gameobject_name: Name of the GameObject.
        :param component_name: Name of the component to remove.
        :return: A dict with the operation result.
        """
        payload = {
            "command": "remove_component",
            "parameters": {
                "gameObjectName": gameobject_name,
                "componentName": component_name
            }
        }
        return self._send_request(payload)
        
    def delete_gameobject(self, gameobject_name: str) -> dict:
        """
        Delete a GameObject from the scene.
        :param gameobject_name: Name of the GameObject to delete.
        :return: A dict with the operation result.
        """
        payload = {
            "command": "delete_gameobject",
            "parameters": {
                "name": gameobject_name
            }
        }
        return self._send_request(payload)

    def _send_request(self, payload: dict) -> dict:
        """
        Internal helper to send a JSON-encoded POST to the MCP server and parse response as JSON.
        Raises an exception if the request fails or if response is not JSON.
        :param payload: Dictionary to send as JSON
        :return: The server's JSON-decoded response as a dict
        """
        url = f"{self.host}/"
        headers = {"Content-Type": "application/json"}
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=5)
            resp.raise_for_status()  # raises HTTPError if not 200-299
            return resp.json() if resp.text else {}
        except (requests.exceptions.RequestException, ValueError) as e:
            raise RuntimeError(f"Request to MCP server failed: {e}")
