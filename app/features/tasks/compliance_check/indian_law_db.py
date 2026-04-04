"""
Indian Law Reference Database
Used by the compliance grader to verify agent citations.
"""

INDIAN_LAWS = {
    "Indian Contract Act": {
        "year": 1872,
        "aliases": ["ICA", "Contract Act 1872", "Indian Contract Act 1872"],
        "key_sections": {
            "10": "All agreements are contracts if made by free consent of competent parties, for lawful consideration and object",
            "11": "Capacity to contract — every person is competent except minors, unsound mind, or disqualified by law",
            "13": "Free consent — parties must agree on the same thing in the same sense",
            "14": "Free consent is vitiated by coercion, undue influence, fraud, misrepresentation, or mistake",
            "23": "Lawful consideration and object — not opposed to public policy",
            "25": "Agreement without consideration is void (with exceptions)",
            "27": "Agreement in restraint of trade is void",
            "28": "Agreement in restraint of legal proceedings is void",
            "74": "Compensation for breach — reasonable compensation, not penalty clauses",
        },
        "common_violations": [
            "Unreasonable penalty clauses (violates S.74)",
            "Restraint of trade clauses (violates S.27)",
            "Restraint on legal proceedings (violates S.28)",
            "Agreements without consideration (violates S.25)",
            "Missing essential elements: offer, acceptance, consideration",
        ],
    },
    "Information Technology Act": {
        "year": 2000,
        "aliases": ["IT Act", "IT Act 2000", "ITA 2000"],
        "key_sections": {
            "10A": "Validity of contracts formed through electronic means",
            "43A": "Compensation for failure to protect sensitive personal data",
            "65B": "Admissibility of electronic records",
            "66": "Computer related offences",
            "72A": "Punishment for disclosure of information in breach of lawful contract",
        },
        "common_violations": [
            "Electronic contracts not recognizing S.10A validity",
            "No data protection provisions for sensitive personal data",
        ],
    },
    "Consumer Protection Act": {
        "year": 2019,
        "aliases": ["CPA", "Consumer Protection Act 2019", "COPRA 2019"],
        "key_sections": {
            "2(9)": "Definition of consumer",
            "2(47)": "Unfair trade practices",
            "2(48)": "Unfair contract — terms excessively one-sided against consumer",
            "49": "Jurisdiction of State Consumer Disputes Redressal Commission",
        },
        "common_violations": [
            "Unfair one-sided contract terms (S.2(48))",
            "No consumer grievance redressal mechanism",
            "Misleading terms about product/service",
            "Mandatory arbitration clauses preventing consumer forum access",
        ],
    },
    "Digital Personal Data Protection Act": {
        "year": 2023,
        "aliases": ["DPDP", "DPDP Act", "DPDPA 2023", "Data Protection Act"],
        "key_sections": {
            "4": "Lawful processing of personal data — requires consent or legitimate use",
            "5": "Notice requirements before collecting personal data",
            "6": "Consent — must be free, specific, informed, unconditional, unambiguous",
            "8": "General obligations of data fiduciary",
            "9": "Processing of personal data of children",
            "16": "Rights of data principal",
            "17": "Right to erasure",
        },
        "common_violations": [
            "Collecting personal data without explicit consent clause",
            "No data retention/deletion policy",
            "Broad data sharing without consent",
            "No mention of data principal rights",
            "Missing data breach notification obligation",
        ],
    },
    "Arbitration and Conciliation Act": {
        "year": 1996,
        "aliases": ["ACA", "Arbitration Act", "Arbitration Act 1996", "ACA 1996"],
        "key_sections": {
            "7": "Arbitration agreement must be in writing",
            "8": "Power of judicial authority to refer to arbitration",
            "11": "Appointment of arbitrators",
            "20": "Place of arbitration — parties free to agree on seat",
            "28": "Rules applicable to substance of dispute",
            "34": "Application for setting aside arbitral award",
        },
        "common_violations": [
            "Arbitration clause not in writing (violates S.7)",
            "Unclear seat of arbitration",
            "One-sided arbitrator appointment",
            "No governing law specified for arbitration",
        ],
    },
}

# Map common agent citation variants to canonical law names
LAW_ALIASES = {}
for law_name, details in INDIAN_LAWS.items():
    for alias in details.get("aliases", []):
        LAW_ALIASES[alias.lower()] = law_name
    LAW_ALIASES[law_name.lower()] = law_name


def resolve_law(citation: str) -> str | None:
    """Resolve a law citation string to canonical law name."""
    c = citation.lower().strip()
    for alias, canonical in LAW_ALIASES.items():
        if alias in c:
            return canonical
    return None


def is_valid_section(law_name: str, section: str) -> bool:
    """Check if a section number is valid for a given law."""
    if law_name not in INDIAN_LAWS:
        return False
    return section in INDIAN_LAWS[law_name]["key_sections"]
