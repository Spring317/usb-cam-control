# FastAPI & Camera Control Technical Architecture (LaTeX & PDF)

This directory contains formal technical documentation detailing low-level **data acquisition mechanisms** (PTP over USB, buffer extraction, memory retrieval) and standardized **UML Diagrams** (Use Case and Sequence Diagrams) for the **Canon EOS R8 USB Control Application**.

## Files in this Directory

- **`main.tex`**: The primary LaTeX document source file containing architectural topology diagrams, TikZ UML Use Case diagrams, TikZ UML Sequence diagrams for full data acquisition, C-Python memory retrieval patterns, and MJPEG preview generator dynamics.
- **`main.pdf`**: The compiled 5-page PDF document.
- **`README.md`**: Overview and build instructions.

## Key Diagrams & Sections

1. **Figure 1: Architectural Data Flow Topology:** Maps interactions across Browser Frontend, FastAPI API Layer, CameraController Mutex Wrapper, `libgphoto2` Drivers, and Canon Hardware.
2. **Figure 2: UML Use Case Diagram:** Standardized UML diagram outlining System Boundary (`FastAPI Camera Control Application`), Actors (`User/Web UI`, `Canon EOS R8 Camera`, `Linux V4L2 Subsystem`), and functional use cases with `<<include>>` and `<<extend>>` relationships.
3. **Figure 3: UML Sequence Diagram (Full Data Acquisition):** Comprehensive 4-lifeline UML sequence diagram showing message calls (`POST /api/capture`, `acquire(lock)`, `set_config(viewfinder=0)`, `capture(GP_CAPTURE_IMAGE)`, `file_get()`, `release(lock)`).
4. **Data Acquisition Mechanisms:** Low-level breakdown of USB Bulk IN payload retrieval, `capturetarget = 1` SDRAM buffering, and `capture_preview()` MJPEG stream encapsulation.

## Compiling the LaTeX Source

To recompile `main.tex` into `main.pdf`, run:

```bash
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```
