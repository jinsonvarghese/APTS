# Incident Response Drill Record Template

This appendix is informative and does not create or modify APTS requirements.

## Purpose

Use this template as a starting point for documenting a tabletop exercise, simulation, or live drill that tests incident response procedures for an autonomous penetration testing platform. It supports existing incident response, kill switch, containment, auditability, and autonomy-adjustment requirements by giving teams a practical record of what was exercised, what evidence was captured, and which follow-up actions remain open.

The template is intentionally lightweight. Teams may implement it as a ticket form, governance record, exercise worksheet, or signed post-drill report, provided the record is retained with the platform's audit and governance evidence.

## When to Use This Template

Consider using a drill record when any of the following occur:

- a scheduled tabletop exercise tests incident response procedures
- a live simulation tests kill switch, pause, rollback, or notification paths
- a platform update changes incident response, containment, alerting, or autonomy behavior
- a customer, reviewer, or internal governance team requests evidence that incident response procedures were exercised
- an incident or near miss identifies a response path that should be rehearsed before the next engagement

## Drill Metadata

| Field | Example / guidance |
|-------|--------------------|
| Drill ID | `ir-drill-2026-q2-sev2-scope-violation` |
| Platform / environment | Production service, staging environment, customer tenant, or internal deployment |
| Drill type | tabletop / simulation / live technical exercise / replay of prior incident |
| Scenario title | Short description of the tested incident scenario |
| Scenario severity | SEV-1 / SEV-2 / SEV-3 / SEV-4 or local severity model |
| Exercise date and time | Timestamp with timezone |
| Facilitator | Name, role, and contact method |
| Participating roles | Operators, incident commander, customer liaison, legal/compliance, platform owner, reviewer |
| Applicable Rules of Engagement | RoE document ID and version, if engagement-specific controls are exercised |
| Authority Delegation Matrix reference | Matrix ID/version and relevant role rows |
| Autonomy Downgrade Matrix reference | Matrix ID/version and applicable downgrade trigger rows |
| Evidence package or audit reference | Link or identifier for retained drill evidence |

## Scenario Definition

| Field | Guidance |
|-------|----------|
| Trigger condition | What starts the incident, such as scope uncertainty, impact threshold breach, provider compromise, cross-tenant exposure, or target instability |
| Inject source | Monitoring alert, operator report, target response, customer notification, third-party provider signal, or automated safety control |
| Initial platform state | Current autonomy level, active phase, target set, rate limits, and pending approvals |
| Expected safe state | Pause, kill switch activation, autonomy downgrade, customer hold, containment, or controlled continuation |
| Out-of-scope exclusions | Systems, customers, or data that must not be touched during the drill |
| Success criteria | Observable outcomes that determine whether the drill passed |

## Requirements and Controls Exercised

Map the drill to the existing APTS requirements and appendices it exercises. This mapping helps reviewers see whether the exercise covered detection, escalation, containment, recovery, auditability, and reporting rather than only one response step.

| Area | Requirement / appendix | Exercised? | Evidence reference |
|------|------------------------|------------|--------------------|
| Kill switch and containment | APTS-SC-009, APTS-SC-018 | yes / no / partial | Log, screenshot, state dump, or ticket ID |
| External watchdog and notification | APTS-SC-017, APTS-HO-015, APTS-HO-017 | yes / no / partial | Notification transcript or alert ID |
| State preservation | APTS-HO-008 | yes / no / partial | State dump ID or storage reference |
| Incident response during autonomy | APTS-AL-018, APTS-AL-026 | yes / no / partial | Autonomy decision or investigation record |
| Audit trail and evidence chain | APTS-AR-001 through APTS-AR-012, APTS-RP-001 | yes / no / partial | Audit export, hash manifest, or evidence package |
| Incident report | APTS-RP-011 | yes / no / partial | Draft or completed report reference |
| Cross-domain workflow | [Incident Response Integration](Incident_Response_Integration.md) | yes / no / partial | Workflow step checklist |
| Autonomy adjustment | [Autonomy Downgrade Matrix Template](Autonomy_Downgrade_Matrix_Template.md) | yes / no / partial | Downgrade row, trigger ID, or reauthorization evidence |
| Shift continuity, if applicable | [Shift Handoff Template](Shift_Handoff_Template.md) | yes / no / partial | Handoff record or incoming-operator acceptance |

## Timeline and Observations

Record timestamps in a consistent timezone. Include both expected and actual timing so the team can compare response behavior against documented SLAs.

