import pandas as pd
from string_grouper import match_strings
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)

accounts = pd.read_csv('./tutorials/accounts.csv')
#print(accounts)
matches = match_strings(accounts['name'], master_id = accounts['id'], ignore_index=True, min_similarity = 0.1)
dupes = matches[matches.left_id != matches.right_id]

company_dupes = pd.DataFrame(dupes.left_id.unique()).squeeze().rename('company_id')
result = dupes[dupes.left_name.str.contains('hyper')]
print(result)