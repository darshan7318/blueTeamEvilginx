# Threat model and research notes

## Scope and assumptions

BlueTeamEvilginx addresses AiTM phishing and adjacent account/session compromise. Evilginx is one implementation of a general reverse-proxy/session-interception pattern; detections must target behaviors and outcomes, not a product fingerprint. We assume attackers can rotate domains, certificates, hosting, IPs, user agents, and lure content. We assume identity events may be delayed or incomplete and that a valid stolen session may look normal in isolation.

## Attack lifecycle and defensive observables

1. **Lure and delivery** — email, QR, chat, search/social links, compromised legitimate services, redirects, or trusted-site abuse. Signals: URL reputation and age, sender/authentication anomalies, user-reported messages, click telemetry, redirect chain, and tenant-wide campaign clustering.
2. **Lookalike access path** — attacker-controlled domain or compromised infrastructure presents a relayed login. Signals: domain/certificate/hosting relationships, DNS and proxy logs, browser navigation, newly observed destinations, identity-provider portal protection events. Infrastructure indicators are short-lived and corroborative, never sufficient alone.
3. **Authentication relay** — username/password and non-phishing-resistant MFA can be relayed live. Signals: IdP authentication details and risk detections, unusual client context, device compliance and session binding. Do not ingest the credentials or MFA material.
4. **Session/token replay** — a completed session can be replayed outside the original client. Signals: anomalous token/issuer events, non-interactive sign-ins after interactive auth, same session across changed IP/ASN/device context, unbound session, unfamiliar client, resource access inconsistent with history. VPNs, mobile networks, proxies, and travel create false positives.
5. **Post-authentication abuse** — mailbox rules/forwarding, OAuth consent, MFA registration, password reset, role changes, data access, or internal phishing. Signals: identity audit events and workload-specific activity correlated to the suspected account and time window.
6. **Persistence and evasion** — attackers may retain alternate factors, app grants, refresh/session artifacts, or use trusted infrastructure. Response needs a full identity/session review, not just password reset or domain block.

## Threat classes and confidence limits

- **Known**: reverse-proxy AiTM, credential/MFA relay, session-cookie/token theft/replay, phishing URL rotation, mailbox abuse/BEC, post-authentication persistence, and infrastructure churn.
- **Likely variants**: QR-based delivery, adversary-in-the-middle through compromised legitimate sites, multi-stage redirects, OAuth/device-code consent abuse adjacent to AiTM, MFA fatigue/social engineering, malicious browser extensions or endpoint theft, residential proxy use, and attacker-controlled or compromised cloud hosting.
- **Unknown/unknowable exhaustively**: new identity flows, provider-specific token behavior, novel lures, compromised vendors, unobserved endpoints, and evasion using legitimate shared infrastructure. Treat this as an evolving detection engineering problem; publish coverage gaps and measure telemetry completeness.

## Mapping

Primary mappings: MITRE ATT&CK T1557 (Adversary-in-the-Middle), T1539 (Steal Web Session Cookie), and T1550.004 (Use Alternate Authentication Material: Web Session Cookie). Adjacent investigation includes phishing, account discovery, inbox manipulation, cloud account compromise, and data exfiltration; map detailed behavior to ATT&CK only when evidence supports it.

## Defensive priorities

1. Prefer phishing-resistant authentication (FIDO2/WebAuthn/passkeys or platform credentials configured with origin binding) for privileged and high-impact users.
2. Use device compliance and provider token protection/session binding where supported; validate platform/app coverage before assuming protection.
3. Enforce risk-based access, reauthentication for sensitive operations, least privilege, and short exposure windows where operationally appropriate.
4. Centralize interactive and non-interactive sign-ins, identity risk, audit events, endpoint configuration, DNS/proxy, and mail telemetry; retain time synchronization and stable event IDs.
5. Revoke sessions and investigate factors, app grants, inbox rules, roles, and downstream access after confirmed compromise. A password reset alone may not eradicate persistence.
6. Train users to report suspicious links and provide a trusted reporting channel; use authorized, non-credential-collecting simulations only.

## Sources (primary/authoritative)

- MITRE ATT&CK, [T1557 Adversary-in-the-Middle](https://attack.mitre.org/techniques/T1557/) and [DET0296 detection strategy](https://attack.mitre.org/detectionstrategies/DET0296/).
- MITRE ATT&CK, [T1539 Steal Web Session Cookie](https://attack.mitre.org/techniques/T1539/) and [T1550.004 Web Session Cookie](https://attack.mitre.org/techniques/T1550/004/).
- CISA, [Implementing Phishing-Resistant MFA](https://www.cisa.gov/resources-tools/resources/implementing-phishing-resistant-mfa).
- Microsoft Security, [Token tactics: prevent, detect, and respond to cloud token theft](https://www.microsoft.com/en-us/security/blog/2022/11/16/token-tactics-how-to-prevent-detect-and-respond-to-cloud-token-theft/).
- Microsoft Learn, [Protecting tokens in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/devices/protecting-tokens-microsoft-entra-id), [Token Protection](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-token-protection), and [Identity Protection risk detections](https://learn.microsoft.com/en-us/entra/id-protection/concept-identity-protection-risks).
- Canadian Centre for Cyber Security, [Defending against AiTM with phishing-resistant MFA](https://www.cyber.gc.ca/en/guidance/defending-against-adversary-middle-threats-phishing-resistant-multi-factor-authentication-itsm30031).

Research snapshot: 2026-11-22. Vendor fields, feature coverage, and threat infrastructure change; verify current provider documentation during adapter implementation.
