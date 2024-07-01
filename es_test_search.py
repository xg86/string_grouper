import pandas as pd
import numpy as np
import datetime
from string_grouper import match_strings, match_most_similar, \
	group_similar_strings, compute_pairwise_similarities, \
	StringGrouper
from timeit import default_timer as timer

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)
import fuzzy
dmeta = fuzzy.DMetaphone(4)
import sys
import pandas as pd
from pandas import DataFrame
import os
import locale
os.environ["PYTHONIOENCODING"] = "utf-8"
scriptLocale=locale.setlocale(category=locale.LC_ALL, locale="en_GB.UTF-8")
print(sys.stdout.encoding )
wcfile = "C://git//string_grouper//tutorials//wc_sanction_list.csv"

wc_sanction = pd.read_csv(wcfile, encoding='utf-8')
#print(*wc_sanction)
print("wc_sanction with rows", len(wc_sanction))
wc_sanction.FIRST_NAME = wc_sanction.FIRST_NAME.fillna('')
wc_sanction['WHOLE_NAME'] = wc_sanction['FIRST_NAME']+' '+wc_sanction['LAST_NAME']
wc_sanction['FIRST_NAME'] = wc_sanction['FIRST_NAME'].map(lambda x: x.encode('unicode-escape').decode('utf-8'))
wc_sanction['firstname_phone'] = wc_sanction['FIRST_NAME'].apply(lambda x: str(dmeta(x)))
wc_sanction['LAST_NAME'] = wc_sanction['LAST_NAME'].map(lambda x: x.encode('unicode-escape').decode('utf-8'))
wc_sanction['lastname_phone'] = wc_sanction['LAST_NAME'].apply(lambda x: str(dmeta(x)))

request_names = './tutorials/jinxin_test.csv'
requests = pd.read_csv(request_names, encoding='latin-1')
requests.firstName = requests.firstName.fillna('')
requests.lastName = requests.lastName.fillna('')
import re
requests['lastName'] = requests['lastName'].apply(lambda x: re.sub('[@]', '', x))
requests['wholeName'] = requests['firstName']+" "+ requests['lastName']
requests['firstnamePhone'] = requests['firstName'].apply(lambda x: str(dmeta(x)))
requests['lastName'] = requests['lastName'].map(lambda x: x.encode('unicode-escape').decode('utf-8'))
requests['lastnamePhone'] = requests['lastName'].apply(lambda x: str(dmeta(x)))

start = timer()
print("start", datetime.datetime.now())
double_matches = match_strings(master = wc_sanction['WHOLE_NAME'],
							   duplicates = requests['wholeName'],
							   master_id = wc_sanction['UID'],
							   duplicates_id = requests['requestID'],
							   ignore_index=True, min_similarity = 0.25)
print("end: ", datetime.datetime.now())
end = timer()
time_use_s = end - start
double_matches.to_csv('es_test_search.csv')

matches_above_60 = double_matches.loc[double_matches["similarity"] >= 0.60]
matches_above_60['boost_similarity'] = matches_above_60.similarity
matches_above_60.to_csv('matches_above_60.csv')

matches_below_60 = double_matches.loc[double_matches["similarity"] < 0.60]
matches_below_60.to_csv('matches_below_60_b4.csv')
sanction_phone = wc_sanction[wc_sanction.UID.isin(matches_below_60.left_UID)]
requests_phone = requests[requests.requestID.isin(matches_below_60.right_requestID)]
#requests_phone.to_csv('requests_phone.csv')
sanction_phone_firsname = sanction_phone.copy()
sanction_phone_firsname = sanction_phone_firsname.replace(r'^s*$', float('NaN'), regex = True)
sanction_phone_firsname.dropna(subset = ['FIRST_NAME'], inplace = True)

requests_phone_firsname = requests_phone.copy()
requests_phone_firsname = requests_phone_firsname.replace(r'^s*$', float('NaN'), regex = True)
requests_phone_firsname.dropna(subset = ['firstName'], inplace = True)


