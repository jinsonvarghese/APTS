# Authority Delegation Matrix Template

Informative Appendix (non-normative)

This appendix provides an illustrative template for documenting who can approve which autonomous penetration testing actions, at which autonomy levels, and under which escalation conditions. It supports the Authority Delegation Matrix required by APTS-HO-004 and the decision audit trail required by APTS-HO-005. It does not prescribe one mandatory format for every organization.

## Purpose

APTS requires organizations operating autonomous penetration testing systems to maintain a documented Authority Delegation Matrix (ADM). Reviewers and customers need a practical artifact that shows whether approval authority is current, role-based, scoped to action risk, and auditable.

The ADM should be treated as the authority source of record. Engagement-specific artifacts such as Rules of Engagement may reference the ADM by `matrix_id`, `version`, role identifier, or approval ticket, but they should not silently redefine who is allowed to approve high-risk actions.

This appendix shows:

- a compact role-and-authority matrix
- suggested metadata for review, renewal, and revocation
- a YAML starter template
- reviewer questions for customer or audit inspection
- cross-references to related APTS requirements

## Primary Use Cases

Use an Authority Delegation Matrix to document:

- which roles may approve actions at each autonomy level
- which actions require escalation or dual control
- who may activate pause, redirect, or kill-switch procedures
- which approver is primary, secondary, or emergency authority for each shift or engagement
- when an authority assignment was approved, last reviewed, suspended, or revoked

## Design Principles

An Authority Delegation Matrix should:

- bind authority to roles rather than individual convenience exceptions
- separate routine approval authority from emergency intervention authority
- identify dual-control requirements for high-risk actions
- make escalation paths explicit when an operator lacks authority
- avoid storing unnecessary personal data in broadly shared artifacts
- be protected as sensitive operational information
- be easy to reconcile against approval records, shift handoffs, and immutable decision logs

## Recommended Template Sections

### 1. Matrix metadata

Use stable identifiers and review dates so customers can tell whether the matrix is current.

Recommended fields:

- `matrix_id`
- `organization`
- `engagement_id` or `program_scope`
- `version`
- `effective_from`
- `expires_on`
- `owner_role`
- `last_reviewed_at`
- `approved_by`
- `classification`

### 2. Role catalog

Define each role once before assigning authority.

Recommended fields:

- `role_id`
- `role_name`
- `minimum_qualification`
- `training_required`
- `mfa_required`
- `employment_or_contract_status`
- `backup_role`

### 3. Authority matrix

Capture approval authority by action category, autonomy level, and risk threshold.

Recommended fields:

- `action_category`
- `autonomy_levels`
- `approval_authority_roles`
- `maximum_risk_or_impact`
- `dual_control_required`
- `secondary_approver_role`
- `escalation_role`
- `default_safe_action_if_unavailable`
- `evidence_required_before_approval`

Suggested action categories include:

- exploitation attempt
- lateral movement
- data access or exfiltration
- persistence or callback deployment
- scope expansion or redirect
- irreversible action
- pause or resume
- kill-switch activation
- customer notification
- legal or compliance escalation

### 4. Emergency authority

Document emergency-only authority separately so it cannot be confused with routine approval authority.

Recommended fields:

- `emergency_condition`
- `authorized_roles`
- `activation_channel`
- `authentication_requirement`
- `notification_targets`
- `post_activation_review_required`

### 5. Review and revocation history

Track changes to authority assignments over time.

Recommended fields:

- `change_id`
- `changed_at`
- `changed_by`
- `change_type`
- `affected_role_or_authority`
- `reason`
- `approval_reference`

## Example YAML Template

