Run Jenkins locally (Docker)

docker run -p 8080:8080 --name jenkins -d jenkins/jenkins:lts


# minimal-secure-ci-demo

Minimal repo to demonstrate CI/CD concepts with GitHub Actions:
- pytest tests
- coverage reports (XML + HTML)
- bandit static scanning
- pip-audit dependency scanning
- one consolidated HTML security dashboard

## Run locally
pip install -r requirements.txt
pytest -v --cov=app --cov-report=term --cov-report=html

## Generate dashboard locally
pytest --junitxml=test_results.xml --cov=app --cov-report=xml
bandit -r app -f json -o bandit.json
pip-audit -f json -o dependencies.json
python generate_dashboard.py
open security_dashboard.html


git init
git add .
git commit -m "Minimal CI demo: tests + coverage + security dashboard"
git branch -M main
git remote add origin https://github.com/YOURNAME/minimal-secure-ci-demo.git
git push -u origin main

macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip


Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip


Windows (cmd.exe)
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip

Install Dependencies
pip install -r requirements.txt

Run Tests Locally
pytest -v

Run Coverage Locally (Terminal + HTML)
pytest -v --cov=app --cov-report=term --cov-report=xml --cov-report=html


macOS
open htmlcov/index.html

Linux
xdg-open htmlcov/index.html

Windows (PowerShell)
start htmlcov\index.html

Run Security Scans Locally
Static Analysis (Bandit)
bandit -r app

Dependency Vulnerability Scan (pip-audit)
pip-audit

Generate the Consolidated Security Dashboard (HTML)
pytest --junitxml=test_results.xml --cov=app --cov-report=xml
bandit -r app -f json -o bandit.json
pip-audit -f json -o dependencies.json
python generate_dashboard.py


macOS
open security_dashboard.html
Linux
xdg-open security_dashboard.html
Windows (PowerShell)
start security_dashboard.html



How to run it

GitHub Actions runs automatically when you:

push commits to GitHub, or
open a pull request
Where to find outputs (artifacts)
Go to your repo on GitHub
Click Actions
Click the latest workflow run
Scroll to Artifacts
Download:
coverage-html
security-artifacts (includes security_dashboard.html, scan JSON, and test/coverage XML)

deactivate
Jenkins Demo
docker run -p 8080:8080 --name jenkins -d jenkins/jenkins:lts

pytest --cov=app --cov-fail-under=85

add GitHub Pages workflow

add GitHub Pages workflow


Enable GitHub Pages in the repo settings

On GitHub:

Repo → Settings
Pages
Under Build and deployment:
Source: GitHub Actions

git add .github/workflows/pages.yml
git commit -m "Add GitHub Pages dashboard workflow"
git push

Repo → Actions → “Publish Security Dashboard to GitHub Pages”
Or Repo → Settings → Pages
''pytest --cov=app --cov-report=term-missing --cov-report=xml --cov-report=html






