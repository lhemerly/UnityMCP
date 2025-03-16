# Unity MCP Client

A Python client library for communicating with Unity Editor through the MCP (Multiplatform Control Protocol).

## Overview

Unity MCP Client is a Python library that allows you to control Unity Editor remotely. It communicates with a server running within Unity to manipulate GameObjects, components, and assets in real-time using a simple API.

This client enables you to:
- Automate Unity Editor tasks
- Create and manipulate GameObjects programmatically
- Add components to objects
- Set component properties
- Create C# scripts dynamically
- Work with prefabs
- Query scene information

## Installation

```sh
pip install unity-mcp
```

## Usage

```python
from unity_mcp_client import UnityMCP

# Create a client instance (default connects to http://127.0.0.1:8080)
mcp = UnityMCP()

# Create a new GameObject
result = mcp.create_gameobject("MyObject")
print(f"Created: {result}")

# Create a GameObject with a parent
result = mcp.create_gameobject("Child", parent_name="MyObject")
print(f"Created child object: {result}")

# Add a component to it
mcp.add_component_to_gameobject("MyObject", "Rigidbody")

# Set a component property
mcp.set_component_property("MyObject", "Rigidbody", "mass", 5.0)

# Get all GameObjects in the current scene
all_objects = mcp.get_all_gameobjects_in_scene()
print(f"Scene contains {len(all_objects['gameObjects'])} objects")

# Find all GameObjects with a specific tag
tagged_objects = mcp.find_gameobjects_by_tag("Player")
print(f"Found {len(tagged_objects['gameObjects'])} with 'Player' tag")
```

## Available Commands

The Python client provides the following methods:

### Scene Management
- `get_all_scenes()` - Get a list of all scenes in the project
- `get_all_gameobjects_in_scene()` - Get all GameObjects in the active scene

### GameObject Operations
- `create_gameobject(object_name, parent_name=None)` - Create a new GameObject with an optional parent
- `delete_gameobject(gameobject_name)` - Delete a GameObject
- `find_gameobjects_by_tag(tag)` - Find all GameObjects with a specific tag

### Component Manipulation
- `add_component_to_gameobject(gameobject_name, component_type_name)` - Add a component to a GameObject
- `get_all_components(gameobject_name)` - Get all components attached to a GameObject
- `remove_component(gameobject_name, component_name)` - Remove a component from a GameObject
- `set_component_property(gameobject_name, component_type, property_name, value)` - Set a property value on a component

### Prefab Operations
- `get_all_prefabs()` - Get a list of all prefabs in the project
- `instantiate_prefab(prefab_path)` - Instantiate a prefab in the current scene

### Asset Creation
- `create_script_asset(script_name, script_content, folder_path=None)` - Create a C# script file

## Error Handling

The client uses standard HTTP requests and will raise exceptions for connection errors:

```python
try:
    result = mcp.create_gameobject("MyObject")
except RuntimeError as e:
    print(f"Error: {e}")
```

## Requirements

- Python 3.6+
- The `requests` Python package
- Unity Editor running with the MCP server plugin

## How It Works

The client sends HTTP requests with JSON payloads to the MCP server running within Unity Editor. The server processes these commands and performs the requested operations in Unity, then returns results as JSON responses.

## Server Setup

To use this client, you'll need a Unity project with the MCP server plugin installed and running. Please refer to the Unity MCP Server documentation for setup instructions.

## License

See the LICENSE file for details.
