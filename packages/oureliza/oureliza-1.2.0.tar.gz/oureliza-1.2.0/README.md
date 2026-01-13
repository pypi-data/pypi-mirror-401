# Our Eliza (oureliza)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/oureliza.svg)](https://pypi.org/project/oureliza/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A minimal Python implementation of the classic ELIZA chatbot with zero dependencies.

## Installation

```bash
pip install oureliza
```

Or with Poetry:

```bash
poetry add oureliza
```

## Usage

```python
from oureliza import Eliza

eliza = Eliza()

# Get initial greeting
print(eliza.initial())

# Have a conversation
print(eliza.respond("I feel sad today"))
print(eliza.respond("My mother never understood me"))
print(eliza.respond("I dream about flying"))

# Get final message
print(eliza.final())
```

## Script Format

ELIZA uses a script-based pattern matching system designed by Joseph Weizenbaum in 1966. See [SCRIPT_FORMAT.md](SCRIPT_FORMAT.md) for full history and specification.

The built-in `DOCTOR_SCRIPT` follows this format:

### Tags

| Tag | Description | Example |
|-----|-------------|---------|
| `initial` | Greeting messages shown at start | `initial: How do you do. Please tell me your problem.` |
| `final` | Goodbye messages shown at end | `final: Goodbye. Thank you for talking to me.` |
| `quit` | Words that end the conversation | `quit: bye` |
| `pre` | Pre-substitution (before matching) | `pre: dont don't` |
| `post` | Post-substitution (in responses) | `post: i you` |
| `synon` | Synonym groups | `synon: sad unhappy depressed` |
| `key` | Keyword with optional weight | `key: mother 10` |
| `decomp` | Decomposition pattern | `decomp: * i feel *` |
| `reasmb` | Reassembly response | `reasmb: Why do you feel (2)?` |

### Pattern Matching

- `*` matches zero or more words
- `@word` matches any synonym in the group
- `(1)`, `(2)`, etc. reference captured groups from decomposition

### Example Script Block

```
key: mother 10
  decomp: * my mother *
    reasmb: Tell me more about your mother.
    reasmb: What else comes to mind when you think of your mother?
  decomp: * mother *
    reasmb: Who else in your family (2)?
```

### Special Features

- **goto**: Redirect to another keyword's patterns
  ```
  reasmb: goto family
  ```

- **save ($)**: Save response to memory for later use
  ```
  decomp: $ * i want *
  ```

- **xnone**: Fallback responses when no pattern matches
  ```
  key: xnone
    decomp: *
      reasmb: Please go on.
      reasmb: Tell me more about that.
  ```

## Custom Scripts

You can provide your own script:

```python
from oureliza import Eliza

my_script = """
initial: Hello! How can I help you today?
final: Goodbye!
quit: bye
quit: exit

key: xnone
  decomp: *
    reasmb: I see. Tell me more.
    reasmb: Please continue.

key: hello 10
  decomp: *
    reasmb: Hi there! What's on your mind?
"""

eliza = Eliza(script=my_script)
print(eliza.respond("hello"))
```

## Development

```bash
# Install dependencies
make install

# Run tests
make test

# Build package
make build

# Do everything
make all
```

## References

Based on [wadetb/eliza](https://github.com/wadetb/eliza) with significant script expansion.

## License

MIT
