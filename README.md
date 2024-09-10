# TNO PET Lab - secure Multi-Party Computation (MPC) - MPyC - Stubs

This package contains stubs to use for type hinting [MPyC](https://github.com/lschoe/mpyc).

### PET Lab

The TNO PET Lab consists of generic software components, procedures, and functionalities developed and maintained on a regular basis to facilitate and aid in the development of PET solutions. The lab is a cross-project initiative allowing us to integrate and reuse previously developed PET functionalities to boost the development of new protocols and solutions.

The package `tno.mpc.mpyc.stubs` is part of the [TNO Python Toolbox](https://github.com/TNO-PET).

_Limitations in (end-)use: the content of this software package may solely be used for applications that comply with international export control laws._  
_This implementation of cryptographic software has not been audited. Use at your own risk._

## Documentation

Documentation of the `tno.mpc.mpyc.stubs` package can be found
[here](https://docs.pet.tno.nl/mpc/mpyc/stubs/2.6.2).

## Install

Easily install the `tno.mpc.mpyc.stubs` package using `pip`:

```console
$ python -m pip install tno.mpc.mpyc.stubs
```

_Note:_ If you are cloning the repository and wish to edit the source code, be
sure to install the package in editable mode:

```console
$ python -m pip install -e 'tno.mpc.mpyc.stubs'
```

If you wish to run the tests you can use:

```console
$ python -m pip install 'tno.mpc.mpyc.stubs[tests]'
```

## Usage

### Structure of the Package

When installing this package, the package is actually installed twice under two
different names:
 - `tno.mpc.mpyc.stubs`
 - `mpyc-stubs`

By convention, stubs packages should be named `<package>-stubs`, such that they
can easily be picked up by tooling.

Some of our other packages also directly depend on the types and utilities
provided by this repository. Therefore, `tno.mpc.mpyc.stubs` can also be
installed.

