progress-crm
============

An open source CRM designed for the Code for Progress curriculum final project.  Provides a flexible framework for aggregating data from many vendors into one central database.

Setup
-----

To activate the pre-commit script, create a symbolic link between the pre-commit file in the "scripts" folder to .git/git-hook/pre-commit.

Development Instructions
------------------------

To contribute to this project:

1. Create an issue on github for your new feature
2. Create a fork
3. Clone your fork, and create a new feature branch off the "develop" branch, named "feature_<yourfeature>"
4. Make changes, commit, rebasing if necessary to consolidate commits (http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html), then push.
5. Make sure to include tests!
6. Once done, issue a pull request against progress-crm@develop
7. Add the main repo as an upstream remote: (https://help.github.com/articles/syncing-a-fork) and merge changes to your local branch after the PR is accepted.
8. Do it again!