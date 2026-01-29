CI and Release
==============

CI workflows
------------

The repository uses GitHub Actions to validate builds and publish release
artifacts.

- ``ci-release.yml`` runs tests, builds sdist/wheel, publishes to PyPI with
  ``twine``, and attaches artifacts to a GitHub Release when a tag is pushed.
  The extension demo wheels are built with ``cibuildwheel`` to produce
  manylinux-compatible tags.
- ``docs.yml`` builds Sphinx documentation on each push/PR to catch breakages.

Release flow
------------

1. Tag a release (for example, ``v1.2.3``).
2. Push the tag to GitHub.
3. CI builds packages and attaches artifacts to the GitHub Release.

Read the Docs
-------------

Read the Docs watches the default branch and renders documentation from the
``docs/`` folder. You can enable tag builds in the RTD project settings to
publish versioned docs such as ``/en/v1.2.3/``.
