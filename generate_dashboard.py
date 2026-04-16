import json
import xml.etree.ElementTree as ET
from jinja2 import Template

# -----------------------------
# Load pytest JUnit XML
# -----------------------------
tree = ET.parse("test_results.xml")
root = tree.getroot()

tests = failures = errors = 0

if root.tag == "testsuite":
    tests = int(root.attrib.get("tests", 0))
    failures = int(root.attrib.get("failures", 0))
    errors = int(root.attrib.get("errors", 0))
else:
    for suite in root.findall("testsuite"):
        tests += int(suite.attrib.get("tests", 0))
        failures += int(suite.attrib.get("failures", 0))
        errors += int(suite.attrib.get("errors", 0))

pass_rate = round(((tests - failures - errors) / tests) * 100, 2) if tests else 0

# -----------------------------
# Load coverage.xml
# -----------------------------
try:
    cov_tree = ET.parse("coverage.xml")
    cov_root = cov_tree.getroot()
    coverage_percent = round(float(cov_root.attrib.get("line-rate", 0)) * 100, 2)
except Exception:
    coverage_percent = 0

# -----------------------------
# Load Bandit report
# -----------------------------
try:
    with open("bandit.json") as f:
        bandit_data = json.load(f)
    issues = bandit_data.get("results", [])
    bandit_total = len(issues)
    high = sum(1 for i in issues if i.get("issue_severity") == "HIGH")
    medium = sum(1 for i in issues if i.get("issue_severity") == "MEDIUM")
    low = sum(1 for i in issues if i.get("issue_severity") == "LOW")
except Exception:
    bandit_total = high = medium = low = 0

# -----------------------------
# Load pip-audit report
# -----------------------------
try:
    with open("dependencies.json") as f:
        dep_data = json.load(f)
    dependency_vulns = len(dep_data)
except Exception:
    dependency_vulns = 0

risk_score = (high * 5) + (medium * 3) + (low * 1) + (dependency_vulns * 4)

html_template = """
<html>
<head>
<title>Minimal CI Security Dashboard</title>
<style>
body { font-family: Arial; background:#f4f4f4; padding:30px; }
h1 { color:#2c3e50; }
.card { background:white; padding:20px; margin:15px 0; border-radius:10px; box-shadow:0 2px 5px rgba(0,0,0,0.1); }
.good { color:green; font-weight:bold; }
.bad { color:red; font-weight:bold; }
.warning { color:orange; font-weight:bold; }
</style>
</head>
<body>

<h1>Minimal CI Security Dashboard</h1>

<div class="card">
<h2>Test Results</h2>
<p>Total Tests: {{ tests }}</p>
<p>Failures: <span class="{{ 'bad' if failures else 'good' }}">{{ failures }}</span></p>
<p>Errors: <span class="{{ 'bad' if errors else 'good' }}">{{ errors }}</span></p>
<p>Pass Rate:
  <span class="{% if pass_rate == 100 %}good{% elif pass_rate >= 80 %}warning{% else %}bad{% endif %}">
    {{ pass_rate }}%
  </span>
</p>
</div>

<div class="card">
<h2>Coverage</h2>
<p>Line Coverage:
  <span class="{% if coverage_percent >= 85 %}good{% elif coverage_percent >= 70 %}warning{% else %}bad{% endif %}">
    {{ coverage_percent }}%
  </span>
</p>
</div>

<div class="card">
<h2>Static Code Analysis (Bandit)</h2>
<p>Total Issues: <span class="{{ 'bad' if bandit_total else 'good' }}">{{ bandit_total }}</span></p>
<p>High: <span class="bad">{{ high }}</span> |
   Medium: <span class="warning">{{ medium }}</span> |
   Low: <span class="good">{{ low }}</span></p>
</div>

<div class="card">
<h2>Dependency Vulnerabilities (pip-audit)</h2>
<p>Detected: <span class="{{ 'bad' if dependency_vulns else 'good' }}">{{ dependency_vulns }}</span></p>
</div>

<div class="card">
<h2>Overall Risk Score</h2>
<p><span class="{% if risk_score > 10 %}bad{% elif risk_score > 5 %}warning{% else %}good{% endif %}">
  {{ risk_score }}
</span></p>
</div>

</body>
</html>
"""

out = Template(html_template).render(
    tests=tests, failures=failures, errors=errors, pass_rate=pass_rate,
    coverage_percent=coverage_percent,
    bandit_total=bandit_total, high=high, medium=medium, low=low,
    dependency_vulns=dependency_vulns, risk_score=risk_score
)

with open("security_dashboard.html", "w") as f:
    f.write(out)

print("✅ Generated security_dashboard.html")