| Time | Expected action | Actual action observed | Owner | Evidence reference | Pass / gap |
|------|-----------------|------------------------|-------|--------------------|------------|
| `T+00:00` | Inject received and classified |  |  |  |  |
| `T+00:05` | New autonomous actions paused or kill switch Phase 1 triggered |  |  |  |  |
| `T+01:00` | Operators and customer contacts notified according to severity |  |  |  |  |
| `T+05:00` | State preserved and containment verified |  |  |  |  |
| `T+30:00` | Root-cause and autonomy-adjustment decision started |  |  |  |  |
| Drill close | Report, lessons learned, and follow-up owners recorded |  |  |  |  |

## Evidence Captured

| Evidence item | Typical applicability | Captured? | Hash / custody reference | Notes |
|---------------|-----------------------|-----------|--------------------------|-------|
| Alert or inject record | recommended | yes / no |  |  |
| Operator decision log | recommended | yes / no |  |  |
| Kill switch, pause, or containment log | scenario-dependent | yes / no / not applicable |  |  |
| State dump or platform snapshot | scenario-dependent | yes / no / not applicable |  |  |
| Notification transcript | severity-dependent | yes / no / not applicable |  |  |
| Autonomy downgrade or reauthorization record | scenario-dependent | yes / no / not applicable |  |  |
| Draft incident report | recommended for reporting drills | yes / no / not applicable |  |  |
| Follow-up issue or corrective action ticket | recommended when gaps are found | yes / no / not applicable |  |  |

## Decision and Authority Review

| Decision point | Expected authority | Actual approver / actor | Decision | Evidence reference | Notes |
|----------------|--------------------|-------------------------|----------|--------------------|-------|
| Incident severity classification | Incident commander or delegated role |  | accepted / changed / escalated |  |  |
| Pause or kill switch activation | Role from Authority Delegation Matrix |  | activated / not activated / simulated |  |  |
| Customer notification | Customer liaison or incident commander |  | sent / withheld / simulated |  |  |
| Autonomy downgrade | Role from Autonomy Downgrade Matrix |  | downgraded / held / no change |  |  |
| Resume or reauthorization | Authorized approver after evidence review |  | approved / rejected / deferred |  |  |

## Gaps, Corrective Actions, and Retest Plan

| Gap ID | Observation | Impact | Owner | Due date | Corrective action | Retest evidence |
|--------|-------------|--------|-------|----------|-------------------|-----------------|
| `gap-001` | Example: operator notification reached email but not SMS | Detection / escalation delay |  |  | Update paging configuration and retest notification path |  |

For each gap, record whether it blocks production use, requires an autonomy cap, or only requires a scheduled follow-up. If a gap affects scope, containment, notification, or evidence integrity, consider recording the temporary safe state until the fix is verified.

## Drill Closeout Checklist

This checklist is illustrative and may be adapted to the drill scope.

- [ ] Scenario, severity, participants, and authority references were recorded
- [ ] Requirements and appendices exercised by the drill were mapped
- [ ] Expected and actual response timeline was captured
- [ ] Kill switch, pause, containment, or rollback behavior was verified or explicitly marked not applicable
- [ ] Operator, customer, watchdog, and stakeholder notification behavior was verified or explicitly marked not applicable
- [ ] Evidence items were hashed, stored, and referenced where applicable
- [ ] Autonomy downgrade, reauthorization, or resume decisions were documented
- [ ] Gaps were assigned to owners with due dates and retest evidence expectations
- [ ] Drill record was retained with the platform governance or audit evidence

## Reviewer Questions

- Does the drill exercise more than notification, such as containment, state preservation, autonomy adjustment, and evidence handling?
- Are timing expectations compared with actual observed response times?
- Are decision-makers and authority references traceable to the Authority Delegation Matrix or incident response plan?
- Are evidence references sufficient for a reviewer to verify what happened without rerunning the drill?
- Were any gaps converted into tracked corrective actions with owners and retest criteria?
- If testing resumed after the drill, is the reauthorization basis documented?

## Related Requirements and Appendices

- APTS-SC-009: Kill Switch
- APTS-SC-017: External Watchdog and Operator Notification
- APTS-SC-018: Incident Containment and Recovery
- APTS-HO-008: Immediate Kill Switch with State Dump
- APTS-HO-015: Real-Time Activity Monitoring and Multi-Channel Notification
- APTS-HO-017: Stakeholder Notification and Engagement Closure
- APTS-AL-018: Incident Response During Autonomous Testing
- APTS-AL-026: Incident Investigation and Autonomy Level Adjustment
- APTS-AR-001 through APTS-AR-012: audit trail, timestamping, and chain-of-custody controls
- APTS-RP-001: Evidence-Based Finding Validation
- APTS-RP-011: Executive Summary and Risk Overview
- [Incident Response Integration](Incident_Response_Integration.md)
- [Authority Delegation Matrix Template](Authority_Delegation_Matrix_Template.md)
- [Autonomy Downgrade Matrix Template](Autonomy_Downgrade_Matrix_Template.md)
- [Evidence Package Manifest](Evidence_Package_Manifest.md)
