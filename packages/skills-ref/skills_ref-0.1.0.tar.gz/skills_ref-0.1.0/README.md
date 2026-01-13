# Agent Skills

[Agent Skills](https://agentskills.io) are a simple, open format for giving agents new capabilities and expertise.

Skills are folders of instructions, scripts, and resources that agents can discover and use to perform better at specific tasks. Write once, use everywhere.

## Installation

```bash
pip install skills-ref
```

Or using [uv](https://docs.astral.sh/uv/):

```bash
uv add skills-ref
```

## Quick Start

### CLI Usage

```bash
# Validate a skill
agentskills validate path/to/skill

# Read skill properties (outputs JSON)
agentskills read-properties path/to/skill

# Generate <available_skills> XML for agent prompts
agentskills to-prompt path/to/skill-a path/to/skill-b
```

### Python API

```python
from pathlib import Path
from agentskills import validate, read_properties, to_prompt

# Validate a skill directory
errors = validate(Path("my-skill"))
if errors:
    print("Validation errors:", errors)
else:
    print("Valid skill!")

# Read skill properties
props = read_properties(Path("my-skill"))
print(f"Skill: {props.name}")
print(f"Description: {props.description}")

# Generate prompt XML for agent integration
prompt = to_prompt([Path("skill-a"), Path("skill-b")])
print(prompt)
```

## Features

- **Validation**: Check skills for proper format and required fields
- **Parsing**: Extract skill metadata from SKILL.md frontmatter
- **Prompt Generation**: Create XML blocks for agent system prompts
- **i18n Support**: Full Unicode support for international skill names
- **CLI Tools**: Command-line utilities for skill management

## Documentation

- [Full Documentation](https://agentskills.io) - Guides and tutorials
- [Specification](https://agentskills.io/specification) - Format details
- [Example Skills](https://github.com/anthropics/skills) - See what's possible

## About

Agent Skills is an open format maintained by [Anthropic](https://anthropic.com) and open to contributions from the community.

## License

Apache 2.0