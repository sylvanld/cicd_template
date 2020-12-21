import argparse


def register_create_parser(subparsers):
    create_parser = subparsers.add_parser('create', help='Create branch of given type')
    create_parser.add_argument('branch_type', choices=['feature', 'hotfix', 'bugfix', 'devops'])


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    register_create_parser(subparsers)

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
