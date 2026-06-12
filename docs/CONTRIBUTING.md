# Contributing to Termux

## Shared Library

The [termux-shared](termux-shared) library (introduced in v0.109) defines shared constants and utilities for the Termux app and its plugins. It exists to eliminate hardcoded paths.

**Rules:**
- Never use hardcoded values. Use `TermuxConstants` from `termux-shared`
- Shared classes go under `com.termux.shared.termux` (Termux-specific) or the base package (general)
- Check and update the [termux-shared LICENSE](termux-shared/LICENSE.md) when contributing

Key classes:
- [`TermuxConstants`](https://github.com/termux/termux-app/blob/master/termux-shared/src/main/java/com/termux/shared/termux/TermuxConstants.java) — main constants, package name docs, forking info

See [Termux Libraries](https://github.com/termux/termux-app/wiki/Termux-Libraries) for importing in plugin apps.

## Versioning

`versionName` in `build.gradle` must follow [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html): `major.minor.patch(-prerelease)(+buildmetadata)`.

Always include the patch number in tags (e.g., `v0.1.0`, not `v0.1`). The build workflow validates this.

## Commit Messages

Commits **must** follow the [Conventional Commits](https://www.conventionalcommits.org) spec:

```
<type>[optional scope]: <description>

[optional body]
```

Rules:
- First letter of `type` and `description` must be capitalized
- Description in present tense
- Space after `:` is required
- For breaking changes, add `!` before `:`

**Allowed types:**

| Type | Meaning |
|------|---------|
| Added | New features |
| Changed | Changes to existing functionality |
| Deprecated | Soon-to-be-removed features |
| Removed | Removed features |
| Fixed | Bug fixes |
| Security | Vulnerability fixes |

Examples:
- `Added: Add floating terminal support`
- `Fixed(terminal): Fix paste crash with ESC characters`
- `Changed!: Remove sharedUserId (breaking change)`

## Forking

1. Check [`TermuxConstants`](https://github.com/termux/termux-app/blob/master/termux-shared/src/main/java/com/termux/shared/termux/TermuxConstants.java) javadocs for package name changes
2. Recompile the bootstrap zip for the new package name ([Building Packages](https://github.com/termux/termux-packages/wiki/Building-packages))
3. Some plugins still have hardcoded `com.termux` values — patch them manually
4. See [Forking and Local Development](https://github.com/termux/termux-app/wiki/Termux-Libraries#forking-and-local-development) for plugin library setup

## Sponsors and Funders

Termux is supported by:

- [GitHub Accelerator](https://github.com/accelerator)
- [GitHub Secure Open Source Fund](https://resources.github.com/github-secure-open-source-fund)
- [NLnet NGI Mobifree](https://nlnet.nl/mobifree)
- [Cloudflare](https://www.cloudflare.com)
