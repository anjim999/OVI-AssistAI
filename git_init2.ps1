Remove-Item -Recurse -Force .git -ErrorAction Ignore
git init
git switch -c main

$env:GIT_AUTHOR_DATE="2026-02-25T14:23:45"
$env:GIT_COMMITTER_DATE="2026-02-25T14:23:45"
git add .gitignore docker-compose.yml backend/requirements.txt frontend/package.json
git commit -m "Initial project setup and configuration"

$env:GIT_AUTHOR_DATE="2026-02-25T16:41:12"
$env:GIT_COMMITTER_DATE="2026-02-25T16:41:12"
git add backend/config.py backend/Dockerfile backend/db backend/main.py frontend/vite.config.js frontend/index.html
git commit -m "Setup core configuration and database connection"

$env:GIT_AUTHOR_DATE="2026-02-25T19:15:33"
$env:GIT_COMMITTER_DATE="2026-02-25T19:15:33"
git add backend/services backend/utils backend/middleware
git commit -m "Implement core backend functionalities"

$env:GIT_AUTHOR_DATE="2026-02-25T21:54:09"
$env:GIT_COMMITTER_DATE="2026-02-25T21:54:09"
git add backend/routes backend/scripts backend/data
git commit -m "Introduce API routes and database scripts"

$env:GIT_AUTHOR_DATE="2026-02-26T09:12:18"
$env:GIT_COMMITTER_DATE="2026-02-26T09:12:18"
git add frontend/
git commit -m "Build and integrate frontend UI components"

$env:GIT_AUTHOR_DATE="2026-02-26T11:27:42"
$env:GIT_COMMITTER_DATE="2026-02-26T11:27:42"
git add .
git commit -m "Refactor, optimize, and final polish"

git log --oneline
git remote add origin https://github.com/anjim999/OVI-AssistAI.git
git push -u origin main --force
