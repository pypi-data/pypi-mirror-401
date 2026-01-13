# PyListenerTool
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![PyPI Version](https://img.shields.io/pypi/v/PyListenerTool.svg)
![Downloads](https://img.shields.io/pypi/dm/PyListenerTool.svg)

A lightweight event listener system for Python classes that auto-generates documentation.

## 📦 Installation
```bash
pip install PyListenerTool
```

## 📜 Changelog
See [CHANGELOG.md](https://github.com/qiufengcute/PyListenerTool/blob/main/CHANGELOG.md)

## ✨ Features

- **Decorator-based API**: Use `@Listener` to transform any class into an event-driven system
- **Flexible Event Handling**: Support both synchronous and asynchronous event handlers
- **One-time Listeners**: Register listeners that trigger only once
- **Error Handling**: Custom error callbacks for each listener
- **Auto-documentation**: Generate HTML or Markdown documentation for all events
- **Thread-safe Async Support**: Async handlers run in separate threads
- **Event Discovery**: Analyze classes to extract event information

## 🚀 QuickStart

### Basic Usage

```python
from PyListenerTool import Listener, extract_listeners

@Listener
class ChatRoom:
    def __init__(self, name):
        self.name = name
        self._addListenerDoc("message", "Triggered when a message is received", "username: str", "message: str")
        self._addListenerDoc("user_joined", "Triggered when a user joins the room", "username: str")
    
    def send_message(self, username, message):
        self._call("message", username, message)
    
    def user_join(self, username):
        self._call("user_joined", username)

# Create an instance
room = ChatRoom("Python Developers")

# Add listeners
@room.on("message")
def handle_message(username, message):
    print(f"[{room.name}] {username}: {message}")

@room.on("user_joined", once=True)
def welcome_user(username):
    print(f"Welcome {username} to {room.name}!")

# Trigger events
room.user_join("Alice")
room.send_message("Alice", "Hello World!")
room.send_message("Bob", "Hi everyone!")
```

### Advanced Features

```python
@Listener
class DataProcessor:
    def __init__(self):
        self._addListenerDoc("data_received", "Process incoming data", "data: dict", "timestamp: float")
        self._addListenerDoc("error", "Handle processing errors", "error: Exception")
    
    def process(self, data):
        try:
            # Process data
            self._call("data_received", data, time.time())
        except Exception as e:
            self._call("error", e)

processor = DataProcessor()

# Async listener
@processor.on("data_received", is_async=True)
async def handle_data_async(data, timestamp):
    await asyncio.sleep(0.1)
    print(f"Async processing: {data} at {timestamp}")

# Error handler
def log_error(error):
    print(f"Error occurred: {error}")

@processor.on("error", on_error=log_error)
def handle_error(error):
    # This will trigger log_error if an exception occurs
    raise ValueError("Simulated error")

# One-time listener
@processor.on("data_received", once=True)
def initial_data_handler(data, timestamp):
    print(f"First data received: {data}")
```

### Documentation Generation

```python
@Listener
class MyComponent:
    def __init__(self):
        self._addListenerDoc("start", "Component started", "config: dict")
        self._addListenerDoc("stop", "Component stopped")
        self._addListenerDoc("data", "Data processed", "data: list", "metadata: dict")

component = MyComponent()

# Generate HTML documentation
html_docs = component.buildListenerDocs("html")
with open("docs.html", "w", encoding="utf-8") as f:
    f.write(html_docs)

# Generate Markdown documentation
md_docs = component.buildListenerDocs("markdown")
print(md_docs)
```

### Event Discovery

```python
# Analyze a class to discover all events
result = extract_listeners(ChatRoom)
print(f"Has @Listener decorator: {result['has_listener_decorator']}")
print(f"Events found: {result['events']}")
```

## 📖 API Reference

### @Listener Decorator
Transforms a class into an event listener system. Adds the following methods:

#### `addListener(event, func, is_async=False, once=False, on_error=None)`
Register a listener for an event.

**Parameters:**
- `event` (str): Event name
- `func` (callable): Callback function
- `is_async` (bool): Whether the function is async
- `once` (bool): Whether to trigger only once
- `on_error` (callable): Error callback function

#### `_call(event, *args, **kwargs)`
Trigger an event with arguments.

#### `on(event_name, is_async=False, once=False, on_error=None)`
Decorator version of `addListener`.

#### `_addListenerDoc(event, desc, *cpd)`
Add documentation for an event.

**Parameters:**
- `event` (str): Event name
- `desc` (str): Event description
- `*cpd` (str): Parameter descriptions

#### `buildListenerDocs(model="html")`
Generate documentation in HTML or Markdown format.

#### `_buildListenerDocs_html()` and `_buildListenerDocs_md()`
Internal methods for documentation generation.

### `extract_listeners(cls)`
Analyze a class to extract listener information.

**Returns:** Dict with keys:
- `events`: List of event names found
- `error`: Any error during extraction

## 🔧 Requirements

- Python 3.7+
- No external dependencies

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
3. Push to the branch (`git push origin main`)
4. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Bug Reports and Feature Requests

If you encounter any bugs or have feature requests, please open an issue on the [GitHub repository](https://github.com/qiufengcute/PyListenerTool).

## 🙏 Acknowledgments

- Thanks to all contributors who have helped shape this project
- Inspired by event-driven patterns in various frameworks

## 🌟 Support

If you find this package useful, please consider giving it a star on GitHub!