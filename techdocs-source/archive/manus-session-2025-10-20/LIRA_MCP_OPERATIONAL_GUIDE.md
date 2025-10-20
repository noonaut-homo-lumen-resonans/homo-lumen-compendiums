# 🌿 Lira MCP Operational Guide

**Version:** 1.0  
**Date:** 16. oktober 2025  
**For:** Lira (ChatGPT-5) & Homo Lumen Developers  
**Formål:** This guide provides a complete overview of the MCP infrastructure and instructions on how to use it for ontological audits.

---

## 📋 Infrastructure Overview

The MCP infrastructure is now fully operational and integrates Notion, GitHub, and Linear to automate the Triadisk Etikk validation process.

### Notion

- **Ontology Audit Database:** Tracks all ontological audits.
- **MCP Audit Log Database:** Logs all MCP operations for monitoring.

### GitHub

- **Repository:** `noonaut-homo-lumen-resonans/homo-lumen-compendiums`
- **PR Template:** A comprehensive template with the Triadisk Etikk checklist is automatically applied to all new pull requests.
- **Thalus Gate Workflow:** A GitHub Action that automatically validates PRs. It blocks merging if the `TH-OK` label is missing.
- **Labels:** `TH-OK`, `TH-REV`, `TH-STOP`, `TH-SHD`, `TH-DSN` for tracking the status of the ontological audit.

### Linear

- **Team:** `HOMO LUMEN`
- **Labels:** 10 labels for detailed issue tracking related to the Thalus Gate workflow.

---

## 🚀 End-to-End Workflow Validation

A test pull request has been created to demonstrate the complete workflow:

**Test PR:** [https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums/pull/1](https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums/pull/1)

### Validation Process

1.  **PR Creation:** When a developer creates a new pull request, the Triadisk Etikk checklist is automatically added to the PR description.
2.  **Thalus Gate Workflow:** The `thalus-gate.yml` GitHub Action is triggered.
3.  **Validation:** The workflow checks for the presence of the `TH-OK` label. If the label is not present, the workflow fails, and the PR is blocked from merging.
4.  **Ontological Audit:** A designated team member (e.g., Thalus) performs an ontological audit based on the PR content and the Triadisk Etikk checklist.
5.  **Labeling:** Based on the audit, the appropriate label (`TH-OK`, `TH-REV`, `TH-STOP`) is applied to the PR.
6.  **Merge:** Once the `TH-OK` label is applied, the workflow passes, and the PR can be merged.

---

## 👩‍💻 Developer Guide

### Creating a Pull Request

1.  Create a new branch for your changes.
2.  Make your code changes and commit them.
3.  Push your branch to the `homo-lumen-compendiums` repository.
4.  Create a new pull request on GitHub. The Triadisk Etikk PR template will be automatically applied.
5.  Fill out the Triadisk Etikk checklist in the PR description to the best of your ability.

### Requesting Thalus Validation

- Once the PR is created, mention `@thalus` in a comment to request an ontological audit.

### Handling `TH-REV` and `TH-STOP`

- If your PR receives a `TH-REV` or `TH-STOP` label, review the comments from Thalus for required changes.
- Make the necessary changes and push them to your branch.
- Mention `@thalus` again for re-validation.

### Merging a PR

- Once your PR has the `TH-OK` label and all other checks have passed, you can merge it.

---

## ❓ FAQ

**Q: What is Triadisk Etikk?**

A: Triadisk Etikk is an ethical framework with three ports: Kognitiv Suverenitet, Ontologisk Koherens, and Regenerativ Healing. It is used to validate that all changes align with the core principles of the Homo Lumen project.

**Q: Why is my PR blocked?**

A: Your PR is likely blocked because it is missing the `TH-OK` label. This means it has not yet been approved by the ontological audit process.

**Q: How do I get the `TH-OK` label?**

A: The `TH-OK` label is applied by a designated auditor (e.g., Thalus) after a successful ontological audit.

---

This completes the setup and handoff of the Lira MCP infrastructure. The system is now ready for use.

