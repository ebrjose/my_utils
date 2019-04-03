# Python
import json, decimal

# Django
from django.db import connection

def execute_query(query, get='object'):	
	cursor = connection.cursor()
	cursor.execute(query)
	_result = cursor.fetchall()

	if get == 'object':
		from collections import namedtuple
		result = []
		for row in _result:
			d = dict(zip([key[0] for key in cursor.description], row))
			d_named = namedtuple("QuerySet", d.keys())(*d.values())
			result.append(d_named)

	if get == 'dict':
		result = [dict(zip([key[0] for key in cursor.description], row) ) for row in _result]

	if get == 'json':

		def decimal_default(obj):
		    if isinstance(obj, decimal.Decimal):
			return float(obj)
		    raise TypeError

		items = [dict(zip([key[0] for key in cursor.description], row) ) for row in _result]
		result = json.dumps(items, default=decimal_default)

	return result
