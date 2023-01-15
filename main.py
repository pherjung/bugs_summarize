import os
import requests


BASE_URL = 'https://api.taiga.io/api/v1'
SFOS = 'https://forum.sailfishos.org/t/'
PROJECT = 'thigg-sfos-bug-mod'
json_data = {
    'username': os.getenv('USERNAME'),
    'password': os.getenv('PASSWORD'),
    'type': 'normal'
}
response = requests.post(f'{BASE_URL}/auth', json=json_data)
token = response.json()['auth_token']
HEADERS = {'Authorization': f'Bearer {token}'}
kanban = requests.get(f'{BASE_URL}/projects/by_slug?slug={PROJECT}',
                      headers=HEADERS)
kanban_id = kanban.json()['id']

good_meeting = requests.get(
    f'{BASE_URL}/userstories?project={kanban_id}&status=3020511',
    headers=HEADERS
).json()
bugs_close = requests.get(
    f'{BASE_URL}/userstories?project={kanban_id}&status=3023266',
    headers=HEADERS
).json()
bugs_duplicate = requests.get(
    f'{BASE_URL}/userstories?project={kanban_id}&status=3235139',
    headers=HEADERS
).json()


def return_attributes(ticket):
    """
    Return custom attributes from the ticket
    :option ticket: dict
    """
    attributes = requests.get(
        f"{BASE_URL}/userstories/custom-attributes-values/{ticket['id']}",
        headers=HEADERS
    )
    attributes = attributes.json()
    bug_id = attributes['attributes_values']['32818']
    bug_link = attributes['attributes_values']['32819']
    url = requests.get(bug_link).url
    return f"[{bug_id}]({url})"


def return_comment(ticket):
    """
    Return comment from the ticket
    :option ticket: dict
    """
    data = requests.get(f"{BASE_URL}/history/userstory/{ticket['id']}",
                        headers=HEADERS)
    data = data.json()
    for comment in data:
        if comment['comment']:
            comment = comment['comment'].replace('\\[', '[')
            comment = comment.replace('\\]', ']')
            return comment


with open('bugs.md', 'w', encoding='utf-8') as f:
    f.write('# Untracked bug reports\n')
    f.write('| ID | Comments | Additional Information |\n')
    f.write('| -- | -- | --\n')
    # Keep only 10 bugs from the column Good for meeting
    for bug in good_meeting[:10]:
        site = return_attributes(bug)
        blabla = return_comment(bug)
        f.write(f"| {site} | {blabla} |\n")

    if bugs_close[:10]:
        f.write('\n')
        f.write('# To be closed\n')
        f.write('| ID | Reason\n')
        f.write('| -- | --\n')
        for bug in bugs_close:
            site = return_attributes(bug)
            blabla = return_comment(bug)
            f.write(f"| {site} | {blabla}\n")

    if bugs_duplicate[:10]:
        f.write('\n')
        f.write('# Duplicate\n')
        f.write('| ID | Duplicate with\n')
        f.write('| -- | --\n')
        for bug in bugs_duplicate:
            site = return_attributes(bug)
            blabla = return_comment(bug)
            f.write(f"| {site} | {blabla}\n")
