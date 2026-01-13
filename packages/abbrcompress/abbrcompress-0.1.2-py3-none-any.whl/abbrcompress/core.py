import tiktoken
from collections import Counter
import re

# -------------------------------
# 1️⃣ Setup tokenizer for your model
# -------------------------------
model_name = "gpt-3.5-turbo"
encoding = tiktoken.encoding_for_model(model_name)
ABBR_PATTERN = re.compile(r"\bABB\d+\b")

def token_len(text):
    """Return number of tokens in a string."""
    return len(encoding.encode(text))

# -------------------------------
# 2️⃣ Extract candidate phrases (n-grams)
# -------------------------------
def extract_phrases(text, max_phrase_len=4):
    tokens = text.split()
    phrases = []
    for n in range(2, max_phrase_len+1):
        for i in range(len(tokens)-n+1):
            phrase = " ".join(tokens[i:i+n])
            phrases.append(phrase)
    return phrases

# -------------------------------
# 3️⃣ Compute net token saving
# -------------------------------
def net_saving(phrase, abbreviation, freq):
    phrase_tokens = token_len(phrase)
    abbr_tokens = token_len(abbreviation)
    dict_tokens = token_len(f"{abbreviation} = {phrase}\n")
    saving = (phrase_tokens - abbr_tokens) * freq - dict_tokens
    # if saving > 0:
    #     print(f"Saving {saving} tokens for phrase '{phrase}' with abbreviation '{abbreviation}'")
    return saving

# -------------------------------
# 4️⃣ Build abbreviation dictionary
# -------------------------------
def build_abbreviations(
    text,
    min_freq=2,
    max_phrase_len=4,
    max_abbrs=3,
):
    """
    Build abbreviation dictionary with frequencies:
    - Returns: { ABBx: (phrase, freq) }, compressed_text
    - Greedy, avoids ABBx in phrases
    """
    current_text = text
    abbr_dict = {}
    abbr_index = 1

    for _ in range(max_abbrs):
        phrases = extract_phrases(current_text, max_phrase_len)
        counts = Counter(phrases)

        best = None  # (saving, phrase, freq)

        for phrase, freq in counts.items():
            if freq < min_freq:
                continue
            if ABBR_PATTERN.search(phrase):
                continue  # avoid phrases containing ABBx

            abbr = f"ABB{abbr_index}"
            saving = net_saving(phrase, abbr, freq)

            if saving > 0 and (best is None or saving > best[0]):
                best = (saving, phrase, freq)

        if best is None:
            break

        _, phrase, _ = best
        abbr = f"ABB{abbr_index}"

        # Apply abbreviation immediately
        current_text = current_text.replace(phrase, abbr)
        # Frequency will be counted in compressed_text later
        abbr_dict[abbr] = phrase
        abbr_index += 1

    # Count final frequency in compressed text
    abb_occurrences = Counter(re.findall(r'\bABB\d+\b', current_text))
    # Convert to ABB → (phrase, freq)
    abbr_dict_with_freq = {
        abbr: (phrase, abb_occurrences.get(abbr, 0))
        for abbr, phrase in abbr_dict.items()
    }

    return abbr_dict_with_freq, current_text



# -------------------------------
# 5️⃣ Add definitions to compressed text
# -------------------------------
def compress_prompt(original_text, abbr_dict_with_freq):
    """
    Compress prompt by applying ABB replacements and
    prepending ABB definitions.
    """
    if not abbr_dict_with_freq:
        return original_text

    compressed_text = original_text

    # Apply replacements (longer phrases first to avoid partial overlaps)
    for abbr, (phrase, _) in sorted(
        abbr_dict_with_freq.items(),
        key=lambda x: len(x[1][0]),
        reverse=True,
    ):
        compressed_text = compressed_text.replace(phrase, abbr)

    defs = "\n".join(
        f"{abbr} = {phrase}" for abbr, (phrase, _) in abbr_dict_with_freq.items()
    )

    compress_prompt = defs + "\n\n" + compressed_text

    if (token_len(compress_prompt) >= token_len(original_text)):
        return original_text  # revert if no savings

    return compress_prompt

def decode_abbreviations(text, abbr_dict_with_freq):
    """
    Replace ABBx tokens in text with their original phrases.

    abbr_dict_with_freq:
        { "ABB1": ("Luxembourgish GDP report,", 6), ... }
    """
    if not abbr_dict_with_freq:
        return text

    # Replace longer ABBs first (ABB10 before ABB1)
    for abbr in sorted(abbr_dict_with_freq.keys(), key=len, reverse=True):
        phrase, _ = abbr_dict_with_freq[abbr]
        text = text.replace(abbr, phrase)

    return text


