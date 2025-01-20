import json
from json import JSONDecodeError


class  IsolateMetadata:
    def __init__(self, accession, collection_date, location):
        self.accession = accession
        self.collection_date = collection_date
        self.location = location

    def to_dict(self):
        return {
            'accession': self.accession,
            'collection_date': self.collection_date,
            'location': self.location
        }


def extract_json_metadata(json_path):
    # Extract metadata from assembly_data_report.jsonl using 'datasets download genome'
    json_data = []

    # Parse JSON file
    with open(json_path, 'r') as i_json:
        for index, line in enumerate(i_json):
            try:
                json_data.append(json.loads(line))
            except JSONDecodeError:
                print(f'Line {str(index)} does not conform to JSON format convention.')

    # Extract metadata from JSON
    meta_dict = {}
    na_lst = []
    for line in json_data:
        seqid = line['accession']
        if seqid not in meta_dict.keys():
            meta_dict[seqid] = {}

        for dicti in line['assemblyInfo']['biosample']['attributes']:
            if list(dicti.values())[0] == 'collection_date':
                try:
                    meta_dict[seqid] = {list(dicti.values())[0]: list(dicti.values())[1]}
                    date_value = list(dicti.values())[1]
                except IndexError:
                    na_lst.append(seqid)

            if list(dicti.values())[0] == 'geo_loc_name':
                try:
                    meta_dict[seqid].update({list(dicti.values())[0]: list(dicti.values())[1]})
                    location_value = list(dicti.values())[1]
                except IndexError:
                    na_lst.append(seqid)

        seqid_meta = IsolateMetadata(accession=seqid, collection_date=date_value, location=location_value)
        meta_dict[seqid_meta.accession] = seqid_meta

    return meta_dict, na_lst