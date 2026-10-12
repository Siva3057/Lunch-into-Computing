Disaster Recovery Plan: ShopSphere Ltd

1. Organisation Overview

ShopSphere is a hypothetical online retailer that operates entirely on AWS. Its storefront, payment gateway, inventory database, and order management system are hosted in a single primary region (eu-west-1). Any downtime results in immediate lost sales and undermines customer trust.

2. Identified Risks and Impact

Five risks threaten ShopSphere's operations, with a recovery target of 1 hour for service and at most 5 minutes of data loss.


| Risk | Potential impact |
| :--- | :--- |
| Regional or data Centre outage | Storefront unavailable; revenue lost every hour |
| Cyberattack (ransomware, DDoS) | Encrypted or stolen customer data, regulatory fines, reputational harm |
| System failure or faulty deployment | Corrupted databases, failed checkouts, inventory mismatches |
| Human error or insider misuse | Accidental or malicious deletion of production data |
| Third-party failure (payments, CDN) | Customers unable to complete purchases |

Recovery targets: Recovery Time Objective (RTO) of 1 hour; Recovery Point Objective (RPO) of 5 minutes for orders and payments


3. Disaster Recovery Strategy

ShopSphere recovers by replicating continuously to a second region, keeping immutable backups off-platform, and following a six-step runbook.

Tools: AWS Elastic Disaster Recovery (continuous replication to a secondary region), Amazon RDS cross-region replicas, S3 versioning with Object Lock, Bacula for scheduled off-platform backups, CloudWatch for monitoring, Terraform for rebuilding infrastructure, and Route 53 for DNS failover.

Steps:
  1.	Detect and declare: Automated alerts notify the incident commander, who confirms severity and activates the plan.
  
  2.	Contain: Isolate affected systems, revoke compromised credentials, and block malicious traffic with AWS WAF and Shield.
  
  3.	Fail over: Launch recovery instances in the secondary region, promote the database replica, and redirect traffic through health-check-based   DNS failover.
  4.	Communicate: Update the status page and inform staff, customers and, where required, regulators.

  5.	Verify integrity: Check checksums, reconcile orders against payment records, and restore from the last clean Bacula or S3 backup if corruption is found.

  6.	Fail back and review: Return to the primary region once stable, then hold a post-incident review and update the plan.
Data integrity and minimal downtime: Backups follow the 3-2-1 rule (three copies, two media types, one off-site) and are encrypted, immutable and versioned. Multi-AZ deployment, load balancing, and infrastructure as code reduce single points of failure. Failover drills run quarterly to prove the RTO and RPO are achievable.

4. Legal, Ethical and Professional Reflection

Protecting customer data must take precedence over restoring service promptly, and the plan must comply with the laws governing that data.
Legal: ShopSphere must follow applicable data protection laws, including the GDPR and Ghana's Data Protection Act, 2012, with timely breach notifications (within 72 hours under the GDPR) and adequate safeguards. Cardholder data must meet PCI DSS. Cross-region replication raises data-residency concerns, so transfers need lawful safeguards and clear cloud-provider contracts under the shared responsibility model.

Ethical: Customers entrust the company with their personal and financial information. Honest, prompt disclosure of any breaches is essential, even when it may be embarrassing. Protecting personal data should take precedence over restoring service quickly, and recovery decisions should never compromise security for speed.

Professional: The plan should align with ISO 22301 (business continuity) and ISO 27001 (information security). It needs clear role ownership, documented runbooks, staff training, least-privilege access and regular testing. Managers should avoid overpromising recovery times and treat every incident as a chance to improve.

Conclusion: By implementing continuous replication, immutable backups, regularly rehearsed procedures, and lawful, transparent data-handling practices, ShopSphere can minimise disruption, protect its customers, and recover promptly from the incidents most likely to affect its operations.


