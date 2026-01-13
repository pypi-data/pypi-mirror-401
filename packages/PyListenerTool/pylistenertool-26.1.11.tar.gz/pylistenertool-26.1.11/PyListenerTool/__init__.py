import ast
import asyncio
import inspect
import textwrap
import threading
from typing import Any, Callable, Type

__version__ = "26.01.11"


def Listener(cls: Type[Any]):
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        self._listeners = {}
        self._listener_docs = {}
        if original_init:
            original_init(self, *args, **kwargs)

    cls.__init__ = new_init

    def addListener(
        self,
        event: str,
        func: Callable[..., None],
        is_async: bool = False,
        once: bool = False,
        on_error: Callable[[Exception], None] = None,
    ):
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(
            {"func": func, "is_async": is_async, "once": once, "on_error": on_error}
        )

    cls.addListener = addListener

    def _call(self, event: str, *args, **kwargs) -> None:
        if event in self._listeners:
            del_count = 0
            for i, func_info in list(enumerate(self._listeners[event])):
                if func_info["once"]:
                    del self._listeners[event][i - del_count]
                    del_count += 1

                try:
                    if func_info["is_async"]:
                        threading.Thread(
                            target=lambda: asyncio.run(
                                func_info["func"](*args, **kwargs)
                            ),
                            daemon=False,
                        ).start()
                    else:
                        func_info["func"](*args, **kwargs)
                except Exception as e:
                    if func_info["on_error"]:
                        try:
                            func_info["on_error"](e)
                        except:
                            pass

    cls._call = _call

    def _addListenerDoc(self, event: str, desc: str, *cpd: str) -> None:
        self._listener_docs[event] = {"desc": desc, "cpd": cpd}

    cls._addListenerDoc = _addListenerDoc

    def _buildListenerDocs_html(self) -> str:
        container_html = ""
        for i, v in enumerate(self._listener_docs):
            param_html = ""
            for j, n in enumerate(self._listener_docs[v]["cpd"]):
                param_html += f"""
            <!-- {j+1}. {n} -->
            <div class="param">
                <span>{j+1}.</span>
                <span class="param-desc">{n}</span>
            </div>
"""

            if not param_html:
                param_html = """
            <!-- NULL -->
            <div class="param">
                <span><无></span>
            </div>
"""

            container_html += f"""
        <!-- {v} -->
        <div class="event">
            <h2 class="event-name">{v}</h2>
            <div class="event-desc">{self._listener_docs[v]["desc"]}</div>
            
            <div class="params-box">
                <div class="params-title">调用函数时传参：</div>
{param_html}
            </div>
        </div>
"""
            if i != len(self._listener_docs.keys()) - 1:
                container_html += """
        <!-- Divider -->
        <div class="divider"></div>
"""
        return f"""<!-- {cls.__name__} Listener Events Docs -->
<!-- Use @Listener auto generated -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{cls.__name__} Listener Events Docs</title>
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            margin: 40px; 
            background: #f5f5f5; 
        }}
        
        .event {{ 
            background: white; 
            padding: 20px; 
            margin-bottom: 20px; 
            border-radius: 5px; 
            box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
        }}
        
        .event-name {{ 
            color: #2c3e50; 
            font-size: 24px; 
            margin: 0 0 10px 0; 
            border-bottom: 2px solid #3498db; 
            padding-bottom: 5px; 
        }}
        
        .event-desc {{ 
            color: #555; 
            margin-bottom: 15px; 
        }}
        
        .params-box {{ 
            background: #f8f9fa; 
            border-left: 4px solid #3498db; 
            padding: 15px; 
            margin: 15px 0; 
        }}
        
        .params-title {{ 
            color: #2c3e50; 
            font-weight: bold; 
            margin-bottom: 10px; 
        }}
        
        .param {{ 
            margin: 8px 0; 
            padding-left: 15px; 
        }}
        
        .param-desc {{ 
            color: #555; 
        }}
        
        .divider {{ 
            height: 1px; 
            background: #ddd; 
            margin: 25px 0; 
        }}
        
        .event-count {{
            background: #A1ED1F;
            color: white;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 25px;
        }}
        
        .title {{
            color: #2c3e50;
            font-size: 32px;
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .footer {{
            text-align: center;
            color: #888;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }}
    </style>
</head>
<body>
    <h1 class="title">
        {cls.__name__} Listener Events Docs
        <span class="event-count">{len(self._listener_docs)} Events</span>
    </h1>
    <div class="container">
{container_html}
        <!-- No divider-->
    </div>
    <!-- Footer -->
    <div class="footer">
        Generated by @Listener
    </div>
</body>
</html>"""

    def _buildListenerDocs_md(self) -> str:
        container_md = ""
        for i, v in enumerate(self._listener_docs):
            param_md = ""
            for j, n in enumerate(self._listener_docs[v]["cpd"]):
                param_md += f"""
> **{j+1}**. {n}<br>"""

            if not param_md:
                param_md = "\n> **<无>**"

            container_md += f"""
## {v}
{self._listener_docs[v]["desc"]}
{param_md}
"""
            if i != len(self._listener_docs.keys()) - 1:
                container_md += """
---
"""
        return f"""# {cls.__name__} Listener Events Docs <{len(self._listener_docs)} Events>
{container_md}
---
**Generated by @Listener**"""

    def buildListenerDocs(self, model: str = "html") -> str:
        if model in ["markdown", "md"]:
            return _buildListenerDocs_md(self)
        else:
            return _buildListenerDocs_html(self)

    cls.buildListenerDocs = buildListenerDocs

    def on(
        self,
        event_name: str,
        is_async: bool = False,
        once: bool = False,
        on_error: Callable[[str], None] | None = None,
    ) -> None:
        def decorator(func: Callable[..., None]):
            self.addListener(event_name, func, is_async, once)
            return func

        return decorator

    cls.on = on

    return cls


def extract_listeners(cls: Type[Any]):
    result = {"events": [], "error": ""}

    try:
        source = textwrap.dedent(inspect.getsource(cls))
        tree = ast.parse(source)
    except Exception as e:
        result["error"] = e
        return result

    try:
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if (
                    isinstance(node.func, ast.Attribute)
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "self"
                    and (
                        node.func.attr == "_call" or node.func.attr == "_addListenerDoc"
                    )
                ):
                    if node.args and isinstance(node.args[0], ast.Constant):
                        event_name = node.args[0].value
                        if event_name not in result["events"]:
                            result["events"].append(event_name)
    except Exception as e:
        result["error"] = e
        return result

    return result
