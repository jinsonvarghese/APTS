# Governance

This document defines the roles, responsibilities, and decision-making processes for the OWASP Autonomous Penetration Testing Standard (APTS). It applies to all participants in the project and aligns with [OWASP's Project Policy](https://owasp.org/www-policy/operational/projects).

## Roles

### Contributor

Anyone who participates in the project through issues, pull requests, discussions, or translations. No membership or approval is required. All contributions are subject to review before merging.

Contributors are expected to:

- Follow the [Code of Conduct](./CODE_OF_CONDUCT.md)
- Follow the style and formatting conventions in [CONTRIBUTING.md](./CONTRIBUTING.md)
- Engage constructively in issue discussions and PR reviews

### Technical Reviewer

Technical reviewers evaluate pull requests for technical accuracy, structural consistency, normative language compliance, and alignment with the standard's goals. They are the quality gate for all changes to the standard.

Technical reviewers are expected to:

- Review PRs within a reasonable timeframe (target: within two weeks of assignment)
- Verify that changes are accurate, consistent with existing requirements, and follow the style guide
- Flag normative language issues (RFC 2119 misuse, classification mismatches, tier assignment questions)
- Identify cross-domain impacts that the author may have missed
- Provide clear, actionable feedback

**How to become a technical reviewer:** A contributor who has demonstrated sustained, quality engagement with the project (typically three or more merged PRs or substantive reviews on others' PRs) may be nominated by a project lead. The nomination is approved by majority vote of existing project leads. Technical reviewers are listed in the [Acknowledgements](./ACKNOWLEDGEMENTS.md).

There is no fixed cap on the number of technical reviewers. More reviewers improve review throughput and coverage.

### Project Lead

Project leads are responsible for the overall direction, quality, and OWASP compliance of the standard. They make final decisions on scope, structure, release timing, and disputes that cannot be resolved through reviewer consensus.

Project leads are responsible for:

- Setting the roadmap and prioritizing work across releases
- Approving or rejecting changes that affect the standard's scope, tier structure, or domain organization
- Ensuring the project complies with OWASP policies
- Representing the project to the OWASP Foundation and the broader community
- Responding to security reports per [SECURITY.md](./SECURITY.md)
- Managing releases and version tagging

**How to become a project lead:** A technical reviewer with an extended track record of high-quality reviews and demonstrated judgment on scope and direction decisions may be nominated by an existing project lead. Appointment requires approval from a majority of current project leads.

Per OWASP policy, each project must have a minimum of 2 and a maximum of 5 leaders. APTS targets a working maximum of 3 project leads to keep decision-making focused while providing redundancy. Leadership is personal. A project lead's role belongs to them as an individual and is not contingent on their employer or organizational affiliation.

## Decision-Making

Day-to-day decisions (merging PRs, triaging issues, editorial fixes) are made by any technical reviewer or project lead. Decisions that affect the standard's scope, tier definitions, domain structure, or governance model require approval from a majority of project leads.

If a dispute arises that project leads cannot resolve by majority vote, the matter is escalated to the [OWASP Project Committee](https://owasp.org/www-committee-project/).

## Progression Path

The path from contributor to project lead is merit-based:

1. **Contributor**: Open issues, submit PRs, participate in discussions. No barrier to entry.
2. **Technical Reviewer**: Nominated by a project lead after sustained, quality contributions. Approved by majority of project leads.
3. **Project Lead**: Nominated by an existing project lead after demonstrated judgment as a reviewer. Approved by majority of current project leads. Subject to the OWASP 2-5 leader policy and the project's working cap of 3.

Progression is based on the quality and consistency of contributions, not volume. A contributor who submits three carefully researched requirements with proper rationale, verification procedures, and cross-domain analysis demonstrates more than one who submits twenty surface-level typo fixes.

## Inactivity and Removal

An appointed project lead who is inactive for six consecutive months (no reviews, no issues, no commits, no discussion participation) may be contacted by the other project leads to confirm continued interest. If there is no response within 30 days, the appointed lead may be removed by majority vote of the remaining leads, with notice to the OWASP Foundation.

Technical reviewers who become inactive are not formally removed but may be moved to an emeritus list in [Acknowledgements](./ACKNOWLEDGEMENTS.md) after 12 months of inactivity.

## Changes to This Document

Changes to this governance document require approval from a majority of project leads and a 14-day comment period on GitHub Discussions before merging.
