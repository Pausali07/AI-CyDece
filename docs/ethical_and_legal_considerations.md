# Ethical and Legal Considerations — AI-CyDece

## Purpose and scope
This project develops an academic honeypot + LLM analysis framework for research and learning.
It is designed for isolated lab use only.

## Legal boundaries & compliance
- Do not deploy on public networks without authorization.
- Obtain institutional approval before any live deployment.
- Be mindful of applicable laws (e.g., Computer Misuse Acts, IT Act, GDPR principles for data privacy).

## Data handling & privacy
- Enforce redaction of credentials; store only hashed or redacted versions for sharing.
- Keep raw logs in secure, access-controlled storage.
- Implement retention policy (e.g., auto-archive after 7 days).

## Risk mitigation
- Run honeypots in isolated VMs or VLAN segments.
- Monitor resource use; prevent risk of honeypot being used to launch attacks.
- Ensure outbound network is restricted to prevent malware downloads.

## Ethical usage
- Use only for defensive research; never attempt to trace or retaliate.
- Respect privacy of third parties; avoid sharing PII.

## Audit & transparency
- Store an audit log of analyses, prompts, and LLM responses (for reproducibility).
- Document prompts and model versions used.

