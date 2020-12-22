import argparse
import argcomplete

def register_merge_parser(subparsers):
    merge_parser = subparsers.add_parser('merge', help='Merge current branch in main branch, generating changelog, with a nice message')


def register_commit_parser(subparsers):
    commit_parser = subparsers.add_parser('commit', help='Create a commit including current changes and [wip] previous commits')


def register_save_parser(subparsers):
    save_parser = subparsers.add_parser('save', help='Create a temporary [wip] commit that wont appear in final history')


def register_create_parser(subparsers):
    create_parser = subparsers.add_parser('create', help='Create branch of given type')
    create_parser.add_argument('branch_type', choices=['feature', 'hotfix', 'bugfix', 'devops'])


def register_log_parser(subparsers):
    create_parser = subparsers.add_parser('log', help='Display commits difference between this branch and selected branch (default main)')
    create_parser.add_argument('--compared', type=str, default='main', help='Other branch to compare commit diff.')


def register_fix_parser(subparsers):
    create_parser = subparsers.add_parser('fix', help='Rewrite last commit to integrate current changes.')


def register_init_parser(subparsers):
    create_parser = subparsers.add_parser('init', help='Create default configuration files in repository.')


def register_release_parser(subparsers):
    release_parser = subparsers.add_parser('release', help='Publish new release (increment version, changelog...)')

def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    register_merge_parser(subparsers)
    register_create_parser(subparsers)
    register_save_parser(subparsers)
    register_commit_parser(subparsers)
    register_log_parser(subparsers)
    register_fix_parser(subparsers)
    register_init_parser(subparsers)
    register_release_parser(subparsers)

    argcomplete.autocomplete(parser)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        exit(0)

    return args


def main():
    args = parse_args()

    if args.command == 'create':
        from .commands import create_branch
        create_branch(args.branch_type)
    elif args.command == 'save':
        from .commands import save_current_changes
        save_current_changes()
    elif args.command == 'commit':
        from .commands import create_commit
        create_commit()
    elif args.command == 'merge':
        from .commands import merge_current_branch
        merge_current_branch()
    elif args.command == 'log':
        from .commands import show_commit_diff
        show_commit_diff(args.compared)
    elif args.command == 'fix':
        from .commands import fix_previous_commit
        fix_previous_commit()
    elif args.command == 'init':
        from .commands import initialize_project
        initialize_project()
    elif args.command == 'release':
        from .commands import create_release
        create_release()
