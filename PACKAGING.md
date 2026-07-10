# Shipping Lispr Flow on Ubuntu

This is an Ubuntu-first plan that keeps the application portable to other Linux distributions.

## The layers

1. **PySide6 application:** `main.py` is the app source code.
2. **`pyside6-deploy`:** the Qt-provided deployment tool compiles the app with Nuitka and collects the Qt runtime into a runnable Linux build.
3. **Debian package (`.deb`):** installs that app into the normal Ubuntu locations, adds a launcher, and provides clean uninstall support.

Users should install the `.deb`; they should not need Python or `pip`.

## Development versus release

During development, run:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py
```

For a release build, use a clean Ubuntu machine or container matching the oldest Ubuntu version you promise to support. Linux binaries are not reliably cross-built from macOS or Windows.

## First release path

Use the deployment command bundled with PySide6. The first command creates a small `pysidedeploy.spec` release configuration:

```bash
.venv/bin/pyside6-deploy main.py --init
```

In that file, set the title to `Lispr Flow`, add the app icon once it exists, and choose `standalone` mode for the first builds. Then build:

```bash
.venv/bin/pyside6-deploy -c pysidedeploy.spec
```

`pyside6-deploy` uses Nuitka to compile the Python application and gathers the Qt files it needs. Start with its `standalone` directory mode: it is much easier to inspect and debug than a single-file executable. Run the resulting application and test it on a second Ubuntu user account or VM.

Then place the tested build under `/opt/lispr-flow`, add a desktop entry under `/usr/share/applications`, and build a `.deb` package. We should automate that in a small release script once the application has real audio, authentication, and update behavior to test.

## Later distribution options

- **AppImage:** one downloadable file. Good for users on many distributions and for early testing.
- **Flatpak:** stronger sandboxing and a good cross-distro desktop experience, but it adds portal and permission work for microphone access.
- **Snap:** convenient on Ubuntu but more opinionated about sandboxing and startup behavior.

Recommendation: release a signed `.deb` first for Ubuntu, then add an AppImage for broader Linux testing. Consider Flatpak once microphone permissions and automatic updates are mature.

## Stability checklist

- Build and test on Ubuntu, including the oldest supported Ubuntu release.
- Bundle fonts and verify the app opens without a developer environment.
- Test microphone permission, global shortcut, login browser hand-off, offline state, and upgrade/uninstall once those features exist.
- Keep user data in the platform data directory, never beside the installed binary.
- Produce a versioned changelog and checksum for every release.
