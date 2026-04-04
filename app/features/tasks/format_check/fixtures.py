"""
Fixtures for Task 1: format-check
Each fixture has a document_text and ground_truth issues list.
Ground truth is the canonical set of format violations the grader checks against.
"""

FIXTURES = [
    {
        "id": "fc-001",
        "difficulty": "easy",
        "document_type": "Non-Disclosure Agreement",
        "jurisdiction": "India",
        "document_text": """NON-DISCLOSURE AGREEMENT

This Non-Disclosure Agreement ("Agreement") is entered into as of January 15, 2024 between Acme Technologies Private Limited, a company incorporated under the Companies Act 2013, having its registered office at 45 MG Road, Bangalore 560001 ("Disclosing Party") and Sharma Consulting Services, having its principal place of business at 12 Nehru Street, Chennai 600001 ("Receiving Party").

1. DEFINITION OF CONFIDENTIAL INFORMATION
For purposes of this Agreement, "Confidential Information" means any data or information that is proprietary to the Disclosing Party and not generally known to the public.

2. OBLIGATIONS OF RECEIVING PARTY
The Receiving Party agrees to: (a) hold the Confidential Information in strict confidence; (b) not to disclose the Confidential Information to any third parties; (c) not to use the Confidential Information for any purpose except as expressly permitted.

3. TERM
This Agreement shall remain in effect for a period of two (2) years from the date of execution.

4. GOVERNING LAW
This Agreement shall be governed by and construed in accordance with the laws of India.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.

Acme Technologies Private Limited
By: ___________________
Name: Rajesh Kumar
Title: Chief Executive Officer

Sharma Consulting Services
By: ___________________
Name: Priya Sharma
Title: Managing Director""",
        "ground_truth": {
            "issues": [
                {
                    "type": "page_numbers",
                    "description": "Document has no page numbers",
                    "severity": "high",
                },
                {
                    "type": "text_alignment",
                    "description": "Body text is not fully justified",
                    "severity": "medium",
                },
                {
                    "type": "line_spacing",
                    "description": "Document does not specify 1.5x or double line spacing",
                    "severity": "low",
                },
            ],
            "compliant": ["headings", "margins", "font"],
            "issue_count": 3,
            "hints": {
                "page_numbers": "Document has no page numbers anywhere — footer is blank on all pages",
                "text_alignment": "Body paragraphs are left-aligned, not fully justified",
                "line_spacing": "No line spacing is specified; standard legal requires 1.5x or double spacing",
            },
        },
    },
    {
        "id": "fc-002",
        "difficulty": "easy",
        "document_type": "Service Agreement",
        "jurisdiction": "India",
        "document_text": """SERVICE AGREEMENT

Dated: March 1, 2024

BETWEEN:
GlobalTech Solutions Ltd. (hereinafter "Service Provider")
AND
StartupHub India Pvt. Ltd. (hereinafter "Client")

ARTICLE I - SERVICES
The Service Provider shall provide software development services as mutually agreed upon.

ARTICLE II - PAYMENT
The Client shall pay the Service Provider a monthly retainer of INR 2,00,000 (Rupees Two Lakhs only).

ARTICLE III - CONFIDENTIALITY
Both parties agree to maintain strict confidentiality of all proprietary information.

article iv - TERMINATION
Either party may terminate this agreement with 30 days written notice.

ARTICLE V - DISPUTE RESOLUTION
Any disputes shall be resolved through arbitration in Mumbai.

Page 1""",
        "ground_truth": {
            "issues": [
                {
                    "type": "headings",
                    "description": "Article IV heading uses lowercase 'article iv' — inconsistent with all-caps ARTICLE format used elsewhere",
                    "severity": "high",
                },
                {
                    "type": "text_alignment",
                    "description": "Body text is not fully justified",
                    "severity": "medium",
                },
                {
                    "type": "font",
                    "description": "Font type and size not specified in document",
                    "severity": "medium",
                },
            ],
            "compliant": ["margins", "page_numbers"],
            "issue_count": 3,
            "hints": {
                "headings": "Article IV heading reads 'article iv - TERMINATION' in lowercase — all other articles use all-caps ARTICLE format",
                "text_alignment": "Body paragraphs are not fully justified — left-aligned only",
                "font": "No font specification present; standard legal requires Times New Roman 12pt or Arial 11pt",
            },
        },
    },
    {
        "id": "fc-003",
        "difficulty": "easy",
        "document_type": "Employment Contract",
        "jurisdiction": "India",
        "document_text": """EMPLOYMENT CONTRACT

THIS EMPLOYMENT CONTRACT is made on the 1st day of April 2024.

PARTIES:
Employer: Nexus Digital Private Limited, registered at 78 Park Street, Kolkata 700016
Employee: Mr. Amit Verma, residing at 234 Lake Gardens, Kolkata 700045

POSITION: Senior Software Engineer

COMPENSATION:
Base Salary: INR 18,00,000 per annum
Performance Bonus: Up to 20% of base salary

WORKING HOURS:
Standard working hours are 9:00 AM to 6:00 PM, Monday through Friday.

LEAVE ENTITLEMENTS:
Annual Leave: 21 days per year
Sick Leave: 12 days per year
Casual Leave: 8 days per year

PROBATION: Six (6) months from date of joining.

TERMINATION:
Either party may terminate employment with two (2) months written notice.

For and on behalf of Nexus Digital Private Limited:

_______________________
Authorized Signatory

Employee Acceptance:

_______________________
Mr. Amit Verma""",
        "ground_truth": {
            "issues": [
                {
                    "type": "page_numbers",
                    "description": "Document has no page numbers",
                    "severity": "high",
                },
                {
                    "type": "text_alignment",
                    "description": "Body text is not fully justified",
                    "severity": "medium",
                },
            ],
            "compliant": ["headings", "font", "margins", "line_spacing"],
            "issue_count": 2,
            "hints": {
                "page_numbers": "No page numbers present anywhere in the document",
                "text_alignment": "Body text is left-aligned throughout, not justified",
            },
        },
    },
    {
        "id": "fc-004",
        "difficulty": "easy",
        "document_type": "Lease Agreement",
        "jurisdiction": "India",
        "document_text": """LEASE AGREEMENT

THIS LEASE AGREEMENT is executed on February 10, 2024.

LESSOR: Mrs. Sunita Mehta, Flat 302, Sunrise Apartments, Pune 411001
LESSEE: Mr. Vikram Joshi, currently residing at 56 Sector 15, Noida 201301

PROPERTY: Flat No. 302, Sunrise Apartments, Wakad, Pune 411057

LEASE TERM: 11 months commencing March 1, 2024

RENT: INR 25,000 per month payable on or before the 5th of each month.

SECURITY DEPOSIT: INR 75,000 (equivalent to 3 months rent).

CONDITIONS:
1. The lessee shall not sublet the property without prior written consent of the lessor.
2. The lessee shall maintain the property in good condition.
3. The lessee shall pay all utility bills directly.
4. Pets are not permitted without prior written consent.
5. No structural modifications shall be made without consent.

TERMINATION:
One month written notice required from either party.

Signed in the presence of witnesses:
Witness 1: _______________
Witness 2: _______________

Lessor: _______________     Lessee: _______________""",
        "ground_truth": {
            "issues": [
                {
                    "type": "page_numbers",
                    "description": "Document has no page numbers",
                    "severity": "high",
                },
                {
                    "type": "text_alignment",
                    "description": "Body text is not fully justified",
                    "severity": "medium",
                },
                {
                    "type": "headings",
                    "description": "CONDITIONS section uses numbered list instead of formal article headings",
                    "severity": "low",
                },
                {
                    "type": "font",
                    "description": "Font type and size not specified",
                    "severity": "medium",
                },
            ],
            "compliant": ["margins"],
            "issue_count": 4,
            "hints": {
                "page_numbers": "No page numbers present in the document",
                "text_alignment": "Body text is not fully justified — left-aligned",
                "headings": "CONDITIONS section uses numbered list (1. 2. 3.) instead of formal ARTICLE-style headings",
                "font": "Font type and size not specified anywhere in the document",
            },
        },
    },
    {
        "id": "fc-005",
        "difficulty": "easy",
        "document_type": "Vendor Agreement",
        "jurisdiction": "India",
        "document_text": """VENDOR AGREEMENT

                              VENDOR AGREEMENT

This Vendor Agreement is entered into as of 15th January 2024 between:

Purchaser: Horizon Retail Chain Ltd., 99 Commercial Street, Hyderabad 500001
Vendor: Sunrise Textiles & Garments, Plot 45, MIDC Industrial Area, Nagpur 440018

1. SCOPE OF SUPPLY
The Vendor shall supply cotton garments as per specifications in Schedule A.

2. PRICING
All prices are fixed for the contract period and are inclusive of GST.

3.DELIVERY
                    Delivery shall be made within 30 days of purchase order.

4. QUALITY STANDARDS
All goods must conform to BIS standards.

5. PAYMENT TERMS
Payment within 45 days of receipt of invoice and satisfactory goods.

6. INDEMNIFICATION
The Vendor shall indemnify the Purchaser against any claims arising from defective goods.

Page 1 of 1""",
        "ground_truth": {
            "issues": [
                {
                    "type": "text_alignment",
                    "description": "Document title is center-aligned; body text alignment is inconsistent across sections",
                    "severity": "high",
                },
                {
                    "type": "headings",
                    "description": "Duplicate title at top of document; Clause 3 heading missing space: '3.DELIVERY' should be '3. DELIVERY'",
                    "severity": "medium",
                },
                {
                    "type": "font",
                    "description": "Font type and size not specified",
                    "severity": "medium",
                },
            ],
            "compliant": ["page_numbers", "margins"],
            "issue_count": 3,
            "hints": {
                "text_alignment": "Title is center-aligned; body text alignment is inconsistent across sections — not uniformly justified",
                "headings": "Title appears twice at top of document; Clause 3 reads '3.DELIVERY' with missing space after period",
                "font": "No font specification present in the document",
            },
        },
    },
]