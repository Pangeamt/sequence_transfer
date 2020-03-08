from sequence_transfer.sequence import TokenSequence

tokens = ['My', 'name', 'is', 'Nina']

# 01 - We create a char sequence and access basic property
s = TokenSequence.new(tokens)

print(f"Text: {s.text}")  # access text property
print(f"Size: {s.size}")  # access size property
print(f"Length: {len(s)}")  # alias of the size property

# 02 - Playing with subsequences
sub = s[1]  # get the second token. (exactly: return a subsequence of size 1 that contain that second token)
print(f"Sequence `{sub.text}` starts at {sub.start} and stops at: {sub.stop}")

sub = s[1:3]  # First and second token
print(f"Sequence `{sub.text}` starts at {sub.start} and stops at: {sub.stop}")

sub = s[:-1]   # Last token
print(f"Sequence `{sub.text}` starts at {sub.start} and stops at: {sub.stop}")

# 03 - Iterating over a TokenSequence object create a subsequence of size 1 that correspond to each token:
for sub in s:
    print(f"Token `{sub.text}` starts at {sub.start} and stops at: {sub.stop}")

# 04 show a subsequence of token in it's original context
sub = s[1, 2]
print(sub.in_context())

# 05 Conclusion:
# A TokenSequence behave more or less like python list of strings.
# But any subsequence of a TokenSequence  "remember" the entire sequence of token.