```yaml
matrix_id: adm-2026-001
organization: Example Security Operations
engagement_id: eng-2026-001
version: 1.0
effective_from: 2026-04-01T00:00:00Z
expires_on: 2026-07-01T00:00:00Z
owner_role: Head of Offensive Security
last_reviewed_at: 2026-04-01T12:00:00Z
approved_by: CISO
classification: confidential-operational

role_catalog:
  - role_id: ho-role-operator
    role_name: Autonomous Testing Operator
    minimum_qualification:
      - internal APTS operator training
      - engagement-specific Rules of Engagement briefing
    training_required: annual plus engagement-specific
    mfa_required: true
    employment_or_contract_status: approved staff or approved contractor
    backup_role: ho-role-senior-operator

  - role_id: ho-role-senior-operator
    role_name: Senior Autonomous Testing Operator
    minimum_qualification:
      - senior offensive security review qualification
      - prior autonomous testing approval experience
    training_required: annual plus high-risk action approval training
    mfa_required: true
    employment_or_contract_status: approved staff
    backup_role: ho-role-manager-on-call

  - role_id: ho-role-manager-on-call
    role_name: Security Manager On-Call
    minimum_qualification:
      - incident commander training
      - customer escalation authority
    training_required: annual incident and escalation training
    mfa_required: true
    employment_or_contract_status: approved staff
    backup_role: ho-role-ciso

  - role_id: ho-role-ciso
    role_name: CISO Emergency Authority
    minimum_qualification:
      - executive risk acceptance authority
    training_required: annual emergency authority review
    mfa_required: true
    employment_or_contract_status: executive officer
    backup_role: ho-role-board-approved-delegate

authority_matrix:
  - action_category: exploitation_attempt
    autonomy_levels: [L1, L2]
    approval_authority_roles:
      - ho-role-senior-operator
    maximum_risk_or_impact: CVSS < 9.0 and no critical-service impact expected
    dual_control_required: false
    secondary_approver_role: null
    escalation_role: ho-role-manager-on-call
    default_safe_action_if_unavailable: deny_action_and_skip_target
    evidence_required_before_approval:
      - target is in approved scope
      - impact classification completed
      - rollback or stop condition documented

  - action_category: critical_exploitation_attempt
    autonomy_levels: [L1, L2, L3]
    approval_authority_roles:
      - ho-role-senior-operator
      - ho-role-manager-on-call
    maximum_risk_or_impact: CVSS >= 9.0 or critical-service impact possible
    dual_control_required: true
    secondary_approver_role: ho-role-manager-on-call
    escalation_role: ho-role-ciso
    default_safe_action_if_unavailable: pause_and_escalate
    evidence_required_before_approval:
      - target is in approved scope
      - customer authorization permits high-risk exploitation
      - explicit stop condition documented
      - customer notification path confirmed

  - action_category: scope_redirect
    autonomy_levels: [L2, L3, L4]
    approval_authority_roles:
      - ho-role-manager-on-call
    maximum_risk_or_impact: approved customer-owned assets only
    dual_control_required: false
    secondary_approver_role: null
    escalation_role: ho-role-ciso
    default_safe_action_if_unavailable: do_not_expand_scope
    evidence_required_before_approval:
      - updated Rules of Engagement reference
      - scope validation result
      - customer approval reference

  - action_category: kill_switch_activation
    autonomy_levels: [L1, L2, L3, L4]
    approval_authority_roles:
      - ho-role-current-primary-operator
      - ho-role-assigned-secondary-operator
      - ho-role-manager-on-call
      - ho-role-ciso
    maximum_risk_or_impact: any suspected safety, scope, legal, or customer-impact condition
    dual_control_required: false
    secondary_approver_role: null
    escalation_role: ho-role-ciso
    shift_or_handoff_reference: shift-roster-2026-04-01-day
    default_safe_action_if_unavailable: any_currently_assigned_authorized_operator_may_activate
    evidence_required_before_approval:
      - no pre-approval required for emergency kill activation
      - post-activation review record required

emergency_authority:
  - emergency_condition: suspected_out_of_scope_activity
    authorized_roles:
      - ho-role-current-primary-operator
      - ho-role-assigned-secondary-operator
      - ho-role-manager-on-call
      - ho-role-ciso
    activation_channel: dashboard or out-of-band emergency channel
    authentication_requirement: mfa_or_emergency_break_glass_code
    notification_targets:
      - engagement manager
      - customer contact
      - incident response lead
    post_activation_review_required: true

review_and_revocation_history:
  - change_id: adm-change-001
    changed_at: 2026-04-01T12:00:00Z
    changed_by: Head of Offensive Security
    change_type: initial_approval
    affected_role_or_authority: all
    reason: new engagement authority baseline
    approval_reference: approval-ticket-2026-041
```

## Reviewer Questions

When inspecting an Authority Delegation Matrix, ask:

- does the matrix identify current ownership, version, effective date, and expiration date
- are approval powers tied to roles with documented qualifications rather than informal individual preferences
- do CVSS >= 9.0 actions require dual control, and do scope expansion or irreversible actions route through the required approval or escalation path
- is emergency authority documented separately from routine approval authority
- can approval records and shift handoffs be reconciled back to the authority matrix version that was effective at the time
- are unavailable approvers handled with default-safe behavior rather than implicit auto-approval
- is the matrix protected as sensitive operational information and reviewed on a defined cadence

## Related APTS Requirements

This template can help operators and reviewers implement or verify:

- APTS-HO-001 Mandatory Pre-Approval Gates for Autonomy Levels L1 and L2
- APTS-HO-003 Decision Timeout and Default-Safe Behavior
- APTS-HO-004 Authority Delegation Matrix
- APTS-HO-005 Delegation Chain-of-Custody and Decision Audit Trail
- APTS-HO-009 Multi-Operator Kill Switch Authority and Handoff
- APTS-HO-010 Mandatory Human Decision Points Before Irreversible Actions
- APTS-HO-019 24/7 Operational Continuity and Shift Handoff
- APTS-SC-006 Threshold Escalation Workflow
- APTS-SC-009 Kill Switch

## Notes

This appendix is intentionally lightweight. Organizations may implement the matrix in identity governance systems, approval workflows, ticketing platforms, or signed operating procedures as long as authority remains explicit, current, access-controlled, and auditable.
