# WDG Lab — Winding Design Laboratory
WDG Lab is a concise, developer-friendly toolkit for designing, analyzing, and visualizing electrical windings. It focuses on practical outputs for design validation, documentation, and quick iteration.

## Table of contents
- [Key features](#key-features)
- [Quick links](#quick-links)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Project layout](#project-layout)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Key features

- Stranded and hairpin winding generators
- Magnetic calculations: MMF, harmonics, and winding factors
- Slot current distribution and pin/connection details
- 2D visualization utilities for winding layouts and reports
- Example scripts and a lightweight web UI (see Quick links)

## Quick links

- Documentation: [docs/](docs/)
- Examples: [examples/](examples/)
- Web UI (optional): https://github.com/DawnEver/wdg-lab-webui

## Installation

Recommended: install from source (development mode).

1. Clone the repository

```bash
git clone https://github.com/your-org/wdg-lab.git
cd wdg-lab
```

2. Create and activate a virtual environment, uv is recommanded:
```bash
uv venv
# or use venv
pip -m venv .venv
```

3. Install the package
```bash
uv pip install -e . # for normal user
uv pip install -e ".[web]" # for web user
uv pip install -e ".[dev,web]" # for developer
```

## Quick start

- Generate a winding from parameters (examples include basic parameter sets):

```bash
python examples/gen_winding_from_params.py
```

- Generate a winding from winding configuration files:
```bash
python examples/gen_winding_from_toml.py
```

## Project layout

- `wdg_lab/` — core library modules and APIs
- `examples/` — runnable examples and small utilities
- `tests/` — unit tests and validation cases

## Contributing

Contributions, bug reports, and feature requests are welcome. To contribute:

1. Open an issue to discuss large changes.
2. Fork the repo and create a feature branch.
3. Add tests where applicable and follow the existing code style.
4. Open a pull request describing your change.

## License

This project is licensed under the Apache License, Version 2.0. See the full license in the LICENSE file or at https://www.apache.org/licenses/LICENSE-2.0

## Contact

For questions or collaboration, open an issue or contact the maintainers through the repository.
