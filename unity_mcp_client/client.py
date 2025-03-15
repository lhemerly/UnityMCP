import requests


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

    def create_gameobject(self, object_name: str) -> dict:
        """
        Create a new GameObject in the currently active Unity scene.
        :param object_name: The name for the new GameObject.
        :return: A dict with the server's response data.
        """
        payload = {
            "command": "create_gameobject",
            "parameters": {
                "objectName": object_name
            }
        }
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
        :return: A dict with { "prefabs": [ { "name": ..., "path": ... }, ... ] }
        """
        payload = {
            "command": "get_all_prefabs",
            "parameters": {}
        }
        return self._send_request(payload)

    def get_all_gameobjects_in_scene(self) -> dict:
        """
        Get a list of all GameObjects in the currently active scene.
        :return: A dict with { "gameObjects": [ ... ] }
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
        :param component_type_name: The type name, e.g. "Rigidbody", "BoxCollider", etc.
        :return: Response data
        """
        payload = {
            "command": "add_component",
            "parameters": {
                "gameObjectName": gameobject_name,
                "componentTypeName": component_type_name
            }
        }
        return self._send_request(payload)

    def create_script_asset(self, script_name: str, script_content: str) -> dict:
        """
        Dynamically create a C# script in Unity.
        :param script_name: Name of the new script file (no .cs extension).
        :param script_content: The entire script content as a string.
        :return: A dict with a success/failure message
        """
        payload = {
            "command": "create_script_asset",
            "parameters": {
                "scriptName": script_name,
                "scriptContent": script_content
            }
        }
        return self._send_request(payload)

    def set_component_property(self, gameobject_name: str, component_type: str, property_name: str, value) -> dict:
        """
        Set a property on a component attached to a specific GameObject.
        For example, property: 'mass' on a 'Rigidbody' component.
        :param gameobject_name: Name of the GameObject.
        :param component_type: Name of the component type, e.g. "Rigidbody".
        :param property_name: The property to set, e.g. "mass".
        :param value: The value to set, must be convertible to the correct type in Unity.
        :return: A dict with the operation result.
        """
        payload = {
            "command": "set_component_property",
            "parameters": {
                "gameObjectName": gameobject_name,
                "componentType": component_type,
                "propertyName": property_name,
                "value": value
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
