# must-gather-parser
Asyncrhonous (multi) must-gather parser library.
```python
import asyncio
from must_gather_parser import MustGather
import json

must_gather = MustGather()

async def main():
    try:
        must_gather.use("/home/must-gather.local.1972254135986597168")
        x = await must_gather.get_resources(resource_kind_plural="pods", group="core", all_namespaces=True)
        print(json.dumps(x))
    except:
        must_gather.close()


if __name__ == "__main__":
    asyncio.run(main())
```