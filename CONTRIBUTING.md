# Contributing to APTS

Thank you for your interest in contributing to the OWASP Autonomous Penetration Testing Standard (APTS). This guide covers everything you need to get started.

## Code of Conduct

This project follows the [OWASP Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you are expected to uphold it.

## How You Can Help

### Report Issues

Found a gap, inconsistency, or error? [Open an issue](https://github.com/OWASP/APTS/issues):

- Search existing issues first to avoid duplicates
- Provide specific details: which requirement, what's wrong, and a suggested fix if you have one
- Use descriptive titles (for example, "APTS-SE-003: Ambiguous scope boundary definition")

### Improve Documentation

- Fix typos, clarify wording, or improve examples
- Add implementation guidance or practical context to requirements
- Improve cross-references between domains

### Translations

Help make APTS available in other languages. Propose a new language by opening an issue and coordinating with the project leads before starting. See the [translations directory](./standard/translations/) for structure.

## Getting Started

### Prerequisites

- GitHub account
- Git installed locally
- Familiarity with Markdown
- Read the [standard](./standard/README.md) to understand the structure

### Setup

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/<your-github-username>/APTS.git
cd APTS

# Add upstream remote
git remote add upstream https://github.com/OWASP/APTS.git

# Create a branch for your work
git checkout -b your-branch-name
```

### Branch Naming

- `docs/improve-scope-enforcement` - documentation improvements
- `fix/correct-typo-ar-section` - corrections
- `feat/add-glossary-terms` - new content

## Making Changes

1. Keep changes focused. One logical change per PR
2. Follow the existing style and formatting conventions
3. Update related sections if your change affects cross-references
4. Test that all Markdown links work locally

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
type: brief description

Optional longer explanation of what changed and why.
Reference issues with #123.
```

**Types:** `docs:` (content changes), `fix:` (corrections), `feat:` (new content), `refactor:` (restructuring), `style:` (formatting only)

Example:

```
docs: clarify Tier 2 human supervision requirements

Add explicit decision points where Tier 2 systems must pause for
human approval. Addresses #42.
```

## Pull Requests

When opening a PR:

- Describe what you changed and why
- Link related issues (for example, "Fixes #123")
- List the affected sections or requirement IDs
- Confirm that formatting is consistent and links work

### What Reviewers Look For

- Accuracy of technical content
- Consistency with the rest of the standard
- Clear, direct writing
- Proper Markdown formatting

## Style Guidelines

- **Language:** Clear, direct, professional English
- **Perspective:** Vendor-neutral and organization-neutral
- **Terminology:** Use "Tier 1/2/3" (not "Level"), "Rules of Engagement" (capitalized), "kill switch" (two words), "customers" or "reviewers" (not "assessors")
- **Tier names:** Tier 1 (Foundation), Tier 2 (Verified), Tier 3 (Comprehensive). Do not use "Foundational", "Standard", "Advanced", or other variants
- **Autonomy level labels:** L1 Assisted, L2 Supervised, L3 Semi-Autonomous, L4 Autonomous. Short forms (L1, L2, L3, L4) are acceptable in tables and inline references
- **Bullet points:** No trailing periods on sentence fragments
- **Requirement IDs:** Follow `APTS-XX-NNN` format for tier-gated requirements (for example, APTS-SE-001). Appendix-only advisory requirements use a separate ID space: `APTS-XX-A<NN>` (for example, APTS-TP-A01). The `A` prefix on the number segment prevents any collision between active and advisory ID sequences, so contributors may number new tier-gated requirements sequentially without consulting the advisory appendix
- **Normative language:** Follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) (MUST, SHOULD, MAY)
- **Normative language consistency:** The first normative verb (MUST, SHOULD, MAY) in a requirement's body text MUST match the Classification line. If Classification says SHOULD, the body MUST NOT start with MUST
- **Writing style:** Write directly and concisely. Avoid unnecessarily complex sentence structures

## Proposing New Requirements

### Version freeze policy

The normative requirement set (tier-gated requirements counted toward conformance) is frozen for each released version. New normative requirements are not merged into the current release branch. Instead, they are reviewed during the next version cycle and, if accepted, batched into that release so that requirement counts change only once per version.

New advisory requirements (non-normative, documented in the Advisory Requirements appendix) may be accepted between releases because they do not affect conformance counts or tier definitions.

Enhancements to existing requirements (adding sub-requirements, strengthening language, expanding Implementation Guide content) may be accepted between releases as long as they do not change the requirement count or alter the tier classification.

The current version is **v0.1.0**. New normative requirements submitted now will be tagged as **v0.2.0-candidate** and tracked via GitHub issues until the v0.2.0 cycle opens.

### Proposal format

To propose a new requirement, open an issue first with the following fields. Do not submit a PR with cross-cutting count changes until the proposal has been reviewed and accepted for a target version.

- **ID:** Next available ID in the target domain. For a tier-gated requirement, use the next sequential number (for example, APTS-SE-027). For an advisory requirement, use the next sequential `A<NN>` number in the target domain (for example, APTS-SE-A01 if no SE advisory exists yet, or APTS-TP-A04 as the next TP advisory). Tier-gated and advisory IDs are in separate sequences and do not collide
- **Title:** Concise requirement name
- **Classification:** MUST, SHOULD, or MAY
- **Tier:** 1, 2, or 3
- **Requirement body:** What the platform must or should do, using RFC 2119 language
- **Rationale:** Why this requirement matters (business impact, risk it mitigates)
- **Verification:** Specific, testable criteria a customer could use to verify compliance
- **Cross-references:** Related requirements in other domains (use `> **See also:** APTS-XX-NNN` format)
- **Advisory flag:** If the requirement represents a best practice rather than a tier-gated obligation, mark it as Advisory. Advisory requirements are documented in the [Advisory Requirements](./standard/appendix/Advisory_Requirements.md) appendix
- **Framework mappings:** Applicable NIST CSF, ISO 27001, or other framework controls

## AI-Assisted Contributions

Contributions that were generated or substantially assisted by AI tools (including but not limited to LLMs, coding agents, and automated PR generators) are accepted, provided:

1. The contributor discloses AI involvement in the PR description (for example, "Drafted with assistance from [tool name]")
2. The contributor has reviewed the changes for accuracy, consistency with the standard, and compliance with the style guide
3. The contributor takes full ownership of the submission and can respond to review feedback

PRs submitted by fully automated agents without a responsible human author will not be merged. A human must stand behind every contribution.

## Licensing

By contributing, you agree that:

1. Your contributions are provided under the [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license
2. You have the right to contribute the material
3. Your contributions may be modified or adapted

## Recognition

All contributors are acknowledged in [ACKNOWLEDGEMENTS.md](./ACKNOWLEDGEMENTS.md). Submit a PR adding your name to the Contributors table.

## Questions?

- Search [existing issues](https://github.com/OWASP/APTS/issues)
- Ask in [GitHub Discussions](https://github.com/OWASP/APTS/discussions)
- Contact the project lead (see [Frontispiece](./standard/Frontispiece.md))
- Project roles and governance: see [GOVERNANCE.md](./GOVERNANCE.md)
- Security concerns: see [SECURITY.md](./SECURITY.md)
