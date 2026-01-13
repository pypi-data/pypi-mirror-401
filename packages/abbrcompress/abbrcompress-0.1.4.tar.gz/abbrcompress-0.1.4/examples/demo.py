from abbrcompress import build_abbreviations, compress_prompt, decode_abbreviations, token_len

# -------------------------------
# 6️⃣ Demo
# -------------------------------
prompt = """
According to the latest Luxembourgish GDP report, the Luxembourgish GDP grew by 2% in the last quarter, 
reflecting a steady recovery after the economic slowdown caused by global events. 
According to the latest Luxembourgish GDP report, inflation remained stable at 1.8%, 
indicating that the central bank's monetary policy has been effective. 
The Ministry of Finance of Luxembourg will release updates tomorrow regarding public spending and investment plans. 
The Ministry of Finance of Luxembourg also updated the GDP forecast for the next fiscal year. 
Analysts suggest that according to the latest Luxembourgish GDP report, economic growth could accelerate if external conditions remain favorable. 
Moreover, inflation remained within the expected range, supporting consumer confidence. 
Luxembourg's Ministry of Finance confirmed that they will continue monitoring the economic situation closely. 
According to the latest Luxembourgish GDP report, the industrial sector has shown modest growth, while the services sector continues to expand steadily. 
The Ministry of Finance of Luxembourg announced a new set of guidelines for investment in renewable energy. 
The Ministry of Finance of Luxembourg is collaborating with the European Commission to improve fiscal oversight and transparency. 
Investors are optimistic that, according to the latest Luxembourgish GDP report, the financial sector will continue to perform strongly. 
Inflation remained stable across all monitored categories, providing additional assurance to markets. 
The Ministry of Finance of Luxembourg has also issued new recommendations on corporate taxation and incentives. 
According to the latest Luxembourgish GDP report, overall consumer spending increased slightly, supporting domestic demand. 
The Ministry of Finance of Luxembourg will hold a press conference to discuss the upcoming budget and financial projections. 
Policy analysts note that according to the latest Luxembourgish GDP report, external trade remains a key driver of economic growth. 
Inflation remained well-controlled, suggesting that the current economic policies are effective. 
The Ministry of Finance of Luxembourg plans to release detailed sectoral reports in the coming weeks. 
The Ministry of Finance of Luxembourg continues to emphasize transparency, accountability, and timely dissemination of information to the public. 
"""


abbr_dict_with_freq, compressed_text = build_abbreviations(prompt)
compressed_prompt = compress_prompt(prompt, abbr_dict_with_freq)

# Token stats
original_tokens = token_len(prompt)
compressed_tokens = token_len(compressed_prompt)

pct_change = (compressed_tokens - original_tokens) / original_tokens * 100

# Display
print("Abbreviation dictionary with frequencies:")
for abbr, (phrase, freq) in abbr_dict_with_freq.items():
    print(f"{abbr}: '{phrase}' → appears {freq} times")

print(f"\nOriginal tokens: {original_tokens}")
print(f"Compressed tokens: {compressed_tokens} ({pct_change:+.1f}%)\n")
print("Compressed prompt:\n")
print(compressed_prompt)

# Decode return from OpenAI
decoded_text = decode_abbreviations(compressed_text, abbr_dict_with_freq)
if decoded_text == prompt:
    print("\n✅ Decoding successful: Decoded prompt matches original.")
else:
    print("\n❌ Decoding failed: Decoded prompt does not match original.")
