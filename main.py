from taiga import TaigaAPI
import os
import requests


api = TaigaAPI()
api.auth(
    username=os.getenv('USERNAME'),
    password=os.getenv('PASSWORD')
)
kanban = api.projects.get_by_slug('thigg-sfos-bug-mod')
bugs_good_meeting = api.user_stories.list(project=kanban.id, status=3020511)
bugs_close = api.user_stories.list(project=kanban.id, status=3023266)
bugs_duplicate = api.user_stories.list(project=kanban.id, status=3235139)


def write_bug(file, ticket):
    """
    Write all datas from a ticket
    :option file: File
    :option ticket: UserStory
    """
    attributes = ticket.get_attributes()
    bug_id = attributes['attributes_values']['32818']
    bug_link = attributes['attributes_values']['32819']
    url = requests.get(bug_link).url
    file.write(f"| [{bug_id}]({url}) | |\n")


with open('bugs.md', 'w', encoding='utf-8') as f:
    f.write('#Untracked bug reports\n')
    f.write('| ID | Comments | Additional Information |\n')
    f.write('| -- | -- | --\n')
    # Keep only 10 bugs from the column Good for meeting
    for bug in bugs_good_meeting[:10]:
        write_bug(f, bug)

    if bugs_close:
        f.write('\n')
        f.write('#To be closed\n')
        f.write('| ID | Reason\n')
        f.write('| -- | --\n')
        for bug in bugs_close:
            write_bug(f, bug)

    if bugs_duplicate:
        f.write('\n')
        f.write('#Duplicate\n')
        f.write('| ID | Duplicate with\n')
        f.write('| -- | --\n')
        for bug in bugs_duplicate:
            write_bug(f, bug)
