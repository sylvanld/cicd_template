# ChangeLog

> Below are described significant changes that occured in this project...

## Releases

### 0.0.2 - 2020-12-22

**Feature**

- Automatic changelog generation.
	- Simple changelog generation.
- Command to fix previous commit.
	- Add docstring to 'fix_previous_commit'.
	- Add logic for fix command.
	- Add parser for 'fix' command.
- Add init command.
	- Generate project assets using init command.
	- Create changelog and bump setup on init.
	- Add parser for init command.
- Add release command.
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

**Bugfix**

- Fix changelog format.
	- Add spacing between releases.
	- Add heading style to new release title.
	- Manually update changelog.

**Devops**

- Restructure package.
	- Remove one level of nesting in structure.

## Unreleased work