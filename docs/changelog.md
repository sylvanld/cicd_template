# ChangeLog

> Below are described significant changes that occured in this project...

## Releases
## Unreleased work

### [feature] Automatic changelog generation. (2020-12-21)
- Simple changelog generation.

### [bugfix] Fix changelog format. (2020-12-21)
- Add spacing between releases.
- Add heading style to new release title.
- Manually update changelog.

### [feature] Command to fix previous commit. (2020-12-21)
- Add docstring to 'fix_previous_commit'.
- Add logic for fix command.
- Add parser for 'fix' command.

### [devops] Restructure package. (2020-12-21)
- Remove one level of nesting in structure.

### [feature] Add init command. (2020-12-21)
- Generate project assets using init command.
- Create changelog and bump setup on init.
- Add parser for init command.

### [feature] Add release command. (2020-12-22)
- Manually create tag and deploy it on release.
- Fix version incremented twice.
- Auto update setup version on release.
- Bump version before creating changelog.
- Don't use bump2version to commit nor tag.
- Let bump2version manage commit.
- Parse and increment current version to populate changelog.
- Do changelog update on release, and bump version.
- Adapt release message to be homogeneous.
- Create functions to generate changelog on release.