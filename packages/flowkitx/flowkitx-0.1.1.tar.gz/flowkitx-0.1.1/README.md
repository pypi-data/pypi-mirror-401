# 🚀 **FlowKitX - Simplify Async Workflows**

[![PyPI version](https://badge.fury.io/py/flowkitx.svg)](https://badge.fury.io/py/flowkitx)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/flowkit/flowkit/actions/workflows/publish.yml/badge.svg)](https://github.com/flowkit/flowkit/actions)

> **FlowKitX provides fluent async workflows with lazy execution and minimal boilerplate.**

## ⚡ **Why FlowKitX?**

**Before (Traditional Async):**
```python
async def fetch_user_data(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.example.com/users/{user_id}") as response:
            user = await response.json()
            async with session.get("https://api.example.com/posts", params={"userId": user_id}) as posts_response:
                posts = await posts_response.json()
                return {"user": user, "posts": posts}
```

**After (FlowKitX):**
```python
@flowkit.simple
def fetch_user_data(user_id):
    user = flowkit.get(f"https://api.example.com/users/{user_id}").json()
    posts = flowkit.get("https://api.example.com/posts", params={"userId": user_id}).json()
    return {"user": user, "posts": posts}
```

## 🎯 **Key Features**

- 🔗 **Fluent API** - Chain operations with `.pipe()` method
- 🛡️ **Type Safe** - Full IDE support and type hints
- 🚀 **Modern Foundation** - Built on battle-tested httpx
- 🔧 **Framework Ready** - FastAPI, Django, Flask examples
- 📦 **Simple Installation** - `pip install flowkitx`

## 📦 **Installation**

```bash
pip install flowkitx
```

## 🔧 **How FlowKitX Works**

FlowKitX provides lazy async pipelines - operations are queued and executed when awaited.

```python
import flowkit

# FlowKitX operations return awaitable Flow objects
user_flow = flowkit.get("https://api.example.com/users/1")
posts_flow = flowkit.get("https://api.example.com/posts")

# Execute both operations
user = await user_flow.json()
posts = await posts_flow.json()
```

### **Core Concept: Flow Objects**
Flow objects are awaitable pipelines that:
- Chain operations without immediate execution
- Execute when awaited in the current event loop
- Enable fluent, readable async patterns

**This is structured async workflows, not sync-to-async magic.**

## 🏆 **Real-World Examples**

### **Data Processing Pipeline**
```python
@flowkit.simple
def fetch_user_data(user_id: int):
    """Fetch and process user data."""
    return (flowkit.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
              .json()
              .pipe(lambda user: {**user, "processed": True}))
```

### **Concurrent Operations**
```python
@flowkit.simple
def fetch_dashboard():
    """Fetch multiple data sources concurrently."""
    users = flowkit.get("https://jsonplaceholder.typicode.com/users").json()
    posts = flowkit.get("https://jsonplaceholder.typicode.com/posts").json()
    comments = flowkit.get("https://jsonplaceholder.typicode.com/comments").json()
    
    # These execute concurrently when awaited
    return {"users": users, "posts": posts, "comments": comments}
```

## 🛠 **When to Use FlowKitX**

FlowKitX is ideal for:
- API-heavy applications with multiple calls
- Data pipelines and processing workflows
- Teams wanting consistent async patterns
- Rapid prototyping with clean syntax

## ⚠️ **Important Notes**

FlowKitX does NOT:
- Block the event loop or use thread pools
- Make synchronous code magically non-blocking  
- Replace understanding of asyncio fundamentals
- Work with CPU-bound operations

Always use async/await with CPU-intensive tasks.

## 🆚 **How FlowKitX Compares**

| Feature | FlowKitX | aiohttp | httpx | requests |
|---------|---------|---------|-------|----------|
| Fluent API | ✅ | ❌ | ❌ | ❌ |
| Type Safe | ✅ | ✅ | ✅ | ✅ |
| Sessions | ✅ | ✅ | ✅ | ❌ |
| Pipelines | ✅ | ❌ | ❌ | ❌ |

FlowKitX provides **structured async workflows** with minimal overhead.

## 📋 **License**

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

---

**🚀 Try FlowKitX today for cleaner async workflows:**

```bash
pip install flowkitx
```

**⭐ Star us on GitHub!** [github.com/flowkit/flowkit](https://github.com/flowkit/flowkit)