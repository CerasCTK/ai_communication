# Commit Convention for DASH Project

This project follows a clean and structured commit style based on **Conventional Commits**. All contributions should follow this format to ensure a clear and maintainable Git history.

---

## 🧩 Commit Message Format

```
<type>(optional-scope): <subject>

<body> (optional)

<footer> (optional)
```

### ✅ Rules
- Use **English** for all commit messages.
- Use **present tense** and **imperative mood** (e.g., `add feature`, not `added feature` or `adds feature`).
- Keep the **subject under 50 characters**. If you need more than 50 characters, you're probably doing too much in this commit, split it into smaller commits.
- Keep **each line of body under 70 characters**.
- **Do not** end the subject with a period.

---

## 🎯 Allowed Commit Types

| Type        | Description |
|------------|------------|
| `feat`      | Add a new feature |
| `fix`       | Fix a bug |
| `refactor`  | Refactor code without changing functionality |
| `style`     | Code style changes (formatting, naming, PEP8 fixes) |
| `build`     | Changes related to build system, Docker or dependencies |
| `docs`      | Documentation only changes (README, comments) |
| `test`      | Add or update tests |
| `chore`     | Maintenance tasks, setup scripts, gitignore, CI setup |
| `perf`      | Performance improvements |

---

## 📌 Examples

```
feat(api): add endpoint for user communication
```
```
fix(auth): correct token validation logic
```
```
style: apply black formatting
```
```
build: update Dockerfile to use Python 3.15-slim
```
```
refactor(views): simplify chat message processing
```
```
docs: update README with Docker usage instructions
```

---

## 🔧 Optional Sections

### Body (`<body>`) — when to use
Use when the change needs more explanation, especially for **why** it was done.

```
refactor(chat): remove redundant query in message view

Reduces database calls and improves response time for chat endpoints.
```

### Footer (`<footer>`) — when to use
- Reference issues: `Closes #12`
- Breaking changes: `BREAKING CHANGE: ...`

```
feat(api): change message payload format

BREAKING CHANGE: Payload now includes timestamp and user ID fields
```

---

## 🚀 Recommended Workflow
1. Stage your changes: `git add .`
2. Create commit (2 options):
   - **Option A - Short Commit** (for small changes, no body needed):
     `git commit -m "type(scope): subject"`
   - **Option B - Full Commit** (for meaningful changes, with body/footer):
     `git commit` → then write full message using editor
3. Push with clean history

> Example: `git commit -m "feat(chat): add real-time message broadcasting"`
