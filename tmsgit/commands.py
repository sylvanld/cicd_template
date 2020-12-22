import os
import re
import datetime
import subprocess
from collections import defaultdict


def get_current_branch():
    p = subprocess.Popen(['git', 'branch', '--show-current'], stdout=subprocess.PIPE)
    return p.stdout.read().decode('utf-8').strip()


def normalize_sentence(sentence):
    return sentence[0].upper() + sentence[1:].replace('_', ' ') + '.'*(not sentence[-1]=='.')


def input_branch_name(branch_type):
    description = ""
    while len(description) < 4 or len(description) > 30:
        description = input('branch description: ')
        if len(description) < 4 or len(description) > 30:
            print('len(description) >= 4 and len(description) <= 30 ===> current:', len(description))
    return branch_type.lower() + '/' + description.lower().replace(' ', '_')


def input_commit_message():
    message = ""
    while len(message) < 10 or len(message) > 60:
        message = input('commit message: ').lower()
        if len(message) < 10 or len(message) > 60:
            print('len(message) >= 4 and len(message) <= 30 ===> current:', len(message))
    return message[0].upper() + message[1:] + "."*(not message.endswith('.'))


def create_branch(branch_type):
    # input short description to create branch name
    branch_name = input_branch_name(branch_type)

    # switch to branch main and update code based on remote
    subprocess.call(['git', 'checkout', 'main'])
    subprocess.call(['git', 'pull', '--rebase', 'origin', 'main'])

    # create branch locally and push it to remote
    subprocess.call(['git', 'checkout', '-b', branch_name])
    subprocess.call(['git', 'push', '-u', 'origin', branch_name])


def save_current_changes():
    """
    Generate a [wip] commit that won't be indexed in changelog
    """
    subprocess.call(['git', 'add', '.'])
    subprocess.call(['git', 'commit', '-m', '[wip]'])


def extract_commits_from_logs(command):
    LOG_COMMIT_PATTERN = re.compile("(?:^|\n)commit\s+(?P<commit_sha>\w+).+\nAuthor:\s+(?P<author>.+)\nDate:\s+(?P<date>.+)\n\n\s+(?P<message>.+)")
    
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = p.stdout.read().decode('utf-8').strip()
    return [m.groupdict() for m in LOG_COMMIT_PATTERN.finditer(output)]


def get_saved_commits():
    commits = []
    for commit in extract_commits_from_logs(['git', 'log']):
        if commit['message']!='[wip]':
            break
        commits.append(commit)
    return commits


def create_commit():
    # save all changes in a wip commit
    save_current_changes()

    # get number of wip commits to squash
    saved_commits = get_saved_commits()
    
    # number of commits to be squashed
    message = input_commit_message()
    squash_number = len(saved_commits)

    subprocess.call(["git", "reset", "--soft", "HEAD~%s"%squash_number])
    subprocess.call(['git', 'commit', '-m', message])


def enforce_changelog(filepath):
    """
    Create changelog and its folder if it does not exists.
    """
    filepath = os.path.abspath(filepath)
    directory = os.path.dirname(filepath)
    subprocess.call(['mkdir', '-p', directory])


def update_changelog(message, descriptions):
    """
    Append commits diff in changelog.
    """
    enforce_changelog('docs/changelog.md')
    datestr = datetime.datetime.now().strftime('%Y-%m-%d')
    with open('docs/changelog.md', 'a') as changelog:
        changelog.write('\n\n### %s (%s)\n'%(message, datestr))
        changelog.write('\n'.join(descriptions))


def merge_current_branch():
    merged_branch = get_current_branch()
    branch_types = ['feature', 'hotfix', 'bugfix', 'devops']
    mergeable_branch = any([merged_branch.startswith(branch_type + '/') for branch_type in branch_types])

    if not mergeable_branch:
        raise Exception("Branch prefix must be one of %s"%branch_types)

    branch_type, branch_name = merged_branch.split('/')
    message = "[%s] %s" % (branch_type, normalize_sentence(branch_name))
    descriptions = [commit['message'] for commit in extract_commits_from_logs(['git', 'log', 'main..'+merged_branch])]
    descriptions = ['- %s' % description for description in descriptions if description != '[wip]' and not description.startswith('[pre-release]')]

    # update changelog
    update_changelog(message, descriptions)
    save_current_changes()

    squash_message = message + "\n\n" + "\n".join(descriptions)
    
    subprocess.call(['git', 'checkout', 'main'])
    subprocess.call(['git', 'merge', '--squash', merged_branch])
    subprocess.call(['git', 'commit', '-m', squash_message])
    subprocess.call(['git', 'push', '-u', 'origin', 'main'])

    input('%s branch will be deleted (press [enter] to continue, [ctrl+c] to abort)'%branch_type)
    subprocess.call(['git', 'branch', '-D', merged_branch])
    subprocess.call(['git', 'push', '--delete', 'origin', merged_branch])


