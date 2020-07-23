from sequence_transfer.sequence import CharSequence

text = "My name is Nina"

# 01 - We create a char sequence and access basic property
s = CharSequence.new(text)

print(f"Text: {s.text}")  # access text property
print(f"Size: {s.size}")  # access size property
print(f"Length: {len(s)}")  # alias of the size property

# 02 - Playing with subsequences
sub = s[1]  # get the second char
print(f"Sequence `{sub.text}` starts at {sub.start} and stops at: {sub.stop}")

sub = s[11:15]  # correspond to the Nina
print(f"Sequence `{sub.text}` starts at {sub.start} and stops at: {sub.stop}")

sub = s[-4:]   # get the last foor chars
print(f"Sequence `{sub.text}` starts at {sub.start} and stops at: {sub.stop}")

# 03 - Iterating over a CharSequence object create a subsequence of size 1 that correspond to each letter:
for sub in s[-4:]:
    print(f"Sequence `{sub.text}` starts at {sub.start} and stops at: {sub.stop}")

# 04 show a subsequence in it's original context
sub = s[5, 10]
print(sub.in_context())

# 05 Conclusion:
# A CharSequence basically behave like a python string object.
# But any substring generated from it "remember" the original string it comes from.






