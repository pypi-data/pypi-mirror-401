# ⚠️ DEPRECATED - Use `aisentry` instead

**This package has been renamed to `aisentry`.**

## Migration

```bash
pip uninstall ai-security-cli
pip install aisentry
```

## New Usage

```bash
# Old (deprecated)
ai-security-cli scan ./my-project

# New
aisentry scan ./my-project
aisentry audit ./my-project
aisentry test -p openai -m gpt-4
```

## Links

- **New Package**: https://pypi.org/project/aisentry/
- **GitHub**: https://github.com/deosha/aisentry
- **Website**: https://aisentry.co
