import unittest
from unittest import mock
import json
import requests
from unity_mcp_client.client import UnityMCP


class TestUnityMCP(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.default_host = "http://127.0.0.1:8080"
        self.custom_host = "http://192.168.1.100:9000"
        self.client = UnityMCP()
        self.custom_client = UnityMCP(host=self.custom_host)

    def test_init_default(self):
        """Test constructor with default parameters."""
        self.assertEqual(self.client.host, self.default_host)

    def test_init_custom(self):
        """Test constructor with custom host."""
        self.assertEqual(self.custom_client.host, self.custom_host)

    def test_init_trailing_slash(self):
        """Test constructor removes trailing slash from host."""
        client = UnityMCP(host="http://example.com/")
        self.assertEqual(client.host, "http://example.com")

    @mock.patch('requests.post')
    def test_create_gameobject(self, mock_post):
        """Test create_gameobject method."""
        # Setup mock response
        mock_response = mock.Mock()
        mock_response.text = json.dumps({"success": True, "id": "123"})
        mock_response.json.return_value = {"success": True, "id": "123"}
        mock_post.return_value = mock_response

        # Call the method
        result = self.client.create_gameobject("TestObject")

        # Assertions
        mock_post.assert_called_once_with(
            f"{self.default_host}/",
            json={
                "command": "create_gameobject",
                "parameters": {"objectName": "TestObject"}
            },
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        self.assertEqual(result, {"success": True, "id": "123"})

    @mock.patch('requests.post')
    def test_get_all_scenes(self, mock_post):
        """Test get_all_scenes method."""
        # Setup mock response
        mock_response = mock.Mock()
        mock_response.text = json.dumps({"scenes": ["scene1.unity", "scene2.unity"]})
        mock_response.json.return_value = {"scenes": ["scene1.unity", "scene2.unity"]}
        mock_post.return_value = mock_response

        # Call the method
        result = self.client.get_all_scenes()

        # Assertions
        mock_post.assert_called_once_with(
            f"{self.default_host}/",
            json={"command": "get_all_scenes", "parameters": {}},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        self.assertEqual(result, {"scenes": ["scene1.unity", "scene2.unity"]})

    @mock.patch('requests.post')
    def test_get_all_prefabs(self, mock_post):
        """Test get_all_prefabs method."""
        # Setup mock response
        mock_response = mock.Mock()
        prefabs_data = {
            "prefabs": [
                {"name": "Prefab1", "path": "Assets/Prefabs/Prefab1.prefab"},
                {"name": "Prefab2", "path": "Assets/Prefabs/Prefab2.prefab"}
            ]
        }
        mock_response.text = json.dumps(prefabs_data)
        mock_response.json.return_value = prefabs_data
        mock_post.return_value = mock_response

        # Call the method
        result = self.client.get_all_prefabs()

        # Assertions
        mock_post.assert_called_once_with(
            f"{self.default_host}/",
            json={"command": "get_all_prefabs", "parameters": {}},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        self.assertEqual(result, prefabs_data)

    @mock.patch('requests.post')
    def test_get_all_gameobjects_in_scene(self, mock_post):
        """Test get_all_gameobjects_in_scene method."""
        # Setup mock response
        mock_response = mock.Mock()
        gameobjects_data = {
            "gameObjects": ["MainCamera", "Player", "Enemy"]
        }
        mock_response.text = json.dumps(gameobjects_data)
        mock_response.json.return_value = gameobjects_data
        mock_post.return_value = mock_response

        # Call the method
        result = self.client.get_all_gameobjects_in_scene()

        # Assertions
        mock_post.assert_called_once_with(
            f"{self.default_host}/",
            json={"command": "get_all_gameobjects_in_scene", "parameters": {}},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        self.assertEqual(result, gameobjects_data)

    @mock.patch('requests.post')
    def test_add_component_to_gameobject(self, mock_post):
        """Test add_component_to_gameobject method."""
        # Setup mock response
        mock_response = mock.Mock()
        mock_response.text = json.dumps({"success": True})
        mock_response.json.return_value = {"success": True}
        mock_post.return_value = mock_response

        # Call the method
        result = self.client.add_component_to_gameobject("Player", "Rigidbody")

        # Assertions
        mock_post.assert_called_once_with(
            f"{self.default_host}/",
            json={
                "command": "add_component",
                "parameters": {
                    "gameObjectName": "Player",
                    "componentTypeName": "Rigidbody"
                }
            },
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        self.assertEqual(result, {"success": True})

    @mock.patch('requests.post')
    def test_create_script_asset(self, mock_post):
        """Test create_script_asset method."""
        # Setup mock response
        mock_response = mock.Mock()
        mock_response.text = json.dumps({"success": True, "path": "Assets/Scripts/Test.cs"})
        mock_response.json.return_value = {"success": True, "path": "Assets/Scripts/Test.cs"}
        mock_post.return_value = mock_response

        # Sample script content
        script_content = """
        using UnityEngine;
        
        public class Test : MonoBehaviour {
            void Start() {
                Debug.Log("Hello World");
            }
        }
        """

        # Call the method
        result = self.client.create_script_asset("Test", script_content)

        # Assertions
        mock_post.assert_called_once_with(
            f"{self.default_host}/",
            json={
                "command": "create_script_asset",
                "parameters": {
                    "scriptName": "Test",
                    "scriptContent": script_content
                }
            },
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        self.assertEqual(result, {"success": True, "path": "Assets/Scripts/Test.cs"})

    @mock.patch('requests.post')
    def test_set_component_property(self, mock_post):
        """Test set_component_property method."""
        # Setup mock response
        mock_response = mock.Mock()
        mock_response.text = json.dumps({"success": True})
        mock_response.json.return_value = {"success": True}
        mock_post.return_value = mock_response

        # Call the method
        result = self.client.set_component_property("Player", "Rigidbody", "mass", 10.5)

        # Assertions
        mock_post.assert_called_once_with(
            f"{self.default_host}/",
            json={
                "command": "set_component_property",
                "parameters": {
                    "gameObjectName": "Player",
                    "componentType": "Rigidbody",
                    "propertyName": "mass",
                    "value": 10.5
                }
            },
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        self.assertEqual(result, {"success": True})

    @mock.patch('requests.post')
    def test_send_request_success(self, mock_post):
        """Test _send_request with successful response."""
        # Setup mock response
        mock_response = mock.Mock()
        mock_response.text = json.dumps({"success": True})
        mock_response.json.return_value = {"success": True}
        mock_post.return_value = mock_response

        # Call the method
        result = self.client._send_request({"command": "test", "parameters": {}})

        # Assertions
        mock_post.assert_called_once_with(
            f"{self.default_host}/",
            json={"command": "test", "parameters": {}},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        self.assertEqual(result, {"success": True})

    @mock.patch('requests.post')
    def test_send_request_empty_response(self, mock_post):
        """Test _send_request with empty response."""
        # Setup mock response
        mock_response = mock.Mock()
        mock_response.text = ""  # Empty response
        mock_post.return_value = mock_response

        # Call the method
        result = self.client._send_request({"command": "test", "parameters": {}})

        # Assertions
        self.assertEqual(result, {})

    @mock.patch('requests.post')
    def test_send_request_http_error(self, mock_post):
        """Test _send_request with HTTP error."""
        # Setup mock to raise an HTTPError
        mock_post.side_effect = requests.exceptions.HTTPError("404 Client Error")

        # Call the method and assert it raises RuntimeError
        with self.assertRaises(RuntimeError) as context:
            self.client._send_request({"command": "test", "parameters": {}})

        self.assertIn("Request to MCP server failed", str(context.exception))

    @mock.patch('requests.post')
    def test_send_request_connection_error(self, mock_post):
        """Test _send_request with connection error."""
        # Setup mock to raise a ConnectionError
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection refused")

        # Call the method and assert it raises RuntimeError
        with self.assertRaises(RuntimeError) as context:
            self.client._send_request({"command": "test", "parameters": {}})

        self.assertIn("Request to MCP server failed", str(context.exception))

    @mock.patch('requests.post')
    def test_send_request_timeout(self, mock_post):
        """Test _send_request with timeout."""
        # Setup mock to raise a Timeout
        mock_post.side_effect = requests.exceptions.Timeout("Request timed out")

        # Call the method and assert it raises RuntimeError
        with self.assertRaises(RuntimeError) as context:
            self.client._send_request({"command": "test", "parameters": {}})

        self.assertIn("Request to MCP server failed", str(context.exception))

    @mock.patch('requests.post')
    def test_send_request_json_decode_error(self, mock_post):
        """Test _send_request with invalid JSON response."""
        # Setup mock response with invalid JSON
        mock_response = mock.Mock()
        mock_response.text = "Not a valid JSON"
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_post.return_value = mock_response

        # Call the method and assert it raises RuntimeError
        with self.assertRaises(RuntimeError) as context:
            self.client._send_request({"command": "test", "parameters": {}})

        self.assertIn("Request to MCP server failed", str(context.exception))


if __name__ == '__main__':
    unittest.main()