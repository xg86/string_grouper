import pandas as pd
from string_grouper import match_strings
from string_grouper import StringGrouper

company_names = './tutorials/sec_edgar_company_info.csv'
companies = pd.read_csv(company_names)[0:50000]
string_grouper = StringGrouper(companies['Company Name'], ignore_index=True)
#calculate cosine
string_grouper = string_grouper.fit()
companies['deduplicated_name'] = string_grouper.get_groups()
companies[companies.deduplicated_name.str.contains('PRICEWATERHOUSECOOPERS LLP')]
result = companies[companies.deduplicated_name.str.contains('PWC')]
#add 同义词
tring_grouper = string_grouper.add_match('PRICEWATERHOUSECOOPERS LLP', 'PWC HOLDING CORP')
companies['deduplicated_name'] = string_grouper.get_groups()
# Now lets check again:

result = companies[companies.deduplicated_name.str.contains('PRICEWATERHOUSECOOPERS LLP')]

#remove 同义词
string_grouper = string_grouper.remove_match('PRICEWATERHOUSECOOPERS LLP', 'ZUCKER MICHAEL')
result = companies['deduplicated_name'] = string_grouper.get_groups()

# Now lets check again:
result = companies[companies.deduplicated_name.str.contains('PRICEWATERHOUSECOOPERS LLP')]