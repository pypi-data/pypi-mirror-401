# Contributing

Thank you for your interest.

## Important: CLA required
All contributions require a signed CLA (see `CLA.md`) **before** a pull request can be merged.

## Development setup
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U pip
pip install -e ".[dev]"
pytest
```

## Code style
- Keep functions small and documented.
- Add tests for bug fixes or new features.

## License
By contributing, you agree your contributions may be released under the AGPL-3.0-or-later and also under commercial terms by the Maintainer.
