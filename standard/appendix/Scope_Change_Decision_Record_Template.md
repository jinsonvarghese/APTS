# Scope Change Decision Record Template

This appendix is informative and does not create or modify APTS requirements.

## Purpose

Use this template to document decisions that add, remove, reject, constrain, or defer changes to an engagement's authorized scope. It supports scope enforcement, human approval, autonomy downgrade, and auditability controls by making the basis for each scope decision explicit before testing continues.

Scope change decisions are especially important when an autonomous platform discovers new assets, follows redirects, observes DNS or cloud drift, receives target-side suggestions, detects overlapping engagements, or needs customer confirmation before expanding activity. The record should explain what changed, who approved or rejected it, what evidence was reviewed, and what operational constraints apply after the decision.

The template should be tailored to the platform's Rules of Engagement, Authority Delegation Matrix, customer approval process, and audit trail implementation. It can be implemented as a ticket form, workflow approval record, policy-as-code artifact, or signed Markdown/YAML document.

This record should not redefine the Rules of Engagement, Authority Delegation Matrix, or Autonomy Downgrade Matrix; it records the decision, evidence, constraints, and approvals applied to a specific proposed scope change.

## When to Use This Template

Create or update a scope change decision record when:

- a new asset, domain, IP range, API endpoint, cloud account, tenant, or identity is proposed for testing
- a redirect chain, DNS change, cloud tag, CMDB update, deployment event, or discovered relationship suggests a scope change
- a customer, operator, or automated component requests scope expansion or restriction
- an asset is removed from active scope because authorization, ownership, availability, or time-window validity changed
- scope ambiguity requires temporary autonomy downgrade, testing pause, or customer confirmation
- an overlapping engagement creates a conflict between permissions or restrictions
- a proposed change is rejected and the rejection needs to remain auditable

## Decision Metadata

| Field | Example / guidance |
|-------|--------------------|
| Record ID | `scope-change-2026-05-001` |
| Engagement ID | Current engagement, cycle, or RoE identifier |
| Customer / environment | Customer name, tenant, environment, or business unit |
| APTS version | Version used for the engagement claim or review |
| Requester | Person, role, customer contact, workflow, or automated component requesting the change |
| Decision owner | Role authorized to approve, reject, or defer the decision |
| Authority reference | Authority Delegation Matrix ID/version, approval ticket, or signed customer amendment |
| Related RoE section | Scope, exclusions, time window, testing profile, or evidence section affected |
| Decision timestamp | UTC timestamp of approval, rejection, or deferral |
| Effective window | Start/end time or cycle where the decision applies |
| Record status | Draft, pending approval, approved, approved with constraints, rejected, superseded, expired |

## Requested Scope Change

| Field | Example / guidance |
|-------|--------------------|
| Change type | Add target, remove target, constrain target, approve exception, reject request, defer pending confirmation |
| Proposed target | Domain, URL, IP/CIDR, cloud resource, API, account, repository, tenant, agent deployment, or identity |
| Existing scope relationship | In current RoE, covered by wildcard, adjacent to in-scope target, shared tenant, out-of-scope, unknown |
| Source of discovery/request | Customer request, operator request, redirect chain, DNS drift, deployment trigger, CMDB/cloud inventory, target response, tool suggestion |
| Trigger evidence | Request/response trace, DNS answer, cloud tag, deployment event, customer ticket, screenshot, log entry, or asset-inventory record |
| Proposed activity | Reconnaissance, vulnerability scanning, exploitation, credential use, lateral movement, data access, deployment of agent, reporting-only |
| Requested autonomy level | L1, L2, L3, L4, or platform-specific level |
| Urgency | Routine, time-sensitive, incident-response, customer-directed emergency, blocked pending clarification |

## Authorization Basis

Document the evidence that gives the platform permission to act on the proposed change.

| Field | Example / guidance |
|-------|--------------------|
| RoE coverage | Existing clause, signed amendment, or note that the RoE does not cover the proposed target |
| Customer approval | Ticket, email, signed amendment, chat transcript, or named customer representative |
| Asset-owner approval | Required when different from the engagement sponsor or when production/shared infrastructure is affected |
| Authority Delegation Matrix mapping | Role IDs allowed to approve this type of change |
| Dual-control requirement | Whether two independent approvals are required for high-risk actions |
| Hard deny / exclusion check | Whether the target matches a hard deny list, exclusion, restricted business unit, or protected environment |
| Time-window validity | Whether approval applies to the current testing window and timezone |
| Standing authorization limits | Whether a wildcard, pre-approved relationship rule, or recurring-test authorization covers the change |

## Approval Attestation

