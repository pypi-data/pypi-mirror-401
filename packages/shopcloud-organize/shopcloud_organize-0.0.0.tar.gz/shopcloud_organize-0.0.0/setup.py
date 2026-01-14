#!/usr/bin/env python3
# This setup.py file is a simple shim to support legacy installation methods
# The real package configuration is in pyproject.toml

from setuptools import setup

if __name__ == "__main__":
    setup(
        use_scm_version={
            "local_scheme": "no-local-version",
            "fallback_version": "1.8.0",
        },
    )
