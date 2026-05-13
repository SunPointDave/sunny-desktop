# Sunny Desktop — Tasks

## Phase 1: Repository Setup
- [x] 1.1 Verify source code is clean and rebranded
  - Verified: `grep -r "Cherry Studio"` returns 0 (excluding `@cherrystudio` package refs)
  - Verified: `build/icon.png`, `build/icon.ico`, `build/icon.icns` exist and are the Sunny logo
- [x] 1.2 Create GitHub repository (or verify it exists)
  - Verified: `gh repo view SunPointDave/sunny-desktop` returns repo info
- [x] 1.3 Push rebranded code to GitHub
  - Verified: `git remote -v` shows `https://github.com/SunPointDave/sunny-desktop.git`
  - Verified: `git push origin main` succeeded
- [x] 1.4 Verify GitHub Actions is enabled for the repo
  - Verified: `gh api repos/SunPointDave/sunny-desktop/actions/permissions` returned `"enabled": true`

## Phase 2: CI/CD Pipeline
- [x] 2.1 Create `.github/workflows/build-windows.yml`
  - Workflow runs on `windows-latest`, installs Node.js 24, pnpm 10.27, runs `pnpm install --ignore-scripts`, `pnpm build:win:x64`, uploads `dist/*.exe`
  - Verified: file exists at `.github/workflows/build-windows.yml`
- [x] 2.2 Commit and push the workflow
  - Verified: pushed as part of `main` branch
- [x] 2.3 Trigger first GitHub Actions build
  - Verified: `gh workflow run build-windows.yml --repo SunPointDave/sunny-desktop` returned success
  - Run URL: https://github.com/SunPointDave/sunny-desktop/actions/runs/25818239867
- [x] 2.4 Monitor build and verify success
  - Verified: Build completed in 8m21s with all green checkmarks
  - Verified: All steps passed (setup, checkout, Node.js, pnpm, install, build, upload, complete)

## Phase 3: Verification & Delivery
- [x] 3.1 Download the Windows installer artifact
  - Verified: `gh run download 25818239867 --repo SunPointDave/sunny-desktop` produced `.exe` files
  - Files: `Sunny-1.0.0-x64-setup.exe` and `Sunny-1.0.0-x64-portable.exe`
- [x] 3.2 Verify artifact integrity
  - Verified: File sizes are 135 MB and 134 MB (within 50-200 MB range)
  - Verified: File names match `Sunny-*.exe`
  - Verified: `file` command confirms PE32 executable (GUI) Nullsoft Installer self-extracting archive
- [x] 3.3 Document the final artifact location
  - Updated `README.md` with download instructions pointing to GitHub Actions artifacts and Releases page
  - Verified: `git diff README.md` shows the update
  - Verified: `git push origin main` succeeded
- [x] 3.4 Update parent project status
  - Appended to `/home/azureuser/OpenCodeAzure/Projects/Sunny/Sunny.md` under Notes