| Field | Example / guidance |
|-------|--------------------|
| Approver role | Role ID from the Authority Delegation Matrix |
| Approver identity reference | Name, team, group, or identity-provider subject recorded according to the organization's audit policy |
| Approval timestamp | UTC timestamp for each approval |
| Approval artifact | Ticket, signed amendment, audit-log ID, workflow approval, or customer communication reference |
| Independence check | Whether dual-control approvers are independent when required |
| Signature / immutable log reference | Cryptographic signature, append-only audit entry, or evidence package reference |
| Pending-decision safe state | Actions paused, queued tasks blocked, temporary autonomy cap, and timeout behavior while approval is pending |

## Risk Review

Use the risk review to decide whether to approve, constrain, defer, reject, or downgrade autonomy before acting.

| Risk area | Review question | Notes / decision |
|-----------|-----------------|------------------|
| Scope certainty | Is ownership and authorization clear enough to test without further customer confirmation? |  |
| Customer impact | Could the change affect production reliability, availability, billing, or business operations? |  |
| Shared infrastructure | Could activity affect other customers, tenants, accounts, projects, or business units? |  |
| Sensitive data | Could the change expose credentials, regulated data, customer data, or privileged administrative interfaces? |  |
| Third-party infrastructure | Does the target belong to a hosting provider, SaaS vendor, CDN, identity provider, or other third party not covered by the RoE? |  |
| Irreversible action | Could the proposed action modify data, configuration, identity, persistence, payment, or safety-critical state? |  |
| Manipulation signal | Did the request originate from target-controlled content, prompt injection, configuration instructions, or social-engineering-like wording? |  |
| Evidence quality | Is the supporting evidence complete, attributable, and preserved in the audit trail? |  |
| Conflicting engagements | Does another active engagement impose a stricter rule for the same target? |  |
| Autonomy suitability | Should the platform remain at the requested autonomy level, downgrade, or pause until review completes? |  |

## Decision

| Field | Example / guidance |
|-------|--------------------|
| Decision outcome | Approved, approved with constraints, rejected, deferred pending customer confirmation, removed from scope, superseded |
| Decision rationale | Concise explanation of why the outcome is safe and authorized |
| Effective scope | Exact target identifiers, wildcards, CIDRs, cloud resource IDs, accounts, tenants, URLs, or identity boundaries approved |
| Explicit exclusions | Hosts, subdomains, paths, accounts, tenants, operations, data types, or time windows that remain out of scope |
| Maximum autonomy level | Highest autonomy level allowed for this decision until the next review |
| Required human checkpoints | Approval before exploitation, credential use, data access, lateral movement, persistence simulation, or reporting |
| Required safety controls | Rate limit, time window, kill-switch watcher, monitoring threshold, customer notification, or manual-only operation |
| Evidence preservation | Logs, traces, screenshots, DNS answers, approval artifacts, hashes, custody records, or audit-log IDs to preserve |
| Expiration / renewal | Date, cycle end, approval timeout, or event that invalidates this decision |
| Notification recipients | Customer contact, operator, engagement lead, incident commander, or auditor to notify |

## Operational Constraints

Record constraints in enough detail that operators and automated agents cannot silently interpret the decision more broadly than intended.

| Constraint | Example / guidance |
|------------|--------------------|
| Allowed actions | Passive discovery only, authenticated scan, limited exploit verification, report-only, customer-approved validation |
| Prohibited actions | Destructive testing, persistence, lateral movement, credential replay, bulk extraction, production write operations |
| Tool profile | Scanner profile, browser agent profile, exploit module allowlist, connector approval profile |
| Rate / intensity limits | Requests per second, concurrency, payload size, scan depth, host count, retry limit |
| Time limits | Testing window, maintenance window, pause condition, maximum duration |
| Monitoring requirements | Customer monitor, operator watch, alert threshold, rollback readiness, kill-switch owner |
| Autonomy cap | L1/L2/L3/L4 cap and condition for re-escalation |
| Revalidation requirement | DNS/IP validation, asset-owner confirmation, cloud inventory check, RoE refresh, approval renewal |
| Enforcement delta | Scope policy diff, rule bundle ID, before/after target list, rollback reference, or change-set ID |

## Example YAML Shape

The following illustrative YAML fragment shows one way to encode a scope change decision record. It is not a required format.

