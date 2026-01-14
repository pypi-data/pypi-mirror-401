# gen-commit

Generate concise, descriptive Git commit messages using Groq LLMs.

## Features
- Produce context-aware commit message suggestions from staged changes.
- Simple CLI workflow that fits into existing git usage.
- Configurable via environment variables.

## Requirements
- Python 3.8+
- A valid GROQ API key

## Install
```bash
pip install gen-commit-cli
```

## Quickstart
1. Stage your changes:
```bash
git add .
```
2. Generate a commit message:
```bash
gen-commit
```
3. Use the suggested message for committing:
```bash
git commit -m "feat: add user authentication flow"
```

## Configuration
Set your Groq API key in the environment:
```bash
export GROQ_API_KEY=sk-xxxx
```
For help and available options:
```bash
gen-commit --help
```

## Troubleshooting
- "Invalid API key" — verify GROQ_API_KEY is set and correct.
- "No staged files" — ensure you ran `git add` before generating a message.

## Contributing
Contributions, issues and feature requests are welcome via the project repository.

## License
Specify your project's license (e.g., MIT) in the repository root.
