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

from compasweb.models import Keyword, COMPASJob


def convert_datetime(dinfo):
    nt = datetime.datetime.strptime(f"{dinfo} +0000", "%Y-%m-%d-%H:%M:%S %z")
    return nt

print(os.path.dirname(os.path.abspath(__file__)))
data = pd.read_csv('test_datasets.csv', sep=',')
entries = data.shape[0]

# delete the previous version of test entries
COMPASJob.objects.all().delete()

for i in range(entries):
    author = data['author'][i]
    title = data['title'][i]
    description = data['description'][i]
    published = bool(data['published'][i])
    year = int(data['year'][i])
    journal = data['journal'][i]
    journal_DOI = data['journal_DOI'][i]
    dataset_DOI = data['dataset_DOI'][i]
    public = bool(data['public'][i])
    creation_time = convert_datetime(data['date'][i])
    print(creation_time)
    link = data['link'][i]
    arxiv_id = data['arxiv_id'][i]
    keywords = data['keywords'][i].split(';')

    # add entry to compasjob database
    job = COMPASJob.objects.get_or_create(author=author,title=title,description=description,
                                          published=published,year=year,journal=journal,
                                          journal_DOI=journal_DOI,dataset_DOI=dataset_DOI,
                                          creation_time=creation_time,public=public,
                                          download_link=link,arxiv_id=arxiv_id)[0]


    # add entry to keyword database
    for kw in keywords:
        keyword = Keyword.objects.get_or_create(tag=kw)[0]
        job.keywords.add(keyword)