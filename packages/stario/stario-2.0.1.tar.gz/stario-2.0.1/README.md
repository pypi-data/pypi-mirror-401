<p align="center">
  <picture>
    <img alt="stario-logo" src="https://raw.githubusercontent.com/bobowski/stario/main/docs/img/stario.png" style="height: 200px; width: auto;">
  </picture>
</p>

<p align="center">
  <em>Real-time hypermedia for Python 3.14+</em>
</p>

---

**Documentation**: [stario.dev](https://stario.dev) · **Source**: [github.com/bobowski/stario](https://github.com/bobowski/stario)

---

## What is Stario?

Stario is a Python web framework for **real-time hypermedia**. While most frameworks treat HTTP as request → response, Stario treats connections as ongoing conversations — open an SSE stream, push DOM patches, sync reactive signals.

## Why Stario?

- **Real-time first** — SSE streaming, DOM patching, reactive signals built-in
- **Hypermedia** — Native [Datastar](https://data-star.dev/) integration, no JavaScript frameworks needed
- **Simple** — Go-style handlers `(Context, Writer) → None`
- **Fast** — Built on `httptools` with zstd/brotli/gzip compression

## Example: Multiplayer Counter

A real-time counter in a single file:

```python
import asyncio
from stario import Stario, Context, Writer, Relay, RichTracer
from stario.html import Div, Button, H1
from stario.datastar import data, at

relay = Relay()
count = 0

async def home(c: Context, w: Writer) -> None:
    w.html(
        Div({"id": "app"},
            data.signals({"count": count}),
            data.init(at.get("/stream")),
            H1("Multiplayer Counter"),
            Div({"id": "count"}, data.text("$count"), str(count)),
            Button(data.on("click", at.post("/inc")), "+1"),
        )
    )

async def stream(c: Context, w: Writer) -> None:
    w.sync({"count": count})
    async for _ in w.alive(relay.subscribe("counter")):
        w.sync({"count": count})

async def increment(c: Context, w: Writer) -> None:
    global count
    count += 1
    w.empty()
    relay.publish("counter", None)

async def main():
    with RichTracer() as tracer:
        app = Stario(tracer)
        app.get("/", home)
        app.get("/stream", stream)
        app.post("/inc", increment)
        await app.serve()

if __name__ == "__main__":
    asyncio.run(main())
```

## Get Started

Install with `uv add stario` or `pip install stario`, then run `stario init` to create a new project. Requires **Python 3.14+**.

See the [documentation](https://stario.dev) for tutorials, API reference, and how-to guides.

---

<p align="center"><em>Stario: Real-time hypermedia, made simple.</em></p>
