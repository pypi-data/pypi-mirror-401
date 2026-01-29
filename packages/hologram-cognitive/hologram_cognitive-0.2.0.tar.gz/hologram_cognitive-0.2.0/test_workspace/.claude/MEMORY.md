# Memory System Active

This folder contains portable AI working memory powered by `hologram-cognitive`.

## Quick Start
```python
import hologram

session = hologram.Session('.claude')
result = session.turn("your message")
print(result.injection)
session.save()
```

## CLI
```bash
hologram route .claude "your message"
hologram status .claude
```

## Links
Add `[[wiki-links]]` in your .md files to build the knowledge graph.
