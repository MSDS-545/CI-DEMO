# One-Hour CI/CD Classroom Demo

This exercise uses the repository's existing GitHub Actions workflows to demonstrate the CI/CD feedback loop without leaving broken code in the repository.

## Learning objectives

Students should be able to explain:

- how a push or pull request triggers CI;
- why automated tests act as a quality gate;
- how a coverage threshold can stop a pipeline;
- the difference between report-only security checks and blocking gates;
- what CI artifacts are;
- how a successful build can proceed to deployment.

## Part 1 — Establish a green baseline

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest --cov=app --cov-fail-under=85 -v
```

Push the working code and open **GitHub → Actions**. Open the `Minimal CI - Tests, Coverage, Security, Dashboard` workflow and identify each pipeline step.

## Part 2 — Intentionally make CI fail

Open `app/calc.py`. The correct `add()` function is:

```python
def add(a: int, b: int) -> int:
    return a + b
```

For the demonstration only, change the return statement to:

```python
return a - b
```

Commit and push the intentionally broken change:

```bash
git add app/calc.py
git commit -m "Demo: intentionally break add function"
git push
```

Open **GitHub → Actions** and inspect the failed run. The `test_add()` test expects `add(2, 3)` to equal `5`, so the test gate should fail and later CI steps should not execute.

## Part 3 — Fix the code and observe recovery

Restore:

```python
return a + b
```

Then commit and push:

```bash
git add app/calc.py
git commit -m "Fix: restore add function"
git push
```

Observe the new workflow run. It should pass the test/coverage gate and continue to the security scans, dashboard generation, and artifact upload.

## Part 4 — Inspect artifacts

Open the successful workflow run and find **Artifacts**. Download or inspect:

- `coverage-html`
- `security-artifacts`

The security artifact bundle includes the JUnit test report, coverage XML, Bandit report, dependency audit, and consolidated dashboard.

## Part 5 — Explain the security policy

In `.github/workflows/ci.yml`, Bandit and `pip-audit` currently use `|| true`. This is intentional for the first classroom demo: findings are recorded, but they do not block the pipeline.

Ask students: **Should every security finding block deployment?**

To demonstrate a stricter DevSecOps gate later, remove `|| true` from a security command. Then a non-zero exit status from that tool can fail the job.

## Part 6 — Connect CI to CD

The `ci.yml` workflow demonstrates continuous integration. The `pages.yaml` workflow adds deployment: on a push to `main`, it runs the quality gate, generates the dashboard, prepares a Pages artifact, and deploys it to GitHub Pages.

Before using Pages, configure **Repository → Settings → Pages → Source → GitHub Actions**.

## Pipeline to draw in class

```text
Developer
   |
   | git push / pull request
   v
GitHub Repository
   |
   v
GitHub Actions
   |
   +--> Install dependencies
   |
   +--> Tests + 85% coverage gate ---- FAIL --> pipeline stops
   |
   +--> Bandit (report-only)
   |
   +--> pip-audit (report-only)
   |
   +--> Generate dashboard
   |
   +--> Upload artifacts
   |
   +--> GitHub Pages deployment (main branch workflow)
```

## Suggested timing

| Time | Demonstration |
|---|---|
| 0–10 min | Repository and workflow structure |
| 10–20 min | Run tests locally |
| 20–30 min | Read `ci.yml` and explain triggers/jobs/steps |
| 30–40 min | Intentionally break `add()` and push |
| 40–47 min | Inspect failed GitHub Actions run |
| 47–53 min | Fix, push, and observe successful CI |
| 53–57 min | Inspect coverage/security artifacts |
| 57–60 min | Connect CI to the Pages deployment workflow |
