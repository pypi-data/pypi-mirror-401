# pkgstats - Debian Package Statistics Tool

A Python command-line tool to analyze Debian packages installations details.

## Implementation

### Requirements
No requirements needed to install.

### Features

#### Package popularity statistics - based on Popcon

For each Debian package, the tool retrieves and exposes Popularity Contest (Popcon) metrics:
- Installed systems (inst)
- Votes (vote) – actively used packages
- Recent installs
- Old / unused installs
- Packages with missing files (no-files)
- Total installs

These values give insight into how widely used and how actively maintained a package is across Debian systems.

#### Package metadata and repository information

By scanning Debian repository metadata, the tool also extracts:
- Global rank
- Maintainer
- Available architectures (e.g. amd64, arm64, armhf, …) for the package


### Command-Line Options
| Option  	| Description   |
|---------- |:--------------|
| package   | Package to analyze |


### Organization

The code is organizzed as follows.
```
project/
├── pyproject.toml    <-- Configuration file
├── package_statistics.py <-- For standalone execution
├── README.md
├── src/
    ├── pkgstats/
        ├── __init__.py
        ├── model.py        <-- Data model
        ├── parse.py        <-- Parse data
│       └── pkgstats.py     <-- Contains logic and cli
└── tests/
    ├── __init__.py
    └── test_pkgstats.py  <-- Unittest file
```

### License

MIT License. Free to use and modify.

## Testing

```bash
python3 -m unittest tests/test_pkgstats.py
# or
python3 -m unittest discover tests
```

## Usage

### With Package Installation

To install for development in editable mode:
```bash
pip3 install -e .
```

To build the distribution files and install the package:
```bash
pip3 install build
python3 -m build
pip3 install dist/pkgstats-<version>-py3-none-any.whl 
```

Then you can directly use:
```bash
$ pkgstats -h # to list the psosiible options
$ pkgstats dpkg # to get the first 10 packages
```
Output example:
```yml
📦 Package: dpkg
Maintainer: Dpkg Developers
Rank position: 1
Available Architectures: amd64, arm64, armel, armhf, i386, ppc64el, riscv64, s390x

Popularity Data:
N. of users with regular usage: 241681
N. of old installs (no regular usage): 9912
N. of recent upgrades: 19258
Entry with no info (atime = ctime = 0): 39

➡️  Total installs of dpkg: 270890
```

### No Package Installation

Use the command to get the results without build/install anything.

```bash
$ ./package_statistics.py amd64   # to get the first 10 packages
$ ./package_statistics.py amd64 -n 20 # to get the first 20
```

## Validate

The code has been verified to check if compliant.

### black – Code formatter (auto-fix)

Automatically formats the code according to standard style PEP8.

```bash
$ pip3 install black && black pkgstats/ tests/

All done! ✨ 🍰 ✨
7 files left unchanged.
```

### flake8 – Python style checker

Check PEP8 style violations, undefined names, line lengths, spaces and so on.

``` bash
$ pip3 install flake8 && flake8 pkgstats/ tests/
```

### Ruff

Linter and formatter that catchs import errors and style issues.

```bash
$ pip3 install ruff && ruff check .

Collecting ruff
  Using cached ruff-0.14.11-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (26 kB)
Using cached ruff-0.14.11-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (13.8 MB)
Installing collected packages: ruff
Successfully installed ruff-0.14.11
All checks passed!
```

### MyPy

A static type checker to check if assignment are correct.

```bash
$ pip3 install mypy && mypy pkgstats tests/test_pkgstats.py 

Requirement already satisfied: mypy in ./.venv/lib/python3.13/site-packages (1.19.1)
Requirement already satisfied: typing_extensions>=4.6.0 in ./.venv/lib/python3.13/site-packages (from mypy) (4.15.0)
Requirement already satisfied: mypy_extensions>=1.0.0 in ./.venv/lib/python3.13/site-packages (from mypy) (1.1.0)
Requirement already satisfied: pathspec>=0.9.0 in ./.venv/lib/python3.13/site-packages (from mypy) (1.0.3)
Requirement already satisfied: librt>=0.6.2 in ./.venv/lib/python3.13/site-packages (from mypy) (0.7.7)
Success: no issues found in 6 source files
```

### Validate-project 

A tool to ensure the `pyproject.toml` file follows the standards PEPs.

```bash
$ pip3 install validate-pyproject && validate-pyproject pyproject.toml

Valid file: pyproject.toml
```

### Py-Spy - profiler

A low-overhead sampling profiler for Python to visualize what the Python program is spending time on without restarting the program or modifying the code.

```bash
$ pip3 install py-spy
$ py-spy top -- python package_statistics.py amd

Collecting samples from 'python package_statistics.py amd64' (python v3.13.5)
Total Samples 200
GIL: 61.00%, Active: 96.00%, Threads: 1

  %Own   %Total  OwnTime  TotalTime  Function (filename)                                                                                                                                                      
 44.00%  44.00%   0.440s    0.440s   parse_contents_index (pkgstats/pkgstats.py)
  1.00%   1.00%   0.320s    0.320s   readinto (socket.py)
 29.00%  32.00%   0.290s    0.320s   read (gzip.py)
 18.00%  18.00%   0.180s    0.180s   write_bytes (pathlib/_abc.py)
  3.00%  32.00%   0.030s    0.320s   readall (_compression.py)
  0.00%   0.00%   0.020s    0.030s   create_connection (socket.py)
  0.00%   0.00%   0.020s    0.020s   _compile (re/_compiler.py)
  0.00%   0.00%   0.010s    0.010s   load_default_certs (ssl.py)
  0.00%   0.00%   0.010s    0.060s   _call_with_frames_removed (<frozen importlib._bootstrap>)
  0.00%   0.00%   0.010s    0.010s   _get_module_lock (<frozen importlib._bootstrap>)
  0.00%   0.00%   0.010s    0.020s   <module> (pathlib/_local.py)
  0.00%   0.00%   0.010s    0.030s   <module> (pathlib/__init__.py)
  1.00%  52.00%   0.010s    0.870s   download_contents_file (pkgstats/pkgstats.py)
  0.00%   0.00%   0.010s    0.010s   getaddrinfo (socket.py)
```


# Uninstall
```bash
pip3 uninstall pkgstats -y
rm -rf dist/ *.egg-info
```

