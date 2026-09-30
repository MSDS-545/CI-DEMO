# Minimal Secure CI/CD Demo

A small Python project that demonstrates a basic secure CI/CD workflow
using GitHub Actions.

The repository includes:

-   Automated tests with `pytest`
-   Code coverage reports
-   Static security scanning with Bandit
-   Dependency vulnerability scanning with `pip-audit`
-   A consolidated HTML security dashboard
-   GitHub Actions artifacts
-   Optional Jenkins support
-   Optional GitHub Pages publishing

## Project Workflow

``` text
Code Change
    |
    v
GitHub Push / Pull Request
    |
    v
GitHub Actions
    |
    +------------------------------+
    |              |               |
    v              v               v
pytest         Bandit          pip-audit
    |              |               |
    +--------------+---------------+
                   |
                   v
          Coverage + Scan Files
                   |
                   v
        Security Dashboard HTML
                   |
          +--------+--------+
          |                 |
          v                 v
   GitHub Artifacts   GitHub Pages
```

## Requirements

-   Python 3.10 or later
-   `pip`
-   Git
-   GitHub account

Optional:

-   Docker
-   Jenkins

## 1. Clone the Repository

``` bash
git clone <repo-url>
cd CI-DEMO
```

If you are creating the repository locally first:

``` bash
git init
git add .
git commit -m "Initial secure CI demo"
git branch -M main
git remote add origin https://github.com/YOURNAME/CI-DEMO.git
git push -u origin main
```

## 2. Create a Virtual Environment

### macOS / Linux

``` bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### Windows PowerShell

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

### Windows Command Prompt

``` cmd
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
```

## 3. Install Dependencies

``` bash
python -m pip install -r requirements.txt
```

The project should include the packages needed for testing, coverage,
and security scanning, such as:

``` text
pytest
pytest-cov
bandit
pip-audit
```

> **Important:** `pytest-cov` is required for the coverage options used
> in this repository. The options `--cov`, `--cov-report`, and
> `--cov-fail-under` come from `pytest-cov`, not from `pytest` itself.
>
> If pytest reports `unrecognized arguments: --cov=app ...`, install the
> testing and coverage packages in the active virtual environment:
>
> ``` bash
> python -m pip install pytest pytest-cov
> ```
>
> Verify the plugin with:
>
> ``` bash
> python -m pytest --help | grep cov
> ```
>
> Normally, `python -m pip install -r requirements.txt` installs
> `pytest-cov` automatically because it should be included in
> `requirements.txt`.

## 4. Run Tests Locally

Run:

``` bash
python -m pytest -v
```

This executes the test suite and shows detailed test results.

## 5. Run Coverage Locally

Run:

``` bash
python -m pytest -v   --cov=app   --cov-report=term   --cov-report=xml   --cov-report=html
```

This creates:

``` text
coverage.xml
htmlcov/
```

To open the HTML coverage report:

### macOS

``` bash
open htmlcov/index.html
```

### Linux

``` bash
xdg-open htmlcov/index.html
```

### Windows PowerShell

``` powershell
start htmlcov\index.html
```

## 6. Enforce a Coverage Threshold

To require at least 85% coverage:

``` bash
python -m pytest --cov=app --cov-fail-under=85
```

If coverage falls below the threshold, the command exits with a failure
status. This is useful in CI because it can block a workflow when test
coverage drops below the required level.

## 7. Run Bandit

Run Bandit against the application directory:

``` bash
bandit -r app
```

To save the results as JSON:

``` bash
bandit -r app -f json -o bandit.json
```

Bandit checks Python code for common security issues and risky coding
patterns.

## 8. Run pip-audit

Run:

``` bash
pip-audit
```

To save dependency scan results:

``` bash
pip-audit -f json -o dependencies.json
```

`pip-audit` checks installed Python dependencies against known
vulnerability advisories.

## 9. Generate the Consolidated Security Dashboard

Create the test, coverage, and scan files first:

``` bash
python -m pytest --junitxml=test_results.xml --cov=app --cov-report=xml
bandit -r app -f json -o bandit.json
pip-audit -f json -o dependencies.json
```

Then generate the dashboard:

``` bash
python generate_dashboard.py
```

Expected output:

``` text
security_dashboard.html
```

Open it with:

### macOS

``` bash
open security_dashboard.html
```

### Linux

``` bash
xdg-open security_dashboard.html
```

### Windows PowerShell

``` powershell
start security_dashboard.html
```

The dashboard consolidates test, coverage, static-analysis, and
dependency-scan results into one HTML report.

## 10. Run the Full Local Security Workflow

For a full local check:

``` bash
python -m pytest --junitxml=test_results.xml   --cov=app   --cov-report=term   --cov-report=xml   --cov-report=html

bandit -r app -f json -o bandit.json

pip-audit -f json -o dependencies.json

