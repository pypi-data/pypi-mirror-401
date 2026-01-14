# matomo-core

[![PyPI version](https://img.shields.io/pypi/v/matomo-core/0.3.2.svg)](https://pypi.org/project/matomo-core/)
[![PyPI License](https://img.shields.io/pypi/l/matomo-core/0.3.2.svg)](https://pypi.org/project/matomo-core/)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/matomo-core/0.3.2.svg)](https://pypi.org/project/matomo-core/)
[![Docs](https://img.shields.io/badge/docs-readthedocs-red.svg?style=flat-square)](https://matomo-core.readthedocs.io)

[![Maturity badge - level 3](https://img.shields.io/badge/Maturity-Level%203%20--%20Stable-green.svg)](https://github.com/spraakbanken/getting-started/blob/main/scorecard.md)
[![Stage](https://img.shields.io/pypi/status/matomo-core/0.3.2.svg)](https://pypi.org/project/matomo-core/)

[![Code Coverage](https://codecov.io/gh/spraakbanken/matomo-core/branch/main/graph/badge.svg)](https://codecov.io/gh/spraakbanken/matomo-core/)

[![CI(check)](https://github.com/spraakbanken/matomo-core/actions/workflows/check.yml/badge.svg)](https://github.com/spraakbanken/matomo-core/actions/workflows/check.yml)
[![CI(release)](https://github.com/spraakbanken/matomo-core/actions/workflows/release.yml/badge.svg)](https://github.com/spraakbanken/matomo-core/actions/workflows/release.yml)
[![CI(rolling)](https://github.com/spraakbanken/matomo-core/actions/workflows/rolling.yml/badge.svg)](https://github.com/spraakbanken/matomo-core/actions/workflows/rolling.yml)
[![CI(test)](https://github.com/spraakbanken/matomo-core/actions/workflows/test.yml/badge.svg)](https://github.com/spraakbanken/matomo-core/actions/workflows/test.yml)

Library for working with Matomo.

## MatomoCore

Business logic for tracking backend calls with Matomo.

Used by [flask-matomo2](https://github.com/spraakbanken/flask-matomo2) and [asgi-matomo](https://github.com/spraakbanken/asgi-matomo).

## trackers

Trackers to record time for different parts of a request.

### PerfMsTracker

A context manager for recording time in milliseconds.
