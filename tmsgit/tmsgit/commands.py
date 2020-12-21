import subprocess

def input_branch_name(branch_type):
    description = ""
    while len(description) < 4 or len(description) > 30:
        description = input('branch description: ')
        if len(description) < 4 or len(description) > 30:
            print('len(description) >= 4 and len(description) <= 30 ===> current:', len(description))
    return branch_type.lower() + '/' + description.lower().replace(' ', '_')
    



def create_branch(branch_type):
    # input short description to create branch name
    branch_name = input_branch_name(branch_type)

    # switch to branch main and update code based on remote
    subprocess.call(['git', 'checkout', 'main'])
    subprocess.call(['git', 'pull', '--rebase', 'origin', 'main'])

    # create branch locally and push it to remote
    subprocess.call(['git', 'checkout', '-b', branch_name])
    subprocess.call(['git', 'push', '-u', 'origin', branch_name])
    
