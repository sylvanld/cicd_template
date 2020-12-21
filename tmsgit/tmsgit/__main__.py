import argparse


def register_commit_parser(subparsers):
    commit_parser = subparsers.add_parser('commit', help='Create a commit including current changes and [wip] previous commits')


def register_save_parser(subparsers):
    save_parser = subparsers.add_parser('save', help='Create a temporary [wip] commit that wont appear in final history')


def register_create_parser(subparsers):
    create_parser = subparsers.add_parser('create', help='Create branch of given type')
    create_parser.add_argument('branch_type', choices=['feature', 'hotfix', 'bugfix', 'devops'])


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    register_create_parser(subparsers)
    register_save_parser(subparsers)
    register_commit_parser(subparsers)

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
