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
- [ ] 3.1 Download the Windows installer artifact
  - Verify: `gh run download <run-id> --repo <org>/sunny-desktop --name installer` produces a `.exe`
- [ ] 3.2 Verify artifact integrity
  - Verify: File size is between 50 MB and 200 MB
  - Verify: File name matches `Sunny-*.exe`
- [ ] 3.3 Document the final artifact location
  - Update `README.md` at repo root with download instructions
  - Verify: `git -C cherry-studio-fork diff README.md` shows the update
  - Verify: `git -C cherry-studio-fork push origin main` succeeds
- [ ] 3.4 Update parent project status
  - Append one line to `/home/azureuser/OpenCodeAzure/Projects/Sunny/Sunny.md` under Notes: "Sunny Desktop v1.0.0 Windows installer built and available."
