# abbrcompress

Token-saving abbreviation compression for OpenAI LLM prompts.

## Install

```bash
pip install abbrcompress
uv pip install abbrcompress

## Usage

from abbrcompress import AbbrCompressor

compressor = AbbrCompressor()
abbrs, _ = compressor.build_abbreviations(text)
compressed = compressor.compress_prompt(text)