python generate_dashboard.py
```

Then review:

``` text
htmlcov/index.html
security_dashboard.html
bandit.json
dependencies.json
test_results.xml
coverage.xml
```

## 11. GitHub Actions

GitHub Actions should run automatically when you:

-   Push commits to the repository
-   Open or update a pull request

A typical CI workflow can run:

1.  Dependency installation
2.  Unit tests
3.  Coverage collection
4.  Bandit
5.  `pip-audit`
6.  Security dashboard generation
7.  Artifact upload

## 12. View GitHub Actions Results

On GitHub:

1.  Open the repository.
2.  Click **Actions**.
3.  Open the latest workflow run.
4.  Review the job output.
5.  Scroll to **Artifacts**.

Typical artifacts include:

``` text
coverage-html
security-artifacts
```

`security-artifacts` may contain:

``` text
security_dashboard.html
bandit.json
dependencies.json
test_results.xml
coverage.xml
```

## 13. GitHub Pages

The generated security dashboard can also be published with GitHub
Pages.

Add a Pages workflow under:

``` text
.github/workflows/pages.yml
```

Commit and push the workflow:

``` bash
git add .github/workflows/pages.yml
git commit -m "Add GitHub Pages dashboard workflow"
git push
```

Then enable GitHub Pages:

1.  Open the repository on GitHub.
2.  Go to **Settings**.
3.  Select **Pages**.
4.  Under **Build and deployment**, set **Source** to **GitHub
    Actions**.

After the workflow runs, check:

``` text
Repository → Actions → Publish Security Dashboard to GitHub Pages
```

You can also verify the Pages configuration under:

``` text
Repository → Settings → Pages
```

## 14. Jenkins Demo

Jenkins can be run locally with Docker:

``` bash
docker run   -p 8080:8080   --name jenkins   -d   jenkins/jenkins:lts
```

Open Jenkins at:

``` text
http://localhost:8080
```

Confirm the container is running:

``` bash
docker ps
```

If you need the initial Jenkins administrator password:

``` bash
docker exec jenkins   cat /var/jenkins_home/secrets/initialAdminPassword
```

Follow the Jenkins setup wizard in the browser.

## 15. Jenkins Pipeline Example

A Jenkins pipeline for this repository can use the same local commands
as GitHub Actions:

``` bash
python -m pip install -r requirements.txt

python -m pytest -v   --cov=app   --cov-fail-under=85   --cov-report=xml   --cov-report=html

bandit -r app -f json -o bandit.json

pip-audit -f json -o dependencies.json

python generate_dashboard.py
```

The generated reports can then be archived as Jenkins build artifacts.

## 16. Recommended CI Checks

A practical CI pipeline should fail when:

-   Unit tests fail
-   Required coverage is not met
-   A configured Bandit severity threshold is exceeded
-   Dependency scanning detects vulnerabilities that violate project
    policy

The exact failure policy depends on the project and should be documented
in the workflow configuration.

## 17. Deactivate the Virtual Environment

When finished:

``` bash
deactivate
```

## Troubleshooting

### `pytest: command not found`

Activate the virtual environment and install dependencies:

``` bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

You can also run:

``` bash
python -m pytest -v
```

### `bandit: command not found`

Install Bandit:

``` bash
python -m pip install bandit
```

### `pip-audit: command not found`

Install `pip-audit`:

``` bash
python -m pip install pip-audit
```

### Coverage files are missing

Run:

``` bash
python -m pytest --cov=app --cov-report=xml --cov-report=html
```

### Security dashboard is missing

Make sure the input files exist:

``` text
test_results.xml
coverage.xml
bandit.json
dependencies.json
```

Then run:

``` bash
python generate_dashboard.py
```

### GitHub Pages deployment fails with `Failed to create deployment` or `HttpError: Not Found`

The CI checks can succeed while the GitHub Pages deployment fails. This
indicates a **CD/deployment configuration problem**, not necessarily a
test failure.

Configure GitHub Pages once:

1.  Open the repository on GitHub.
2.  Go to **Settings → Pages**.
3.  Under **Build and deployment**, set **Source** to **GitHub
    Actions**.
4.  Return to **Actions**.
5.  Open **Publish Security Dashboard to GitHub Pages**.
6.  Re-run the failed workflow or push another commit.

The Pages workflow also requires:

``` yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

If the error stack trace contains `node_modules`, that does not mean
Node.js dependencies must be installed for this Python project. GitHub
Actions themselves use packaged JavaScript actions. Focus on the
`Failed to create deployment` / `HttpError: Not Found` message.

This provides a useful CI/CD teaching example:

``` text
Tests + Coverage + Security Reports
              |
              v
          CI succeeds
              |
              v
       Pages deployment
              |
       configuration issue
              |
              v
           CD fails
```

A successful CI stage does not guarantee that the deployment environment
is configured correctly.

### Jenkins container already exists

If Docker reports that a container named `jenkins` already exists:

``` bash
docker start jenkins
```

Or remove and recreate it:

``` bash
docker rm -f jenkins
docker run -p 8080:8080 --name jenkins -d jenkins/jenkins:lts
```

## Notes

This repository is intended as a small CI/CD and DevSecOps
demonstration. The security scans are useful automated checks, but they
should be treated as part of a broader software assurance process rather
than a complete security assessment.

## 18. Classroom CI/CD Demonstration

The GitHub Actions workflow now enforces two blocking CI quality gates:

1.  All automated tests must pass.
2.  Application coverage must be at least **85%**.

The Bandit and `pip-audit` steps are intentionally **report-only** in
this teaching version. Their commands use `|| true`, allowing students
to compare a blocking quality gate with a non-blocking reporting step.
Removing `|| true` can be used later to demonstrate a stricter DevSecOps
policy.

For a guided one-hour demonstration, including an intentional failing
commit, recovery, artifact inspection, and CI-to-CD discussion, see:

``` text
CI_CD_CLASS_DEMO.md
```

### CI vs. CD in this repository

``` text
.github/workflows/ci.yml
    Push / Pull Request / Manual Run
              |
              v
    Tests + 85% Coverage Gate
              |
              v
    Security Reports + Artifacts

.github/workflows/pages.yaml
         Push to main
              |
              v
    Tests + 85% Coverage Gate
              |
              v
       Build Dashboard
              |
              v
       GitHub Pages Deploy
```

This separation is useful for teaching: `ci.yml` demonstrates
**Continuous Integration**, while `pages.yaml` demonstrates how a
validated change can continue into an automated **deployment** step.
