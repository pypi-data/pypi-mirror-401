# abbrcompress

Token-saving abbreviation compression for OpenAI-compatible LLM prompts. 

`abbrcompress` identifies frequently repeated phrases in a prompt, replaces them with short abbreviations, and decodes the model response back to the original text — helping reduce token usage for long or repetitive prompts. Testing on real datasets shows reductions of 1-2% of tokens sending to OpenAI.

## What this library does

✅ Detects repeated n-grams

✅ Computes net token savings using tiktoken

✅ Applies abbreviations only when savings are positive

✅ Decodes model responses safely

❌ Does not modify OpenAI tokenization

❌ Does not guarantee savings for short prompts

---

## Install

```bash
pip install abbrcompress
# or
uv pip install abbrcompress
```

## Usage

```python
from abbrcompress.core import build_abbreviations, compress_prompt, decode_abbreviations, token_len

prompt = """your prompt text here"""

# Build abbreviation dictionary
abbr_dict, _ = build_abbreviations(prompt)

# Compress prompt
compressed_prompt = compress_prompt(prompt, abbr_dict)

# TODO: send compressed_prompt to OpenAI and get return_message as response
return_message = _  # Placeholder for OpenAI response

# Decode return from OpenAI
decoded_text = decode_abbreviations(return_message, abbr_dict)
```