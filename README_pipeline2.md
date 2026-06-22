\# Pipeline 2 — CI/CD + Security Scanning



\*\*Owner:\*\* Abdul Rafay (F2023-546)  

\*\*Branch:\*\* pipeline-cicd  

\*\*Project:\*\* AutoHealOps — Self-Healing DevOps Pipeline



\---



\## What This Pipeline Does



Pipeline 2 automates testing, Docker image building, and security scanning

on every code push using GitHub Actions.



\## Pipeline Architecture



Push to GitHub

&#x20;     ↓

Job 1: test        → runs 5 pytest cases on Flask app

&#x20;     ↓ (only if tests pass)

Job 2: build       → builds Docker image from ./app

&#x20;     ↓ (only if build passes)

Job 3: security-scan → runs Trivy CVE scanner, uploads results



\## Jobs



| Job | Tool | Purpose |

|-----|------|---------|

| test | pytest | Validates all Flask routes |

| build | Docker | Builds container image |

| security-scan | Trivy | Scans for CRITICAL/HIGH CVEs |



\## Triggers



\- Push to main

\- Push to pipeline-cicd

\- Pull Requests targeting main



\## Files I Created



| File | Purpose |

|------|---------|

| .github/workflows/ci.yml | GitHub Actions pipeline definition |

| app/tests/test\_app.py | 5 pytest test cases |

| README\_pipeline2.md | This documentation file |



\## Tools Used



\- GitHub Actions — CI/CD automation

\- pytest — Python testing framework

\- Docker — Containerization

\- Trivy — Security vulnerability scanner by Aqua Security



\## How to Trigger the Pipeline



Make any change and push to pipeline-cicd branch:



git add .

git commit -m "your message"

git push origin pipeline-cicd



Then view live at: https://github.com/NazishKhalid2/autoheaops/actions

