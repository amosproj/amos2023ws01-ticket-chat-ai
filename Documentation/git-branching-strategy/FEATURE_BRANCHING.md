# Git Branching Strategy

We use the Feature Branching strategy. For a detailed explanation of the Feature Branching workflow, please refer to [Tilburgsciencehub](https://tilburgsciencehub.com/building-blocks/collaborate-and-share-your-work/use-github/git-branching-strategies/?ref=hutte.io).

## Feature Branching Strategy

- We follow the branch naming convention `<BRANCHTYPE>/<ISSUENUMBER>-<DESCRIPTION>` (e.g., feature/10-add-new-input-field). Potential branch types are:
  - feature
  - refactoring
  - bugfix

- We use GitHub or the following command to create branches for issues:
  ```
  git checkout -b feature/10-add-new-input-field
  ```

- We commit/push code changes to feature/refactoring/bugfix branches and merge them into main. In contrast, we can push changes inside `Deliverables` or `Documentation` directly onto main.

## Ensuring Code Quality

To ensure that changes are only made through pull requests, we implement the following measures:

- **Merge Policy:** Changes in the main branch are only made via pull requests. This does not apply to Product Owners (POs) and the Scrum Master, who can commit deliveries directly on main without pull requests.

- **Branch Permissions:** Only specific users - i.e. Release Managers, POs, and the Scrum Master - have the permission to merge directly into the main branch ensuring quality requirements. That also applies to pushing changes directly onto main. Pull requests can be merged by everbody, if they were reviewed by at least one independent person.

## Sprint Release Process

- Release day: before **Tuesday 3 pm**, every team member must merge their feature branch into the main branch, unless the work isn't finished yet. After that, further merges into the main branch are forbidden until the release is completely done.
- The Release Manager is responsible for creating the release and follows a defined process:
    1. Create a new tag for a release candidate in the format `sprint-<NUMBER>-release-candidate`
    2. Compile, build, and run tests for release candidate
    3. **IF** candidate isn't stable, **THAN** fix the bugs and continue with step 1 **OR** (in worst case) stop release process and initiate bug fixing for the next sprint, **ELSE** continue with step 4
    4. Finish with a new release tag `sprint-<NUMBER>-release` and deploy release version to prod
- The Release Manager can address bug fixes until the team meeting on Wednesday.
- During the Wednesday team meeting: the Release Manager adds a new record under "Releases" on the GitHub repository

## CI/CD Workflow (Draft)

- **Trigger:** Our CI/CD workflow is triggered on branch push events and by tags (releases)
- **Build Job Steps:** Our CI/CD workflow includes the following build job steps:
  1. Install dependencies
  2. Build artifacts
  3. Execute test code
  4. Ensure minimum test coverage
  5. **RELEASE** only: upload artifacts to GitHub registry and create new release on the GitHub repository
