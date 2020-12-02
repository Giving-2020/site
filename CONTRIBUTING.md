# Contributing to Giving2020
We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Rules

1. **No force-pushes** or modifying the Git history in any way.
2. If you have direct access to the repository, **create a branch for your changes** and create a pull request for that branch. If not, create a branch on a fork of the repository and create a pull request from there.
    * It's common practice for a repository to reject direct pushes to `master`, so make branching a habit!
    * If PRing from your own fork, **ensure that "Allow edits from maintainers" is checked**. This gives permission for maintainers to commit changes directly to your fork, speeding up the review process.
3. **Adhere to the prevailing code style**, which we enforce using [`flake8`](http://flake8.pycqa.org/en/latest/index.html) and [`pre-commit`](https://pre-commit.com/).
    * Run `flake8` and `pre-commit` against your code **before** you push it. Your commit will be rejected by the build server if it fails to lint.
4. **Make great commits**. A well structured git log is key to a project's maintainability; it efficiently provides insight into when and *why* things were done for future maintainers of the project.
    * Commits should be as narrow in scope as possible. Commits that span hundreds of lines across multiple unrelated functions and/or files are very hard for maintainers to follow. After about a week they'll probably be hard for you to follow too.
    * Avoid making minor commits for fixing typos or linting errors. Since you've already set up a `pre-commit` hook to run the linting pipeline before a commit, you shouldn't be committing linting issues anyway.
    * A more in-depth guide to writing great commit messages can be found in Chris Beam's [*How to Write a Git Commit Message*](https://chris.beams.io/posts/git-commit/)
5. **Avoid frequent pushes to the main repository**. This goes for PRs opened against your fork as well. Our test build pipelines are triggered every time a push to the repository (or PR) is made. Try to batch your commits until you've finished working for that session, or you've reached a point where collaborators need your commits to continue their own work. This also provides you the opportunity to amend commits for minor changes rather than having to commit them on their own because you've already pushed.
    * This includes merging master into your branch. Try to leave merging from master for after your PR passes review; a maintainer will bring your PR up to date before merging. Exceptions to this include: resolving merge conflicts, needing something that was pushed to master for your branch, or something was pushed to master that could potentionally affect the functionality of what you're writing.
6. **Don't fight the framework**. Every framework has its flaws, but the frameworks we've picked out have been carefully chosen for their particular merits. If you can avoid it, please resist reimplementing swathes of framework logic - the work has already been done for you!
7. If someone is working on an issue or pull request, **do not open your own pull request for the same task**. Instead, collaborate with the author(s) of the existing pull request. Duplicate PRs opened without communicating with the other author(s) and/or maintainers will be closed. Communication is key, and there's no point in two separate implementations of the same thing.
    * One option is to fork the other contributor's repository and submit your changes to their branch with your own pull request. We suggest following these guidelines when interacting with their repository as well.
    * The author(s) of inactive PRs and claimed issues will be be pinged after a week of inactivity for an update. Continued inactivity may result in the issue being released back to the community and/or PR closure.
8. **Work as a team** and collaborate wherever possible. Keep things friendly and help each other out - these are shared projects and nobody likes to have their feet trodden on.

## We Use [Github Flow](https://guides.github.com/introduction/flow/index.html), So All Code Changes Happen Through Pull Requests
Pull requests are the best way to propose changes to the codebase (we use [Github Flow](https://guides.github.com/introduction/flow/index.html)). We actively welcome your pull requests:

1. Fork the repo and create your branch from `master`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License
In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using Github's [issues](https://github.com/briandk/transcriptase-atom/issues)
We use GitHub issues to track public bugs. Report a bug by [opening a new issue](); it's that easy!

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can. [Here is an good stackoverflow question](http://stackoverflow.com/q/12488905/180626) which includes sample code that *anyone* with a base R setup can run to reproduce what I was seeing
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

People *love* thorough bug reports. I'm not even kidding.

### Keeping your Pull Request updated

If a maintainer asks you to "rebase" your PR, they're saying that a lot of code
has changed, and that you need to update your branch so it's easier to merge.

To learn more about rebasing in Git, there are a lot of [good][git rebasing]
[resources][interactive rebase] but here's the suggested workflow:

```sh
git checkout add-new-feature
git pull --rebase upstream main
git push --force-with-lease add-new-feature
```

## Merging a PR (maintainers only)

A PR can only be merged into master by a maintainer if:

* It is passing CI.
* It has been approved by at least two maintainers. If it was a maintainer who
  opened the PR, only one extra approval is needed.
* It has no requested changes.
* It is up to date with current master.

Any maintainer is allowed to merge a PR if all of these conditions are
met.