def show_commit_diff(compared_branch):
    current_branch = get_current_branch()

    command = ['git', 'log']
    if current_branch != compared_branch:
        command.append('%s..%s'%(compared_branch, current_branch))
    diff_commits = extract_commits_from_logs(command)
    
    if len(diff_commits) == 0:
        print('No difference between branches', current_branch, 'and', compared_branch)
        exit(0)

    diff_repr = '\n\n'.join([
        "Commit:\t%s\nAuthor:\t%s\nDate:\t%s\n\n\t%s"%(c['commit_sha'], c['author'], c['date'], c['message']) 
        for c in diff_commits])
    print(diff_repr)

import inspect
def file_exist_or_create(filepath, default_content):
    try:
        with open(filepath) as file:
            pass
    except FileNotFoundError:
        directory = os.path.abspath(os.path.dirname(filepath))
        os.makedirs(directory, exist_ok=True)
        with open(filepath, 'w') as version:
            version.write(inspect.cleandoc(default_content))


def initialize_project():
    file_exist_or_create('docs/changelog.md', default_content="""
    # ChangeLog

    > Below are described significant changes that occured in this project...

    ## Releases
    ## Unreleased work
    """)
    file_exist_or_create('setup.cfg', default_content="""
    [bumpversion]
    current_version = 0.0.1
    commit = True
    message = [release] Publish release {new_version}
    tag = True
    """)


def fix_previous_commit():
    """
    Rollback last commit, and integrates current changes as a fix.
    """
    last_commit = extract_commits_from_logs(['git', 'log'])[0]
    subprocess.call(['git', 'reset', 'HEAD~1'])
    subprocess.call(['git', 'add', '.'])
    subprocess.call(['git', 'commit', '-m', last_commit['message']])


def input_release_type():
    release_type = "?"
    while release_type not in ('', 'patch', 'minor', 'major'):
        release_type = input('release type (default=patch): ')
    return release_type if release_type else 'patch'


def current_date():
    return datetime.datetime.now().strftime('%Y-%m-%d')


def get_current_version():
    with open('setup.cfg') as setup:
        version_row = [row for row in setup.read().split('\n') if row.startswith('current_version')][0]
    return version_row.split('=')[1].strip()


def create_release():
    release_type = input_release_type()
    subprocess.call(['bump2version', release_type])
    current_version = get_current_version()

    # parse changelog and determine breakpoints
    with open('docs/changelog.md') as changelog:
        changelog_rows = changelog.read().split('\n')
    
    releases_index = changelog_rows.index('## Releases')
    unreleased_index = changelog_rows.index('## Unreleased work')
    changelog_length = len(changelog_rows)
    
    # iterate through unreleased work and sort it by category
    categories = defaultdict(str)
    category_pattern = re.compile('###\s\[(?P<category>\w+)\]\s(?P<title>.+\.)')
    current_category = None
    for k in range(unreleased_index+1, changelog_length):
        if changelog_rows[k].startswith('###'):
            info = category_pattern.search(changelog_rows[k]).groupdict()
            current_category = info['category'][0].upper() + info['category'][1:]
            categories[current_category] += '- ' + info['title'] + "\n"
        elif changelog_rows[k].startswith('-'):
            categories[current_category] += '\t' + changelog_rows[k] + "\n"

    # write each feature/bugfix/... in release description per-category
    release_description = "\n### %s - %s\n" % (current_version, current_date())
    for category, content in categories.items():
        release_description += '\n**%s**'%category + '\n\n'
        release_description +=  content
    
    #print(release_description)
    changelog = '\n'.join(changelog_rows[:releases_index+1]) \
            + '\n' + release_description + '\n' \
            + '\n'.join(changelog_rows[releases_index+1:unreleased_index]) \
            + '## Unreleased work'
    
    with open('docs/changelog.md', 'w') as changelog_file:
        changelog_file.write(changelog)

    subprocess.call(['git', 'add', '.'])
    subprocess.call(['git', 'commit', '-m', '[release] Publish release %s'%current_version])
    subprocess.call(['git', 'tag', current_version, '-m', 'Release %s'%current_version])
    subprocess.call(['git', 'push', '--follow-tags'])