```yaml
record_id: "scope-change-2026-05-001"
engagement_id: "eng-customer-a-2026-q2"
apts_version: "0.1.0"
status: "approved_with_constraints"
request:
  change_type: "add_target"
  proposed_target: "api-staging.customer.example"
  source: "customer_ticket"
  trigger_evidence:
    - evidence_id: "ev-redirect-trace-001"
      type: "request_response_trace"
    - evidence_id: "ev-customer-ticket-7741"
      type: "customer_approval_ticket"
authorization:
  roe_reference: "roe-customer-a-2026-q2#scope"
  authority_delegation_matrix: "adm-2026-05"
  approvers:
    - role_id: "customer_scope_owner"
      identity_ref: "idp:user/customer-scope-owner"
      approval_id: "ticket-7741"
      approved_at: "2026-05-11T21:14:00Z"
    - role_id: "engagement_lead"
      identity_ref: "idp:user/engagement-lead"
      approval_id: "approval-118"
      approved_at: "2026-05-11T21:20:00Z"
  approval_attestation:
    independence_check: "dual_control_not_required_for_staging_l2"
    immutable_log_ref: "audit-log-58321"
    pending_decision_safe_state: "affected_actions_paused_until_approval"
  hard_deny_checked: true
  time_window: "2026-05-12T02:00:00Z/2026-05-12T05:00:00Z"
risk_review:
  scope_certainty: "confirmed_by_customer_scope_owner"
  customer_impact: "staging_environment_rate_limited"
  shared_infrastructure: "no_shared_tenant_detected"
  manipulation_signal: "none_detected"
decision:
  outcome: "approved_with_constraints"
  effective_scope:
    - "https://api-staging.customer.example/v1/*"
  explicit_exclusions:
    - "https://api-staging.customer.example/admin/*"
    - "production data stores"
  maximum_autonomy_level: "L2"
  allowed_actions:
    - "authenticated_vulnerability_scan"
    - "manual_exploit_verification_after_operator_review"
  prohibited_actions:
    - "credential_reuse_outside_staging"
    - "destructive_payloads"
    - "persistence_simulation"
  enforcement_delta:
    scope_policy_change_set: "scope-policy-diff-441"
    before_scope_ref: "scope-bundle-2026-q2-r3"
    after_scope_ref: "scope-bundle-2026-q2-r4"
    rollback_ref: "scope-bundle-2026-q2-r3"
  expiration: "2026-05-12T05:00:00Z"
post_decision:
  scope_engine_updated: true
  active_agents_reloaded: true
  operators_notified: true
  evidence_package_refs:
    - "manifest-2026-q2#scope-change-2026-05-001"
```

## Post-Decision Checklist

Before testing continues under the updated scope, verify:

- [ ] the decision outcome is recorded with an authorized approver or rejection reason
- [ ] the scope engine, RoE reference, or active target list reflects the exact approved target boundaries
- [ ] explicit exclusions and hard deny entries remain enforced
- [ ] active agents, queued tasks, and cached target lists are reloaded or paused as appropriate
- [ ] autonomy caps and human checkpoints are applied to affected workflows
- [ ] required customer/operator notifications have been sent
- [ ] evidence supporting the decision is preserved in the audit trail or evidence package
- [ ] the decision has an expiration, renewal condition, or supersession path

## Reviewer Questions

- Can an independent reviewer reconstruct why the target was approved, constrained, rejected, or removed?
- Does the record distinguish customer-approved scope from tool-inferred or target-suggested scope?
- Are exact target identifiers and explicit exclusions precise enough for automated enforcement?
- Does the decision preserve hard deny list protections and the most restrictive rule for overlapping engagements?
- Are autonomy caps and human checkpoints conservative enough for the reviewed risk?
- Is the supporting evidence linked to immutable audit logs or an evidence package manifest?
- Does the expiration or renewal rule prevent stale approvals from authorizing future testing cycles?

## Related Requirements and Appendices

- APTS-SE-006: Pre-Action Scope Validation
- APTS-SE-009: Hard Deny Lists and Critical Asset Protection
- APTS-SE-012: DNS Rebinding Attack Prevention
- APTS-SE-015: Scope Enforcement Audit and Compliance Verification
- APTS-SE-016: Scope Refresh and Revalidation Cycle
- APTS-SE-017: Engagement Boundary Definition for Recurring Tests
- APTS-SE-019: Rate Limiting, Adaptive Backoff, and Production Impact Controls
- APTS-SE-020: Deployment-Triggered Testing Governance
- APTS-SE-021: Scope Conflict Resolution for Overlapping Engagements
- APTS-HO-004: Authority Delegation Matrix
- APTS-HO-005: Escalation Decision Audit Trail
- APTS-AL-025: Autonomy Level Authorization, Transition, and Reauthorization
- APTS-MR-010: Scope Expansion Social Engineering Prevention
- APTS-MR-012: Immutable Scope Enforcement Architecture
- [Authority Delegation Matrix Template](Authority_Delegation_Matrix_Template.md)
- [Autonomy Downgrade Matrix Template](Autonomy_Downgrade_Matrix_Template.md)
- [Evidence Package Manifest](Evidence_Package_Manifest.md)
- [Rules of Engagement Template](Rules_of_Engagement_Template.md)
