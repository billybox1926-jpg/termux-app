# Termux Application

[![Build status](https://github.com/termux/termux-app/workflows/Build/badge.svg)](https://github.com/termux/termux-app/actions)
[![Testing status](https://github.com/termux/termux-app/workflows/Unit%20tests/badge.svg)](https://github.com/termux/termux-app/actions)
[![Discord](https://img.shields.io/discord/641256914684084234.svg?label=&logo=discord&logoColor=ffffff&color=5865F2)](https://discord.gg/HXpF69X)

[Termux](https://termux.dev) is an Android terminal application and Linux environment.

This repository is for the app itself (terminal emulation and UI). For installable packages, see [termux/termux-packages](https://github.com/termux/termux-packages).

## Contents

- [Installation](#installation)
- [Uninstallation](#uninstallation)
- [Plugins](#plugins)
- [Documentation](#documentation)
- [Contributing](#contributing)

## Installation

Latest version: **v0.118.3** (or higher — required for security fixes).

Termux requires **Android >= 7**. Choose one source and stick with it — APKs from different sources cannot be mixed (different signing keys).

### F-Droid (Recommended)

Get it from [f-droid.org](https://f-droid.org/en/packages/com.termux/). Updates lag GitHub by a few days. Universal APK only (~180MB).

### GitHub (Latest)

Get it from [GitHub Releases](https://github.com/termux/termux-app/releases) or [Build Actions](https://github.com/termux/termux-app/actions/workflows/debug_build.yml). Both universal and architecture-specific APKs (~120MB).

> **Security warning:** GitHub builds are signed with a public test key. Only download from the official repo. Builds from Telegram or social media may be malicious.

### Google Play (Experimental)

An experimental build for Android 11+ exists on the Play Store. It has missing features and bugs compared to F-Droid/GitHub. Report issues to [termux-play-store](https://github.com/termux-play-store/termux-issues/issues/new/choose), not here.

## Uninstallation

To switch sources or remove Termux completely, uninstall **all** Termux-related APKs (app + any plugins) from Android Settings → Applications, then reinstall from the new source.

## Plugins

Optional companion apps that extend Termux:

| Plugin | Purpose |
|--------|---------|
| [Termux:API](https://github.com/termux/termux-api) | Android system APIs from the command line |
| [Termux:Boot](https://github.com/termux/termux-boot) | Run scripts at device boot |
| [Termux:Float](https://github.com/termux/termux-float) | Floating terminal window |
| [Termux:Styling](https://github.com/termux/termux-styling) | Custom fonts and color schemes |
| [Termux:Tasker](https://github.com/termux/termux-tasker) | Tasker automation integration |
| [Termux:Widget](https://github.com/termux/termux-widget) | Home screen script shortcuts |

All plugins must be installed from the **same source** as the main app.

## Documentation

- [User docs](docs/en/index.md) — debugging, log levels, issue reporting, Android 12+ notes
- [Termux Wiki](https://wiki.termux.com/wiki/)
- [FAQ](https://wiki.termux.com/wiki/FAQ)
- [Package Management](https://wiki.termux.com/wiki/Package_Management)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for commit conventions, forking instructions, and development guidelines.
