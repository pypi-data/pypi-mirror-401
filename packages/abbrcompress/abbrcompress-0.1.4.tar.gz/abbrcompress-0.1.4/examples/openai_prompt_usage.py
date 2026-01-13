from abbrcompress.core import build_abbreviations, compress_prompt, decode_abbreviations, token_len

prompt = """your prompt text here"""

# Build abbreviation dictionary
abbr_dict, _ = build_abbreviations(prompt)

# Compress prompt
compressed_prompt = compress_prompt(prompt, abbr_dict)

# TODO: send compressed_prompt to OpenAI and get compressed_text as response
compressed_text = _  # Placeholder for OpenAI response

# Decode return from OpenAI
decoded_text = decode_abbreviations(compressed_text, abbr_dict)
