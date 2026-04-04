"""
Fixtures for Task 2: content-review
Each fixture has labeled PII and known errors as ground truth.
"""

FIXTURES = [
    {
        "id": "cr-001",
        "difficulty": "medium",
        "document_type": "Service Agreement",
        "jurisdiction": "India",
        "document_text": """SERVICE AGREEMENT

This Service Agreement ("Agreement") is made on 1st Febuary 2024 between:

Service Provider: TechSphere Solutions Pvt. Ltd., 78 Koramangala 4th Block, Bangalore 560034
  Contact: Arjun Nair (arjun.nair@techsphere.in, +91-9876543210)

Client: Meridian Exports & Imports Ltd., 23 BKC, Mumbai 400051
  Contact: Deepa Krishnamurthy (deepa.k@meridianexports.com, 022-4455-6677)

1. SCOPE OF WORK
TechSphere Solutions will develop a custom ERP software for Meridian Exports.

2. TIMELINE
The project will be delivered in three phases over 9 months. The final deliverable is due by November 1, 2024. All interim deliverables will be submitted on a fortnightly basis every two weeks.

3. PAYMENT
Total project cost: INR 45,00,000. Payment shall be made in three equal installments of INR 1,50,000 each. First installment due upon signing.

4. INTELLECTUAL PROPERTY
All intellectual property created under this agreement shall vest with the Client upon full payment.

5. LIMITATION OF LIABILITY
Neither party shall be liable for indirect, incidental, or consequential damage arising from this agreement.""",
        "ground_truth": {
            "pii": {
                "names": ["Arjun Nair", "Deepa Krishnamurthy"],
                "emails": ["arjun.nair@techsphere.in", "deepa.k@meridianexports.com"],
                "phones": ["+91-9876543210", "022-4455-6677"],
                "addresses": [
                    "78 Koramangala 4th Block, Bangalore 560034",
                    "23 BKC, Mumbai 400051",
                ],
                "companies": ["TechSphere Solutions Pvt. Ltd.", "Meridian Exports & Imports Ltd."],
                "shops": [],
            },
            "errors": [
                {
                    "type": "spelling",
                    "text": "Febuary",
                    "correction": "February",
                },
                {
                    "type": "logical_inconsistency",
                    "text": "Three equal installments of INR 1,50,000 each does not equal total of INR 45,00,000",
                    "correction": "Each installment should be INR 15,00,000",
                },
                {
                    "type": "logical_inconsistency",
                    "text": "'fortnightly basis every two weeks' is redundant — fortnightly already means every two weeks",
                    "correction": "Remove 'every two weeks'",
                },
                {
                    "type": "grammar",
                    "text": "consequential damage",
                    "correction": "consequential damages (plural)",
                },
            ],
            "hints": {
                "names": "Look for: Arjun Nair (Service Provider contact), Deepa Krishnamurthy (Client contact)",
                "emails": "Look for: arjun.nair@techsphere.in and deepa.k@meridianexports.com",
                "phones": "Look for: +91-9876543210 and 022-4455-6677",
                "addresses": "Look for: 78 Koramangala 4th Block Bangalore and 23 BKC Mumbai",
                "companies": "Look for: TechSphere Solutions Pvt. Ltd. and Meridian Exports & Imports Ltd.",
                "errors": "Spelling: 'Febuary' should be 'February'. Logic: 3 x INR 1,50,000 = 4,50,000 not 45,00,000. Logic: 'fortnightly every two weeks' is redundant. Grammar: 'damage' should be 'damages'.",
            },
        },
    },
    {
        "id": "cr-002",
        "difficulty": "medium",
        "document_type": "Partnership Deed",
        "jurisdiction": "India",
        "document_text": """PARTNERSHIP DEED

This Partnership Deed is executed on 15th March 2024 between the following partners:

1. Ravi Shankar Gupta, S/o Late Ramesh Gupta, residing at 45 Civil Lines, Allahabad 211001 (ravi.gupta@guptaandco.com, 0532-2456789)
2. Meena Agarwal, D/o Suresh Agarwal, residing at 12 Hazratganj, Lucknow 226001 (meena.agarwal@outlook.com, +91-7654321098)
3. Dr. Sanjay Verma, S/o Vinod Verma, residing at 8 Model Town, Jalandhar 144001 (sanjay.verma@vermalaw.in)

BUSINESS NAME: Gupta, Agarwal & Verma Associates
BUSINESS NATURE: Legal consultancy and advisory services
REGISTERED OFFICE: 45 Civil Lines, Allahabad 211001

CAPITAL CONTRIBUTIONS:
Partner 1 (Ravi Shankar Gupta): INR 10,00,000
Partner 2 (Meena Agarwal): INR 8,00,000
Partner 3 (Dr. Sanjay Verma): INR 7,00,000
Total Capital: INR 24,00,000

PROFIT SHARING RATIO: 40:35:25

DURATION: The partnership shall commence on 1st April 2024 and shall continue until dissolvd by mutual consent.

BANK ACCOUNT: All partnership accounts shall be operated jointly by any two partners.""",
        "ground_truth": {
            "pii": {
                "names": ["Ravi Shankar Gupta", "Meena Agarwal", "Dr. Sanjay Verma", "Ramesh Gupta", "Suresh Agarwal", "Vinod Verma"],
                "emails": ["ravi.gupta@guptaandco.com", "meena.agarwal@outlook.com", "sanjay.verma@vermalaw.in"],
                "phones": ["0532-2456789", "+91-7654321098"],
                "addresses": [
                    "45 Civil Lines, Allahabad 211001",
                    "12 Hazratganj, Lucknow 226001",
                    "8 Model Town, Jalandhar 144001",
                ],
                "companies": ["Gupta, Agarwal & Verma Associates"],
                "shops": [],
            },
            "errors": [
                {
                    "type": "spelling",
                    "text": "dissolvd",
                    "correction": "dissolved",
                },
                {
                    "type": "logical_inconsistency",
                    "text": "Profit sharing ratio 40:35:25 sums to 100 but capital contributions are 10L:8L:7L = 40:32:28 ratio — inconsistent with capital shares",
                    "correction": "Profit ratio should match capital ratio or be explicitly justified",
                },
            ],
            "hints": {
                "names": "6 names total: Ravi Shankar Gupta, Meena Agarwal, Dr. Sanjay Verma, and their fathers: Ramesh Gupta, Suresh Agarwal, Vinod Verma",
                "emails": "3 emails: ravi.gupta@guptaandco.com, meena.agarwal@outlook.com, sanjay.verma@vermalaw.in",
                "phones": "2 phones: 0532-2456789 and +91-7654321098 (Dr. Verma has no phone listed)",
                "addresses": "3 addresses: Allahabad, Lucknow, Jalandhar",
                "errors": "Spelling: 'dissolvd' should be 'dissolved'. Logic: profit ratio 40:35:25 does not match capital ratio 10:8:7 (which is 40:32:28).",
            },
        },
    },
    {
        "id": "cr-003",
        "difficulty": "medium",
        "document_type": "Franchise Agreement",
        "jurisdiction": "India",
        "document_text": """FRANCHISE AGREEMENT

This Franchise Agreement ("Agreement") is entered into on 20th April 2024:

Franchisor: Chai Corner Foods Pvt. Ltd., Corporate Office: 67 Rajaji Salai, Chennai 600001
  Email: franchise@chaicorner.in | Phone: 044-2345-6789

Franchisee: Mr. Harpreet Singh Bhatia, 234 Sector 17, Chandigarh 160017
  Email: harpreet.bhatia@gmail.com | Phone: +91-9988776655

FRANCHISED OUTLET: Chai Corner — Sector 17, Chandigarh
ADDRESS: Shop No. 45, Sector 17-C Market, Chandigarh 160017

FRANCHISE FEE: INR 5,00,000 (non-refundable)
ROYALTY: 8% of monthly gross sales

TERM: 5 years from commencement date of May 1, 2024. The agreement expires on May 1, 2028.

TRAINING: Franchisor will provide 2-week training at the Chennai headquarters at the franchisee's expense.

TERRITORY: Exclusive territory covering Sectors 15 to 20 in Chandigarh.

QUALITY STANDARDS: Franchisee must adhere to all quality standards as per the operations manual dated 2019, which shall not be updated during the term of this agreement.""",
        "ground_truth": {
            "pii": {
                "names": ["Harpreet Singh Bhatia"],
                "emails": ["franchise@chaicorner.in", "harpreet.bhatia@gmail.com"],
                "phones": ["044-2345-6789", "+91-9988776655"],
                "addresses": [
                    "67 Rajaji Salai, Chennai 600001",
                    "234 Sector 17, Chandigarh 160017",
                    "Shop No. 45, Sector 17-C Market, Chandigarh 160017",
                ],
                "companies": ["Chai Corner Foods Pvt. Ltd."],
                "shops": ["Chai Corner — Sector 17, Chandigarh"],
            },
            "errors": [
                {
                    "type": "logical_inconsistency",
                    "text": "5-year term from May 1, 2024 should expire May 1, 2029, not May 1, 2028",
                    "correction": "Expiry date should be May 1, 2029",
                },
                {
                    "type": "logical_inconsistency",
                    "text": "Operations manual dated 2019 with clause that it 'shall not be updated' — unfair and likely unenforceable over 5-year term",
                    "correction": "Allow for manual updates with reasonable notice",
                },
            ],
            "hints": {
                "names": "1 individual: Harpreet Singh Bhatia (franchisee)",
                "emails": "2 emails: franchise@chaicorner.in and harpreet.bhatia@gmail.com",
                "phones": "2 phones: 044-2345-6789 and +91-9988776655",
                "addresses": "3 addresses: Chennai corporate office, Chandigarh residence, and outlet shop address",
                "shops": "1 shop: Chai Corner — Sector 17, Chandigarh",
                "errors": "Logic: 5 years from May 2024 = May 2029, not May 2028. Logic: binding a party to a 2019 manual that cannot be updated for 5 years is unreasonable.",
            },
        },
    },
    {
        "id": "cr-004",
        "difficulty": "medium",
        "document_type": "Loan Agreement",
        "jurisdiction": "India",
        "document_text": """LOAN AGREEMENT

This Loan Agreement is made on 5th June 2024 between:

Lender: Sunrise Microfinance Ltd., 12 Parliament Street, New Delhi 110001
  Contact Person: Ms. Kavya Reddy (kavya.reddy@sunrisemf.com, 011-2334-5566)

Borrower: Om Prakash Yadav, 78 Lal Bahadur Nagar, Varanasi 221001
  Aadhaar: XXXX-XXXX-4521 | Phone: +91-8765432109

LOAN DETAILS:
Principal Amount: INR 2,00,000
Interest Rate: 18% per annum (compound quarterly)
Loan Tenure: 24 months
Monthly EMI: INR 9,950 (approximatly)

REPAYMENT COMMENCEMENT: July 5, 2024

SECURITY: Gold ornaments weighing 50 grams deposited with the Lender.

LATE PAYMENT: A penality of 2% per month on the overdue amount will be charged.

PREPAYMENT: Borrower may prepay the loan after 6 months without any charges. Before 6 months, a prepayment penality of 3% shall apply.""",
        "ground_truth": {
            "pii": {
                "names": ["Kavya Reddy", "Om Prakash Yadav"],
                "emails": ["kavya.reddy@sunrisemf.com"],
                "phones": ["011-2334-5566", "+91-8765432109"],
                "addresses": [
                    "12 Parliament Street, New Delhi 110001",
                    "78 Lal Bahadur Nagar, Varanasi 221001",
                ],
                "companies": ["Sunrise Microfinance Ltd."],
                "shops": [],
            },
            "errors": [
                {
                    "type": "spelling",
                    "text": "approximatly",
                    "correction": "approximately",
                },
                {
                    "type": "spelling",
                    "text": "penality",
                    "correction": "penalty",
                },
                {
                    "type": "spelling",
                    "text": "penality (second occurrence in PREPAYMENT clause)",
                    "correction": "penalty",
                },
            ],
            "hints": {
                "names": "2 names: Kavya Reddy (lender contact) and Om Prakash Yadav (borrower)",
                "emails": "1 email: kavya.reddy@sunrisemf.com",
                "phones": "2 phones: 011-2334-5566 and +91-8765432109",
                "addresses": "2 addresses: New Delhi (lender) and Varanasi (borrower)",
                "errors": "3 spelling errors: 'approximatly', 'penality' in LATE PAYMENT clause, 'penality' again in PREPAYMENT clause — all same misspelling of 'penalty'.",
            },
        },
    },
    {
        "id": "cr-005",
        "difficulty": "medium",
        "document_type": "Distribution Agreement",
        "jurisdiction": "India",
        "document_text": """DISTRIBUTION AGREEMENT

This Distribution Agreement is executed on 10th July 2024 between:

Manufacturer: Bharat Spices & Foods Pvt. Ltd., Plot 12, Food Park, Surat 395010
  Email: export@bharatspices.com | Tel: +91-261-2345678

Distributor: Spice Route Traders, Shop No. 7, Crawford Market, Mumbai 400001
  Proprietor: Mr. Abdul Hamid Sheikh (abdulhamid.sheikh@spiceroute.in, +91-9123456789)

TERRITORY: Maharashtra and Goa

PRODUCTS: All SKUs listed in Annexure A (to be attached)

MINIMUM PURCHASE: Distributor commits to purchase a minimum of 500 units per quarter. Failure to meet minimum purchase requirements for 2 consecutive quarters will lead to immediate termination without notice.

PRICING: As per Manufacturer's current price list, subject to revision with 15 days notice.

EXCLUSIVITY: This is an exclusive distributorship for the Territory.

TERM: 2 years from August 1, 2024 to July 31, 2025.

PAYMENT TERMS: Payment within 30 days of invoice. Interest at 24% per annum on overdue amounts.""",
        "ground_truth": {
            "pii": {
                "names": ["Abdul Hamid Sheikh"],
                "emails": ["export@bharatspices.com", "abdulhamid.sheikh@spiceroute.in"],
                "phones": ["+91-261-2345678", "+91-9123456789"],
                "addresses": [
                    "Plot 12, Food Park, Surat 395010",
                    "Shop No. 7, Crawford Market, Mumbai 400001",
                ],
                "companies": ["Bharat Spices & Foods Pvt. Ltd."],
                "shops": ["Spice Route Traders"],
            },
            "errors": [
                {
                    "type": "logical_inconsistency",
                    "text": "2-year term from August 1, 2024 should end July 31, 2026, not July 31, 2025",
                    "correction": "End date should be July 31, 2026",
                },
                {
                    "type": "logical_inconsistency",
                    "text": "Immediate termination without notice for failing minimum purchase is one-sided and potentially unfair",
                    "correction": "Provide cure period (e.g., 30 days) before termination",
                },
            ],
            "hints": {
                "names": "1 individual: Abdul Hamid Sheikh (distributor proprietor)",
                "emails": "2 emails: export@bharatspices.com and abdulhamid.sheikh@spiceroute.in",
                "phones": "2 phones: +91-261-2345678 and +91-9123456789",
                "addresses": "2 addresses: Surat (manufacturer) and Mumbai Crawford Market (distributor)",
                "shops": "1 shop: Spice Route Traders",
                "errors": "Logic: 2 years from Aug 1 2024 = July 31 2026 not 2025. Logic: immediate termination with no cure period is one-sided.",
            },
        },
    },
]