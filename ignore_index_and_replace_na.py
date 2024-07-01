import pandas as pd
from string_grouper import match_strings, match_most_similar, group_similar_strings
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)
test_series_1_nameless = pd.Series(['foo', 'bar', 'baz', 'foo'])

print(test_series_1_nameless)
print(match_strings(test_series_1_nameless))
print(match_strings(test_series_1_nameless, ignore_index=True))

test_series_1_named = pd.Series(['foo', 'bar', 'baz', 'foo'], name='wow')
print(test_series_1_named)

test_series_1_nameless_index = pd.Series(['foo', 'bar', 'baz', 'foo'], name='wow', index=list('ABCD'))
print(test_series_1_nameless_index)