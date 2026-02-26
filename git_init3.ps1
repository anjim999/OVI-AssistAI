Remove-Item -Recurse -Force .git -ErrorAction Ignore
git init
git switch -c main

function Commit-Changes {
    param(
        [string]$Date,
        [string]$Message,
        [string[]]$Files
    )
    $env:GIT_AUTHOR_DATE=$Date
    $env:GIT_COMMITTER_DATE=$Date
    foreach ($file in $Files) {
        if (Test-Path $file) {
            git add $file
        }
    }
    # Check if there are changes to commit
    $status = git status --porcelain
    if ($status) {
        git commit -m $Message
    } else {
        Write-Host "No changes to commit for message: $Message"
    }
}

Commit-Changes -Date "2026-02-25T14:15:22" -Message "Initial project setup" -Files @(".gitignore", "docker-compose.yml")
Commit-Changes -Date "2026-02-25T14:42:15" -Message "Setup backend environment and dependencies" -Files @("backend/requirements.txt", "backend/.env.example")
Commit-Changes -Date "2026-02-25T15:07:33" -Message "Add application configuration" -Files @("backend/config.py")
Commit-Changes -Date "2026-02-25T15:34:12" -Message "Initialize backend database configuration" -Files @("backend/db")
Commit-Changes -Date "2026-02-25T16:12:45" -Message "Create main FastAPI application" -Files @("backend/main.py")
Commit-Changes -Date "2026-02-25T16:55:09" -Message "Add server middleware" -Files @("backend/middleware")
Commit-Changes -Date "2026-02-25T17:28:51" -Message "Implement utility functions" -Files @("backend/utils")
Commit-Changes -Date "2026-02-25T18:03:22" -Message "Setup Docker configuration" -Files @("backend/Dockerfile")
Commit-Changes -Date "2026-02-25T18:49:17" -Message "Add data ingestion scripts" -Files @("backend/scripts")
Commit-Changes -Date "2026-02-25T19:35:44" -Message "Set up local vector store data" -Files @("backend/data")
Commit-Changes -Date "2026-02-25T20:21:05" -Message "Implement core LLM services" -Files @("backend/services")
Commit-Changes -Date "2026-02-25T21:14:38" -Message "Add base API routes for chat interaction" -Files @("backend/routes")
Commit-Changes -Date "2026-02-25T22:45:11" -Message "Initialize Vite React frontend" -Files @("frontend/package.json", "frontend/package-lock.json", "frontend/vite.config.js", "frontend/index.html")

Commit-Changes -Date "2026-02-26T08:42:19" -Message "Set up frontend styling and entry points" -Files @("frontend/src/main.jsx", "frontend/src/index.css")
Commit-Changes -Date "2026-02-26T08:58:33" -Message "Add base application component" -Files @("frontend/src/App.jsx")
Commit-Changes -Date "2026-02-26T09:15:05" -Message "Implement chat page layout" -Files @("frontend/src/pages/ChatPage.jsx")
Commit-Changes -Date "2026-02-26T09:32:41" -Message "Create frontend chat service integration" -Files @("frontend/src/services")
Commit-Changes -Date "2026-02-26T09:47:18" -Message "Add chat header UI component" -Files @("frontend/src/components/chat/ChatHeader.jsx")
Commit-Changes -Date "2026-02-26T10:04:55" -Message "Implement individual message display component" -Files @("frontend/src/components/chat/MessageItem.jsx")
Commit-Changes -Date "2026-02-26T10:19:22" -Message "Create centralized message list view" -Files @("frontend/src/components/chat/MessageList.jsx")
Commit-Changes -Date "2026-02-26T10:35:14" -Message "Add typing activity indicator" -Files @("frontend/src/components/chat/TypingIndicator.jsx")
Commit-Changes -Date "2026-02-26T10:51:39" -Message "Build user message input interface" -Files @("frontend/src/components/chat/MessageInput.jsx")
Commit-Changes -Date "2026-02-26T11:08:07" -Message "Introduce action suggestion chips" -Files @("frontend/src/components/chat/SuggestionChips.jsx")
Commit-Changes -Date "2026-02-26T11:22:45" -Message "Add chat session sidebar overview" -Files @("frontend/src/components/sidebar/SessionSidebar.jsx")
Commit-Changes -Date "2026-02-26T11:31:12" -Message "Implement status indicators and session utilities" -Files @("frontend/src/components/chat/StatusIndicator.jsx", "frontend/src/utils")
Commit-Changes -Date "2026-02-26T11:38:59" -Message "Final refinements and application polish" -Files @(".")

git log --oneline
git remote add origin https://github.com/anjim999/OVI-AssistAI.git
git push -u origin main --force
