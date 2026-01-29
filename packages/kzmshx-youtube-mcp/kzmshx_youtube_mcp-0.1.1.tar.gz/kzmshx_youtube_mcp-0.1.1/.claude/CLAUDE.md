# CLAUDE.md

## Conventional Commits

| type       | purpose                            |
| ---------- | ---------------------------------- |
| `feat`     | New feature                        |
| `fix`      | Bug fix                            |
| `docs`     | Documentation only                 |
| `refactor` | Code change (not fix nor feature)  |
| `test`     | Adding or modifying tests          |
| `chore`    | Build process or tooling changes   |

## Branch Naming

Format: `{type}/{description}` (e.g., `feat/add-playlist-support`, `fix/url-parsing`)

## PR Review Handling

| Operation      | Command                                                                                     |
| -------------- | ------------------------------------------------------------------------------------------- |
| Check CI       | `gh pr checks {n}`                                                                          |
| Get comments   | `gh api repos/{owner}/{repo}/pulls/{n}/comments`                                            |
| Reply          | `gh api repos/{owner}/{repo}/pulls/{n}/comments/{comment_id}/replies -X POST -f body="..."` |

Reply to comments with commit hash after fixes.

## Documentation Rules

- No emojis
- No horizontal rules (`---`)
- State facts concisely
- Show concrete examples for code and config

### Security (Important)

Prohibited in tracked files:

- Private keys, tokens, passwords, API keys
- Personally identifiable information
- Local environment paths (e.g., `/Users/username/`)

Use `.claude.local.md` for local-only information.
