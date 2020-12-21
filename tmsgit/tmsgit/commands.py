import subprocess


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
    import re
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
