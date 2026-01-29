def compare_intervals(lower_bound_0: int, upper_bound_0: int, lower_bound_1: int, upper_bound_1: int) -> int:
	if lower_bound_0 < lower_bound_1:
		return -1
	if lower_bound_1 < lower_bound_0:
		return 1
	if upper_bound_0 < upper_bound_1:
		return -1
	if upper_bound_1 < upper_bound_0:
		return 1
	return 0

reg_exp_special_chars = list(map(lambda c: c.encode('utf-8'), ['[', '.', '*', '+', '?', '^', '$', '{', '}', '(', ')', '|', '[', '\\', ']']))


# In Python 3, strings are sequences of Unicode code points, so most characters
# are already full code points and surrogate pairs shouldn't normally appear.
# However, if this string contains UTF-16 surrogate code units (e.g. due to
# decoding with 'surrogatepass'), handle combining them so the parser behaves
# similarly to the original JS implementation.

# Helper lambdas for checking surrogate ranges (0xD800-0xDBFF for high,
# 0xDC00-0xDFFF for low).
def is_high_surrogate(ch: str) -> bool:
	return 0xD800 <= ord(ch) <= 0xDBFF

def is_low_surrogate(ch: str) -> bool:
	return 0xDC00 <= ord(ch) <= 0xDFFF