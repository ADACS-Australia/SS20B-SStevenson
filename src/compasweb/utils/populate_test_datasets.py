import os
import sys
import pandas as pd
import datetime

def __setup_django(root_path, settings):
    import django
    # os.chdir(root_path)
    sys.path.append(root_path)
    os.environ["DJANGO_SETTINGS_MODULE"] = settings
    django.setup()

root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
__setup_django(root_path, "compas.settings")

from compasweb.models import COMPASJob


def convert_datetime(dinfo):
    nt = datetime.datetime.strptime(f"{dinfo} +0000", "%Y-%m-%d-%H:%M:%S %z")
    return nt

print(os.path.dirname(os.path.abspath(__file__)))
data = pd.read_csv('test_datasets.csv')
entries = data.shape[0]

# delete the previous version of test entries
COMPASJob.objects.all().delete()

for i in range(entries):
    author = data['author'][i]
    title = data['title'][i]
    description = data['description'][i]
    public = bool(data['access'][i])
    date = convert_datetime(data['date'][i])
    print(date)
    download = data['link'][i]

    # add entry to the database
    job = COMPASJob.objects.get_or_create(author=author,title=title,description=description,
                                          creation_time=date,public=public,
                                          download_link=download)[0]

