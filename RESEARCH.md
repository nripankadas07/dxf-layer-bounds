# Research —18 October2026

User: CAD export maintainers checking a small planar model-space DXF.

Pain: A whole-drawing bounding box does not explain which layer/entity caused an extent, especially on an arc crossing zero degrees.

Smallest useful capability: Report per-layer two-dimensional LINE/CIRCLE/ARC bounds with explicit geometric evidence.

Acceptance: Correct line/circle/cardinal arc extents,350-to10-degree sweep and layer unions; reject3D, nondefault extrusion, inserts, malformed sections and duplicate geometry tags.

Demand is inferred from workflow and adjacent public discussions, not verified product requests. Discovery: descriptive GitHub topics, runnable invented example and chronological portfolio index. No unsolicited outreach or activity manipulation.

## Alternatives and evidence

Live GitHub repository search sorted Most stars: `DXF`. Highest-star relevant comparable found in the inspected scope: **LibreCAD/LibreCAD**. Search and reference-follow coverage is limited, not an exhaustive global ranking. Unrelated keyword matches were excluded.

| Repository | Stars observed | Last push UTC | Archived | API license |
| --- | ---: | --- | --- | --- |
| [LibreCAD/LibreCAD](https://github.com/LibreCAD/LibreCAD) | 6503 | 2026-10-17T17:16:37Z | False | NOASSERTION |
| [mozman/ezdxf](https://github.com/mozman/ezdxf) | 1479 | 2026-10-18T06:04:54Z | False | MIT |
| [LibreCAD/libdxfrw](https://github.com/LibreCAD/libdxfrw) | 294 | 2026-10-13T00:12:33Z | False | GPL-2.0 |

LibreCAD is a complete CAD application. Ezdxf already computes bounding boxes across far broader entity types, including transforms and curves. Libdxfrw provides broad DXF/DWG IO. This smaller strict report is a narrower interface, not an absent competitor feature.

Current README, selected relevant source and up to five issue/PR records were read. [Provenance](RESEARCH_PROVENANCE.json) preserves exact URLs, observations and source identities. NOASSERTION is unclassified licensing, not permission to copy. No third-party implementation or fixtures are bundled.

Our narrow Python wheel has a clean-install example and failure contract. Established alternatives provide broader workflows, capabilities, documentation, examples and support communities. Competitor installs, time to first useful result, reliability, support response and technical performance were not measured. Our examples prove only our specified behavior. Stars inform discovery, not quality or performance. No feature-absence or superiority claim is made.

Portfolio distinction: The owned OBJ island audit analyzes triangle edge topology in3D. This tool analyzes different file semantics, layer identities and planar primitive bounds; no shared product was subdivided.

Standard formats and algorithms are not inventions of this project; the implementation/report interface and invented fixtures are original. No branding or competitor prose is copied. No technical performance benchmark was conducted.
