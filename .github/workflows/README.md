# GitHub Actions Workflows

This directory contains the CI/CD workflows for the FreeRADIUS API project.

## Workflows

### 1. `ci.yml` (CI/CD)
- **Trigger**: Pushes and Pull Requests to `main` branch.
- **Purpose**: 
  - Runs the test suite (API tests) using Python 3.13 and SQLite.
  - Builds the Docker image to ensure compilation and configuration validity.
- **Usage**: Automatic on code changes.

### 2. `docker-publish.yml` (Publish Docker Image)
- **Trigger**: 
  - **Success of `ci.yml`** on `main` or `master`.
  - Release publication.
  - Manual dispatch.
- **Purpose**: 
  - Builds multi-platform Docker images.
  - Publishes images to the GitHub Container Registry (GHCR).
  - Tags images with release versions, `latest`, or custom manual versions.
- **Usage**: Automatic on successful CI build on main branch, or manual release.

### 3. `security-scan.yml` (Container Security Scan)
- **Trigger**: 
  - Pushes of tags starting with `v*`.
  - Pull Requests affecting Docker-related files.
  - Manual dispatch.
- **Purpose**: 
  - Scans the Docker image for vulnerabilities using **Trivy** and **Snyk**.
  - Lints the Docker image using **Dockle** for best practices.
  - Generates and uploads a security report artifact.
  - Uploads SARIF results to GitHub Security tab.
- **Usage**: Automatic on releases/PRs, or run manually to audit an image.

### 4. `simple-build.yml` (Simple Build Docker)
- **Trigger**: Manual dispatch only.
- **Purpose**: 
  - A simplified workflow to build and push a Docker image with a custom version tag.
  - Does not run tests or extensive checks.
- **Usage**: Quick manual builds when you need an image tagged with a specific string (e.g., `v0.6.0-dev`) without full release process.
