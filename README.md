# dxf-layer-bounds

Report per-layer two-dimensional LINE/CIRCLE/ARC bounds with explicit geometric evidence.

For: CAD export maintainers checking a small planar model-space DXF. A whole-drawing bounding box does not explain which layer/entity caused an extent, especially on an arc crossing zero degrees.

## Quickstart

Python3.10+; no runtime packages/network. Building the wheel needs setuptools from the normal Python registry.

```sh
git clone https://github.com/nripankadas07/dxf-layer-bounds.git
cd dxf-layer-bounds
python3 -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/dxf-layer-bounds example.dxf
```

Exit 0: cut layer bounds are [-2,0,3,4]; reference circle bounds are [9,9,11,11]. Three entities on two layers.

Windows equivalents use `.venv\Scripts\python.exe` and `.venv\Scripts\dxf-layer-bounds.exe`; Windows/macOS have not been executed by this release's Linux CI.

## Contract

ASCII DXF with one ENTITIES section and complete section/EOF structure. Only LINE,CIRCLE,ARC in model space with zero Z/thickness and default extrusion. Arc sweeps are counterclockwise, normalized modulo360 and include endpoints plus cardinal extrema. Full/zero-turn arcs are rejected: use CIRCLE. All entities, including invisible ones, contribute raw geometry. Per-layer counts, bounds and approximate total lengths retain entity evidence; zero-length LINE is an exit1 finding.

Report JSON goes to stdout. Exit0 means a valid report without documented findings, exit1 a valid report with findings, exit2 invalid/unsupported input or I/O failure with stderr and no partial report. This is a bounded read-only inspection tool; the optional example generator only creates an explicitly named new file.

## Limits

2 MiB,50000 code/value pairs,10000 entities,256 layers,128-character layer names,1024-character tag values; finite coordinate/angle absolute magnitude<=1e9. Other sections are counted and ignored. Unsupported entities, transforms, duplicate geometry fields, layouts and missing coordinates fail explicitly. No blocks, polylines, text, clipping, units conversion, repair or manufacturing certificate. Bounds/lengths use floating point.

## Verify

```sh
python3 -m unittest -v test_behavior
python3 -m compileall -q .
python3 -m pip wheel --no-deps --wheel-dir dist .
python3 -m venv /tmp/dxf-layer-bounds-check
/tmp/dxf-layer-bounds-check/bin/python -m pip install --no-deps dist/*.whl
python3 verify_installed.py /tmp/dxf-layer-bounds-check/bin/python
```

Installed-command checks run outside the checkout. See [validation](VALIDATION.md), [research](RESEARCH.md), [contributing](CONTRIBUTING.md), [support](SUPPORT.md), [security](SECURITY.md) and [license](LICENSE).

Original implementation, prose and invented fixtures developed with AI assistance. MIT license. No verified production adoption or performance-superiority claim.
