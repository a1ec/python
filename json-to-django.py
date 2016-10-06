import json

with open("cbury.json") as json_file:
    json_data = json.load(json_file)
    
# derive keys list from the first JSON object 
keys_list = list(json_data[0])

from das.models import DA

from datetime import datetime
from django.utils import timezone

# for each JSON item
for i in json_data:
    da = DA()
    # match all JSON attributes to the django model
    for k in keys_list:
        # TODO change? accessing __dict__ probably not good practice
        if k == "date_lodged":
            # TODO convert string from dd/mm/YY to datetime
            da.__dict__[k] = datetime.strptime(i[k], '%d/%m/%Y').date()
        elif k == ('date_rec_created' or 'date_rec_modified'):
            da.__dict__[k] = timezone.now()
        else:
            da.__dict__[k] = i[k]

    da.save()
