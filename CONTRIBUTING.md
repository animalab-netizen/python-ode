# Contributing

Thank you for contributing to `python-ode`.

## Validation

Run the package checks before sending changes:

```bash
python3 -m unittest discover /Users/caiosanchezchristino/Desktop/ode-projects/python-ode/tests
python3 -m pip wheel /Users/caiosanchezchristino/Desktop/ode-projects/python-ode --no-build-isolation --no-deps -w /tmp/python-ode-dist
```

## Guidance

- keep the public API small and explicit
- do not hide output delivery behind implicit exceptions-only flows
- prefer additive changes over breaking changes in runtime contracts
- keep examples aligned with the same ODE vocabulary used in the other language implementations
