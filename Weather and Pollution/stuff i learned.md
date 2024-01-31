# Weather Shit

result_json_data = json.loads(content)       
formated_json = json.dumps(result_json_data, indent=2)

Jako je bitno da znam da **ne mogu da izvlacim podatke iz json.dumps nego iz json.loads**, ako bi zeleo iz json.dumps da izvucem morao bih prvo da tah dumps vratim u json.loads

