"""
Fixtures for Task 3: compliance-check
Each fixture has a contract with known legal compliance violations under Indian law.
"""

FIXTURES = [
    {
        "id": "cc-001",
        "difficulty": "hard",
        "document_type": "Software License Agreement",
        "jurisdiction": "India",
        "document_text": """SOFTWARE LICENSE AGREEMENT

This Software License Agreement is between DataVault Technologies Ltd. and the Licensee.

1. LICENSE GRANT
DataVault grants Licensee a non-exclusive, non-transferable license to use the Software.

2. PAYMENT AND PENALTY
Licensee shall pay INR 50,000 per month. In case of delayed payment, a penalty of 200% of the monthly fee shall be charged as liquidated damages for every week of delay.

3. DATA COLLECTION
By using the Software, Licensee consents to DataVault collecting all data generated through software usage, which may be shared with third parties for commercial purposes without further notice.

4. DISPUTE RESOLUTION
All disputes shall be resolved through arbitration. The arbitrator shall be appointed solely by DataVault Technologies Ltd. The seat of arbitration shall be determined by DataVault at the time of dispute.

5. RESTRAINT
Licensee agrees not to use any competing software products for a period of 5 years from the date of termination of this agreement.

6. LIMITATION OF LEGAL PROCEEDINGS
Licensee waives all rights to approach any court of law or consumer forum in India for any dispute arising from this agreement.""",
        "ground_truth": {
            "violations": [
                {
                    "clause": "Clause 2 — 200% penalty per week",
                    "law": "Indian Contract Act",
                    "section": "74",
                    "issue": "Penalty clause is grossly disproportionate; S.74 only allows reasonable compensation",
                    "suggestion": "Replace with reasonable pre-estimated damages (e.g., 2% per month on overdue amount)",
                },
                {
                    "clause": "Clause 3 — Data sharing without further notice",
                    "law": "Digital Personal Data Protection Act",
                    "section": "6",
                    "issue": "Blanket consent for third-party data sharing violates DPDP Act S.6 (consent must be specific and informed)",
                    "suggestion": "Specify exact categories of data shared, with whom, and for what purpose. Require separate explicit consent.",
                },
                {
                    "clause": "Clause 4 — One-sided arbitrator appointment",
                    "law": "Arbitration and Conciliation Act",
                    "section": "11",
                    "issue": "One-sided arbitrator appointment by one party only is against principles of natural justice and may render award challengeable",
                    "suggestion": "Provide for neutral arbitrator appointment or appointment by mutual agreement or designated institution (e.g., DIAC)",
                },
                {
                    "clause": "Clause 4 — Unilateral seat determination",
                    "law": "Arbitration and Conciliation Act",
                    "section": "20",
                    "issue": "Seat of arbitration to be determined unilaterally by one party at time of dispute is contrary to S.20",
                    "suggestion": "Fix the seat of arbitration in the agreement itself (e.g., 'Seat: Mumbai')",
                },
                {
                    "clause": "Clause 5 — 5-year restraint of trade",
                    "law": "Indian Contract Act",
                    "section": "27",
                    "issue": "Post-termination restraint from using competing software is void under S.27 of the Indian Contract Act",
                    "suggestion": "Remove the restraint of trade clause entirely; non-solicitation/non-disclosure may be permissible",
                },
                {
                    "clause": "Clause 6 — Waiver of court/consumer forum access",
                    "law": "Indian Contract Act",
                    "section": "28",
                    "issue": "Agreement restraining legal proceedings is void under S.28; consumer forum waiver also violates CPA 2019",
                    "suggestion": "Remove the waiver clause; parties retain right to approach courts",
                },
            ],
            "compliant_clauses": [
                "License grant (Clause 1) — properly grants limited, non-exclusive license",
                "Payment terms (Clause 2) — base payment structure is compliant",
            ],
            "hints": {
                "laws_to_check": "Indian Contract Act 1872 (S.74 penalty, S.27 restraint of trade, S.28 waiver of legal proceedings), DPDP Act 2023 (S.6 consent), Arbitration and Conciliation Act 1996 (S.11 arbitrator appointment, S.20 seat)",
                "clause_2": "200% penalty per week is grossly disproportionate — ICA S.74 only allows reasonable compensation not penalties",
                "clause_3": "Blanket third-party data sharing without specific consent violates DPDP Act S.6",
                "clause_4": "Two violations: one-sided arbitrator appointment (ACA S.11) and unspecified seat (ACA S.20)",
                "clause_5": "Post-termination restraint from competing software = void restraint of trade under ICA S.27",
                "clause_6": "Waiving right to approach courts is void under ICA S.28",
            },
        },
    },
    {
        "id": "cc-002",
        "difficulty": "hard",
        "document_type": "E-Commerce Terms of Service",
        "jurisdiction": "India",
        "document_text": """TERMS OF SERVICE — SHOPFAST INDIA

By using ShopFast India's platform, you agree to these Terms.

1. ACCOUNT REGISTRATION
Users must be 18 years of age. By registering, you confirm you are above 18.

2. DATA USAGE
We collect your name, address, phone number, purchase history, browsing behavior, device data, and location. This data may be used for marketing, analytics, and may be sold to advertising partners. You cannot opt out of data collection while using the platform.

3. RETURNS AND REFUNDS
All sales are final. No returns or refunds will be provided for any reason whatsoever.

4. LIABILITY
ShopFast's total liability shall not exceed INR 100 (Rupees One Hundred only) regardless of the nature or quantum of claim.

5. DISPUTE RESOLUTION
Any disputes must be filed within 7 days of the transaction. After 7 days, the consumer's right to claim is extinguished. Disputes will be resolved by arbitration only. No complaints may be filed with any consumer commission.

6. GOVERNING LAW
These Terms are governed by the laws of Delaware, USA.""",
        "ground_truth": {
            "violations": [
                {
                    "clause": "Clause 2 — Selling data to advertising partners; no opt-out",
                    "law": "Digital Personal Data Protection Act",
                    "section": "6",
                    "issue": "Selling personal data to third parties without specific informed consent violates DPDP Act. No opt-out is coercive consent.",
                    "suggestion": "Obtain separate, specific consent for each category of data use. Provide clear opt-out mechanism.",
                },
                {
                    "clause": "Clause 3 — No returns or refunds",
                    "law": "Consumer Protection Act",
                    "section": "2(47)",
                    "issue": "Blanket no-refund policy is an unfair trade practice under CPA 2019 S.2(47) for B2C transactions",
                    "suggestion": "Comply with consumer protection norms — allow returns for defective goods within statutory period",
                },
                {
                    "clause": "Clause 4 — INR 100 liability cap",
                    "law": "Consumer Protection Act",
                    "section": "2(48)",
                    "issue": "Grossly disproportionate liability cap (INR 100) is an unfair contract term under CPA 2019 S.2(48)",
                    "suggestion": "Set a reasonable liability cap (e.g., value of the transaction)",
                },
                {
                    "clause": "Clause 5 — 7-day limitation and no consumer commission",
                    "law": "Consumer Protection Act",
                    "section": "49",
                    "issue": "Artificial 7-day limitation period and waiver of consumer forum access violates CPA 2019 and is void",
                    "suggestion": "Remove artificial limitation; consumers retain right to approach consumer commissions",
                },
                {
                    "clause": "Clause 6 — Delaware, USA governing law",
                    "law": "Indian Contract Act",
                    "section": "23",
                    "issue": "For Indian consumers, Indian law (particularly CPA 2019) cannot be contracted out of regardless of choice-of-law clause",
                    "suggestion": "Apply Indian law for Indian consumers; foreign law choice is unenforceable against CPA rights",
                },
            ],
            "compliant_clauses": [
                "Age verification requirement (Clause 1) — compliant with requirement to contract only with competent parties",
            ],
            "hints": {
                "laws_to_check": "DPDP Act 2023 (S.6 data selling), Consumer Protection Act 2019 (S.2(47) unfair trade, S.2(48) unfair contract, S.49 consumer commission), Indian Contract Act 1872 (S.23 foreign governing law)",
                "clause_2": "Selling data to advertising partners with no opt-out = DPDP Act S.6 violation",
                "clause_3": "Blanket no-refund policy for B2C = CPA 2019 S.2(47) unfair trade practice",
                "clause_4": "INR 100 liability cap regardless of claim value = CPA 2019 S.2(48) unfair contract term",
                "clause_5": "7-day limitation period + barring consumer commission = CPA 2019 S.49 violation",
                "clause_6": "Delaware governing law cannot override CPA rights for Indian consumers = ICA S.23",
            },
        },
    },
    {
        "id": "cc-003",
        "difficulty": "hard",
        "document_type": "Employment Agreement",
        "jurisdiction": "India",
        "document_text": """EMPLOYMENT AGREEMENT

Employer: FutureTech Innovations Pvt. Ltd.
Employee: Candidate to be named upon joining

1. EMPLOYMENT AT WILL
This is an at-will employment arrangement. The employer may terminate the employee at any time, for any reason, without notice and without payment of any compensation.

2. NON-COMPETE
Employee agrees not to work for any competitor in India, USA, UK, Singapore, or any other country globally for a period of 3 years post-termination.

3. INTELLECTUAL PROPERTY
All intellectual property created by the employee, whether during or outside of working hours, including personal projects, shall vest with the Employer.

4. SALARY DEDUCTIONS
The Employer reserves the right to deduct any amount from the employee's salary for losses caused to the company, as determined solely by the Employer.

5. MANDATORY ARBITRATION
All employment disputes including claims under labor laws shall be resolved through mandatory arbitration. Employee waives all rights to approach labor courts or industrial tribunals.

6. ELECTRONIC MONITORING
Employee consents to monitoring of all electronic communications including personal emails and messages on personal devices during working hours.""",
        "ground_truth": {
            "violations": [
                {
                    "clause": "Clause 1 — At-will termination without notice or compensation",
                    "law": "Indian Contract Act",
                    "section": "10",
                    "issue": "At-will employment without notice or compensation is contrary to Indian labor law norms and violates principles of free consent",
                    "suggestion": "Provide reasonable notice period (typically 1–3 months) and comply with applicable labor laws including ID Act",
                },
                {
                    "clause": "Clause 2 — Global 3-year non-compete",
                    "law": "Indian Contract Act",
                    "section": "27",
                    "issue": "Post-employment non-compete covering all competitors globally for 3 years is void under S.27 ICA",
                    "suggestion": "Remove post-employment non-compete; non-solicitation of clients/employees may be permissible with reasonable scope",
                },
                {
                    "clause": "Clause 3 — IP in personal projects outside work hours",
                    "law": "Indian Contract Act",
                    "section": "23",
                    "issue": "Claiming IP over personal projects unrelated to employment is opposed to public policy under S.23",
                    "suggestion": "Limit IP assignment to work created in scope of employment and using employer resources",
                },
                {
                    "clause": "Clause 4 — Unilateral salary deductions",
                    "law": "Indian Contract Act",
                    "section": "14",
                    "issue": "Employer-determined deductions without employee's free consent violates free consent principles under S.14",
                    "suggestion": "Deductions only with employee's written consent or as per statutory deductions; dispute mechanism required",
                },
                {
                    "clause": "Clause 5 — Waiver of labor court rights",
                    "law": "Arbitration and Conciliation Act",
                    "section": "7",
                    "issue": "Statutory rights under labor legislation cannot be waived; labor courts and tribunals have exclusive jurisdiction over labor disputes",
                    "suggestion": "Remove mandatory arbitration for labor disputes; arbitration may supplement but cannot replace statutory forums",
                },
                {
                    "clause": "Clause 6 — Monitoring personal emails on personal devices",
                    "law": "Digital Personal Data Protection Act",
                    "section": "6",
                    "issue": "Blanket consent to monitor personal emails and personal devices violates DPDP Act — consent is not free when employment depends on it",
                    "suggestion": "Limit monitoring to company-issued devices and company accounts; personal device monitoring requires genuinely voluntary consent",
                },
            ],
            "compliant_clauses": [
                "Intellectual property clause partially — work created during employment hours with company resources is legitimately employer's IP",
            ],
            "hints": {
                "laws_to_check": "Indian Contract Act 1872 (S.10 at-will termination, S.27 non-compete, S.23 personal IP, S.14 salary deductions), ACA 1996 (S.7 labor arbitration), DPDP Act 2023 (S.6 personal device monitoring)",
                "clause_1": "At-will with zero notice/compensation violates ICA S.10 free consent principles and Indian labor law norms",
                "clause_2": "Global 3-year post-employment non-compete = void under ICA S.27",
                "clause_3": "Claiming IP over personal projects outside work hours = opposed to public policy under ICA S.23",
                "clause_4": "Unilateral employer deductions = no free consent under ICA S.14",
                "clause_5": "Waiving labor court rights through arbitration clause = ACA S.7 — statutory labor forums cannot be contracted away",
                "clause_6": "Monitoring personal emails on personal devices = DPDP Act S.6 — consent coerced by employment relationship",
            },
        },
    },
    {
        "id": "cc-004",
        "difficulty": "hard",
        "document_type": "Loan Agreement",
        "jurisdiction": "India",
        "document_text": """LOAN AGREEMENT

Lender: QuickCash Digital Lending App
Borrower: As per app registration

1. LOAN AMOUNT AND INTEREST
Principal: As approved by algorithm. Interest: 5% per day compounding daily.

2. DATA ACCESS
Borrower grants QuickCash irrevocable access to all contacts, SMS, photos, location, and social media accounts on borrower's device for the duration of the loan and 2 years after repayment.

3. RECOVERY
In case of default, QuickCash may contact borrower's family members, employers, and all phone contacts to recover the debt. QuickCash may also publish borrower's name and photograph on social media.

4. CONSENT
By downloading the app, Borrower is deemed to have read, understood, and agreed to all terms.

5. JURISDICTION
Disputes shall be governed by the laws of the Cayman Islands.""",
        "ground_truth": {
            "violations": [
                {
                    "clause": "Clause 1 — 5% per day compounding interest",
                    "law": "Indian Contract Act",
                    "section": "23",
                    "issue": "Unconscionably high interest rate (1825% per annum) is opposed to public policy and usurious under S.23; also violates RBI fair practices code",
                    "suggestion": "Comply with RBI guidelines on fair interest rates; disclose effective APR clearly",
                },
                {
                    "clause": "Clause 2 — Access to contacts, SMS, photos, location post-repayment",
                    "law": "Digital Personal Data Protection Act",
                    "section": "4",
                    "issue": "Collecting all device data with irrevocable access for 2 years post-repayment violates DPDP Act purpose limitation and retention principles",
                    "suggestion": "Collect only data necessary for loan processing; delete on repayment; no irrevocable consent",
                },
                {
                    "clause": "Clause 3 — Contacting family/employer, social media publication",
                    "law": "Digital Personal Data Protection Act",
                    "section": "6",
                    "issue": "Publishing borrower's personal data on social media for debt recovery violates DPDP Act and constitutes harassment",
                    "suggestion": "Remove entirely; follow RBI Fair Practices Code for recovery — no harassment, no third-party contact without consent",
                },
                {
                    "clause": "Clause 4 — Deemed consent by app download",
                    "law": "Digital Personal Data Protection Act",
                    "section": "6",
                    "issue": "Deemed/implied consent by app download is NOT valid consent under DPDP Act — must be freely given, specific, informed, unambiguous",
                    "suggestion": "Implement explicit tick-box or affirmative consent for each category of data collection",
                },
                {
                    "clause": "Clause 5 — Cayman Islands governing law for Indian consumers",
                    "law": "Consumer Protection Act",
                    "section": "2(48)",
                    "issue": "Choice of foreign law cannot override Indian consumer protection rights for Indian borrowers",
                    "suggestion": "Apply Indian law; arbitration seat must be in India; consumer rights under CPA 2019 are non-derogable",
                },
            ],
            "compliant_clauses": [],
            "hints": {
                "laws_to_check": "Indian Contract Act 1872 (S.23 usurious interest), DPDP Act 2023 (S.4 data retention, S.6 deemed consent and social media publication), Consumer Protection Act 2019 (S.2(48) foreign governing law)",
                "clause_1": "5% per day = 1825% per annum — unconscionably usurious, opposed to public policy under ICA S.23",
                "clause_2": "Irrevocable device access for 2 years after repayment violates DPDP Act S.4 purpose limitation and data minimisation",
                "clause_3": "Publishing borrower photo on social media for recovery = DPDP Act S.6 + harassment",
                "clause_4": "Deemed consent by app download is not valid under DPDP Act S.6 — must be explicit and affirmative",
                "clause_5": "Cayman Islands law cannot override Indian consumer rights = CPA 2019 S.2(48)",
            },
        },
    },
    {
        "id": "cc-005",
        "difficulty": "hard",
        "document_type": "SaaS Subscription Agreement",
        "jurisdiction": "India",
        "document_text": """SAAS SUBSCRIPTION AGREEMENT

This agreement is between CloudStack India Pvt. Ltd. ("Provider") and Subscriber.

1. SERVICE DESCRIPTION
Provider will provide cloud-based project management software ("Service") as described on the website, which may change at Provider's sole discretion without notice.

2. AUTO-RENEWAL
Subscription auto-renews annually. Cancellation requires 90 days notice before renewal date. No refunds on auto-renewed subscriptions.

3. PRICE CHANGES
Provider may change subscription pricing at any time with 7-day notice. Continued use after price change constitutes acceptance.

4. DATA PORTABILITY
Upon termination, Subscriber has 24 hours to export data. After 24 hours, all subscriber data will be permanently deleted.

5. UNLIMITED LIABILITY WAIVER
Subscriber agrees that Provider's liability for any cause whatsoever shall be limited to zero.

6. GOVERNING LAW AND DISPUTES
Disputes governed by Indian law. Any legal action must be brought in courts of Provider's choice. Limitation period: 30 days from cause of action.""",
        "ground_truth": {
            "violations": [
                {
                    "clause": "Clause 1 — Service changes at sole discretion without notice",
                    "law": "Indian Contract Act",
                    "section": "10",
                    "issue": "Unilateral right to materially change service without notice undermines free consent — subscriber cannot consent to unknown future changes",
                    "suggestion": "Provide reasonable notice (30 days) for material service changes with right to cancel without penalty",
                },
                {
                    "clause": "Clause 2 — 90-day cancellation notice; no refund on auto-renewal",
                    "law": "Consumer Protection Act",
                    "section": "2(47)",
                    "issue": "90-day cancellation requirement for annual subscription with no refunds is an unfair trade practice under CPA 2019",
                    "suggestion": "Reduce to 30-day notice; provide pro-rata refund on cancellation",
                },
                {
                    "clause": "Clause 4 — 24-hour data export window",
                    "law": "Digital Personal Data Protection Act",
                    "section": "17",
                    "issue": "24-hour data portability window is insufficient; DPDP Act S.17 provides right to data portability and erasure on request",
                    "suggestion": "Provide minimum 30-day data export window; confirm deletion after export period",
                },
                {
                    "clause": "Clause 5 — Zero liability",
                    "law": "Indian Contract Act",
                    "section": "23",
                    "issue": "Complete zero-liability clause is against public policy under S.23; cannot exclude liability for gross negligence or fraud",
                    "suggestion": "Limit liability to subscription fees paid; cannot be absolute zero",
                },
                {
                    "clause": "Clause 6 — 30-day limitation period",
                    "law": "Indian Contract Act",
                    "section": "28",
                    "issue": "Contractual 30-day limitation period extinguishes rights far earlier than the Limitation Act allows — violates S.28 ICA",
                    "suggestion": "Remove artificial limitation; statutory limitation periods under Limitation Act 1963 apply",
                },
            ],
            "compliant_clauses": [
                "Governing law clause (Clause 6 partial) — specifying Indian law is appropriate",
                "Auto-renewal disclosure (Clause 2 partial) — disclosing auto-renewal is good practice, though terms are unfair",
            ],
            "hints": {
                "laws_to_check": "Indian Contract Act 1872 (S.10 unilateral changes, S.23 zero liability, S.28 artificial limitation), CPA 2019 (S.2(47) 90-day cancellation), DPDP Act 2023 (S.17 data portability)",
                "clause_1": "Unilateral service changes without notice = subscriber cannot freely consent to unknown future terms, ICA S.10",
                "clause_2": "90-day cancellation + no refunds = unfair trade practice under CPA 2019 S.2(47)",
                "clause_4": "24-hour data export window violates DPDP Act S.17 right to data portability",
                "clause_5": "Zero liability clause = against public policy under ICA S.23",
                "clause_6": "30-day contractual limitation period = void under ICA S.28 (Limitation Act 1963 governs)",
            },
        },
    },
]