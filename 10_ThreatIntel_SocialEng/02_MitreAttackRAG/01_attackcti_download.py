# Derived from https://github.com/OTRF/GenAI-Security-Adventures
# This script downloads the real-time Mitre ATT&CK information on a variety of
# attack groups, formats them in Markdown files, then loads them into a vector
# database (ChromaDB).  This is subsequently used in a RAG chain to handle
# queries through an LLM
from attackcti import attack_client
import os
import re
import copy
from jinja2 import Template

current_directory = f"{os.path.dirname(__file__)}/mitre_rag_data/"
documents_directory = os.path.join(current_directory, "documents")
if not os.path.exists(documents_directory):
    os.makedirs(documents_directory)

lift = attack_client()
techniques_used_by_groups = lift.get_techniques_used_by_all_groups()
techniques_used_by_groups[0]

# Create Group docs
all_groups = dict()

for technique in techniques_used_by_groups:
    if technique['id'] not in all_groups:
        group = dict()

        technique.get('name') and group.update({'group_name': technique['name']})
        technique.get('external_references') and group.update({'group_id': technique['external_references'][0]['external_id']})
        technique.get('created') and group.update({'created': technique['created']})
        technique.get('modified') and group.update({'modified': technique['modified']})
        technique.get('description') and group.update({'description': technique['description']})
        technique.get('aliases') and group.update({'aliases': technique['aliases']})
        technique.get('x_mitre_contributors') and group.update({'contributors': technique['x_mitre_contributors']})

        group['techniques'] = []
        all_groups[technique['id']] = group

    technique_used = dict()

    technique.get('technique_matrix') and technique_used.update({'matrix': technique['technique_matrix']})
    technique.get('x_mitre_domains') and technique_used.update({'domain': technique['x_mitre_domains']})
    technique.get('platform') and technique_used.update({'platform': technique['platform']})
    technique.get('tactic') and technique_used.update({'tactics': technique['tactic']})
    technique.get('technique_id') and technique_used.update({'technique_id': technique['technique_id']})
    technique.get('technique') and technique_used.update({'technique_name': technique['technique']})
    technique.get('relationship_description') and technique_used.update({'use': technique['relationship_description']})
    technique.get('data_sources') and technique_used.update({'data_sources': technique['data_sources']})

    all_groups[technique['id']]['techniques'].append(technique_used)
print("[+] Creating markdown files for each group..")
group_template = os.path.join(current_directory, "group_template.md")
markdown_template = Template(open(group_template).read())
for key in list(all_groups.keys()):
    group = all_groups[key]
    print("  [>>] Creating markdown file for {}..".format(group['group_name']))
    group_for_render = copy.deepcopy(group)
    markdown = markdown_template.render(metadata=group_for_render, group_name=group['group_name'], group_id=group['group_id'])
    file_name = (group['group_name']).replace(' ','_')
    open(f'{documents_directory}/{file_name}.md', encoding='utf-8', mode='w').write(markdown)
