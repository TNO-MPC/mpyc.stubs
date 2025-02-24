# TNO PET Lab - secure Multi-Party Computation (MPC) - MPyC - Stubs

This package contains stubs to use for type hinting [MPyC](https://github.com/lschoe/mpyc).

### PET Lab

The TNO PET Lab consists of generic software components, procedures, and functionalities developed and maintained on a regular basis to facilitate and aid in the development of PET solutions. The lab is a cross-project initiative allowing us to integrate and reuse previously developed PET functionalities to boost the development of new protocols and solutions.

The package `tno.mpc.mpyc.stubs` is part of the [TNO Python Toolbox](https://github.com/TNO-PET).

_Limitations in (end-)use: the content of this software package may solely be used for applications that comply with international export control laws._
_This implementation of cryptographic software has not been audited. Use at your own risk._

## Documentation

Documentation of the `tno.mpc.mpyc.stubs` package can be found
[here](https://docs.pet.tno.nl/mpc/mpyc/stubs/2.11.0).

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

When installing this package, the package is installed twice under two
different names:

- `mpyc-stubs`
- `tno.mpc.mpyc.stubs`

The `mpyc-stubs` installation is named as such by the convention
`<package>-stubs`, which allows static type tooling to easily pick up the
additional annotations. If you only use `MPyC` without defining custom MPyC
coroutines (usually decorated by `@asyncoro.mpc_coro` and
`asyncoro.mpc_coro_no_pc` in the MPyC source code), then this suffices.

The package `tno.mpc.mpyc.stubs` provides some convenience functions that help
you with writing custom, type-checked MPyC coroutines. Most importantly, MPyC's
decorator `@asyncoro.mpc_coro[_no_pc]` uses the type annotations of a function
to determine its MPyC `returnType`. However, this may be undesirable for more
complex functions. As such, `tno.mpc.mpyc.stubs` provides the following
top-level import:

- `mpc_coro_ignore` is a decorator that replaces `mpyc.asyncoro.mpc_coro` and
  avoids interference of type annotations with runtime behaviour. The `_ignore`
  part emphasizes that it ignores the type annotations at runtime. After
  stripping the type annotations, the decorator delegates the runtime logic to
  MPyC.

Additionally, the following top-level imports can be helpful:

- `returnType` replaces `mpyc.asyncoro.returnType` or equivalently
  `mpyc.runtime.Runtime.returnType`. We encountered various Mypy issues in the
  past when annotating `mpyc.runtime.Runtime.returnType` as it is appended to
  the class with `staticmethod()` and that did not preserve type overloads. As
  such, we provide `returnType` directly with proper type annotations. The
  function itself delegates behaviour to the MPyC counterpart.
- `BaseSecureFloat` is a type that represents secure floating point objects. It
  inherits from `mpyc.sectypes.SecureNumber`, and we make Mypy believe that
  both `mpyc.sectypes.SecureFloat` as well as our own
  `tno.mpc.mpyc.floating_point.SecureFloatingPoint` inherit from it. This way,
  the type annotations that we added will apply to both. If you develop MPyC
  coroutines that accept both secure floating point types, then you may use
  this class as a common ancestor.