def fussy_d_meta(matches_below_60: DataFrame,
				 sanction_phone_firstname: pd.Series, requests_phone_firstname : pd.Series,
				 sanction_phone_lastname: pd.Series, requests_phone_lastname : pd.Series,
				 sanction_id: pd.Series, requestID: pd.Series, phone_similarity=0.6):
	first_phone_matches = match_strings(sanction_phone_firstname,
										requests_phone_firstname,
										master_id = sanction_id,
										duplicates_id = requestID,
										ignore_index=True, min_similarity=phone_similarity)
	first_phone_matches.to_csv('first_phone_matches.csv')
	lastname_phone_matches = match_strings(sanction_phone_lastname, requests_phone_lastname,
										   master_id = sanction_id,
										   duplicates_id = requestID,
										   ignore_index=True, min_similarity=phone_similarity)
	lastname_phone_matches.to_csv('lastname_phone_matches.csv')

	matches_below_60_new = matches_below_60.copy()
	matches_below_60_new = pd.merge(matches_below_60_new, lastname_phone_matches, how="outer",on=["right_requestID", "left_UID"])
	matches_below_60_new.to_csv('matches_below_60_new_merged_lastname.csv')
	matches_below_60_new = pd.merge(matches_below_60_new, first_phone_matches, how="outer", on=["right_requestID", "left_UID"])
	matches_below_60_new.to_csv('matches_below_60_new_merged_firstname.csv')
	matches_below_60_new = matches_below_60_new.fillna(0)
	matches_below_60_new[
		'boost_similarity'] = matches_below_60_new.similarity_x + matches_below_60_new.similarity_y / 5.7 + matches_below_60_new.similarity / 5.7
	matches_below_60_boost = matches_below_60_new.loc[matches_below_60_new["boost_similarity"] >= 0.60]
	matches_below_60_boost = matches_below_60_boost.drop('left_firstname_phone', 1)
	matches_below_60_boost = matches_below_60_boost.drop('right_firstnamePhone', 1)
	matches_below_60_boost = matches_below_60_boost.drop('left_lastname_phone', 1)
	matches_below_60_boost = matches_below_60_boost.drop('right_lastnamePhone', 1)
	matches_below_60_boost = matches_below_60_boost.drop('similarity_y', 1)
	matches_below_60_boost = matches_below_60_boost.drop('similarity', 1)
	matches_below_60_boost.columns = ['left_WHOLE_NAME', 'left_UID', 'similarity', 'right_requestID', 'right_wholeName',
									  'boost_similarity']
	matches_below_60_boost.to_csv('matches_below_60_new_boost.csv')

	return matches_below_60_boost

fussy_fl= fussy_d_meta(matches_below_60 = matches_below_60,
					   sanction_phone_firstname = sanction_phone_firsname['firstname_phone'],
					   requests_phone_firstname = requests_phone_firsname['firstnamePhone'],
				 	   sanction_phone_lastname = sanction_phone_firsname['lastname_phone'],
					   requests_phone_lastname = requests_phone_firsname['lastnamePhone'],
				 	   sanction_id= sanction_phone_firsname['UID'],
					   requestID = requests_phone_firsname['requestID'],
					   phone_similarity=0.6)
result = matches_above_60.append(fussy_fl)
result.to_csv('final_result.csv')

fussy_lf= fussy_d_meta(matches_below_60 = matches_below_60,
					   sanction_phone_firstname = sanction_phone_firsname['firstname_phone'],
					   requests_phone_firstname = requests_phone_firsname['lastnamePhone'],
				 	   sanction_phone_lastname = sanction_phone_firsname['lastname_phone'],
					   requests_phone_lastname = requests_phone_firsname['firstnamePhone'],
				 	   sanction_id= sanction_phone_firsname['UID'],
					   requestID = requests_phone_firsname['requestID'],
					   phone_similarity=0.6)

result_double = result.append(fussy_lf)

result_double.to_csv('result_double.csv')
print("Total time usage for searching: {}s ({}rows search result)".format(int(time_use_s + 0.5), int(len(double_matches))))
