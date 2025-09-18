"""Sample case data used when MongoDB is unavailable."""
from __future__ import annotations

SAMPLE_CASES = [
    {
        "_id": "68c93ace241e4ea8580068af",
        "court": "SUPREME COURT OF INDIA",
        "FileID": 2368453,
        "case_title": "In Re: Contagion of Covid-19 Virus in Prisons vs Director General (Prisons)",
        "citation": "2023 0 CJ(SC) 242",
        "judgment_date": "2023-03-24",
        "bench": ["M.R. Shah", "C.T. Ravikumar"],
        "parties": {
            "appellant": "In Re: Contagion of Covid-19 Virus in Prisons",
            "respondent": "Director General (Prisons)",
        },
        "case_type": "I A",
        "case_number": "179931 of 2022 IN SUO MOTO WRIT PETITION (C) NO 01 of 2020",
        "procedural_history": [
            {
                "court": "District Munsif Court",
                "decision": "Dismissed the Election Petition.",
            },
            {
                "court": "Additional District Judge",
                "decision": "Allowed the appeal and declared the election void.",
            },
            {
                "court": "High Court of Kerala",
                "decision": "Dismissed the revision and review petitions, confirming the order of the Additional District Judge.",
            },
            {
                "court": "Supreme Court of India",
                "decision": "Allowed the appeals, setting aside the lower court orders and dismissing the Election Petition.",
            },
        ],
        "issues": [
            "Whether the non-disclosure of a past conviction for a minor, regulatory offence under the Kerala Police Act in a nomination form constitutes a 'corrupt practice' of 'undue influence' under the Kerala Panchayat Raj Act, 1994?",
            "Does such a non-disclosure amount to furnishing 'fake' details under Section 102(1)(ca) of the Kerala Panchayat Raj Act, thereby rendering the election void?",
            "Whether the legislative intent behind mandatory disclosure of criminal antecedents is limited to serious or heinous offences, or if it extends to minor offences arising from political protests?",
        ],
        "reasoning": {
            "rejection_of_high_court_methodology": "The Supreme Court rejected the mechanical application of the disclosure rules by the High Court and District Court. It held that courts must look beyond the literal text to the legislative purpose, which is to prevent the criminalization of politics by targeting serious, not minor, offences.",
            "application_of_precedent": "The Court distinguished the case from Krishnamoorthy vs. Sivakumar, noting that the Kerala Act had a specific provision (Sec 102(1)(ca)) making the circuitous interpretation of 'undue influence' unnecessary. It aligned with the principles of Association for Democratic Reforms and PUCL, emphasizing that the voter's right to know is focused on antecedents involving serious crimes, corruption, or moral turpitude.",
            "duty_of_the_court": "The Court underscored its duty to adopt a purposive interpretation of election laws to avoid absurd outcomes. It held that voiding an election for non-disclosure of a minor offence related to a political protest would defeat the true object of the disclosure mandate, which is to ensure purity in public life by flagging candidates with serious criminal backgrounds.",
            "evidence_based_determination": "The Court's decision was based on a careful examination of the nature of the offence for which the appellant was convicted. It was determined to be a minor, regulatory offence under the Kerala Police Act for disobeying a police officer's direction during a political dharna, not a substantive offence under the Indian Penal Code or other laws related to corruption or heinous crimes.",
        },
        "outcome": {
            "decision": "The appeals were allowed, and the election of the appellant was upheld.",
            "directions": [
                "Set aside the impugned orders of the High Court of Kerala and the Additional District Judge.",
                "Dismiss the Election Petition filed by the respondent.",
            ],
        },
        "search_metadata": {
            "summary": "The Supreme Court allowed the appeal of an elected Panchayat councilor whose election was declared void by lower courts for failing to disclose a past conviction. The conviction was for a minor offence under the Kerala Police Act, resulting from a political protest. The Court held that while the non-disclosure technically qualified as furnishing 'fake' information under Section 102(1)(ca) of the Kerala Panchayat Raj Act, 1994, the legislative intent behind such disclosure laws is to decriminalize politics by informing voters about serious or heinous criminal antecedents, not minor regulatory offences. Drawing a distinction between substantive crimes and minor offences arising from political activity, the Court adopted a purposive interpretation to conclude that voiding the election on this ground would be contrary to the object of the law. The lower court orders were set aside, and the election was upheld.",
            "headnote": "The Supreme Court held that the mandatory disclosure of criminal antecedents by candidates in election nomination forms must be interpreted purposively. The core objective is to inform voters about involvement in serious or heinous offences relating to corruption or moral turpitude to prevent the criminalization of politics. A distinction must be drawn between such substantive offences and minor, regulatory offences arising from political activities like protests. The non-disclosure of a conviction for a minor, regulatory offence (e.g., under a Police Act for disobeying an order during a dharna) does not vitiate an election under Section 102(1)(ca) of the Kerala Panchayat Raj Act, 1994, as it falls outside the intended scope of the disclosure mandate.",
            "keywords": [
                "Election Law",
                "Disclosure of Criminal Antecedents",
                "Kerala Panchayat Raj Act 1994",
                "Corrupt Practice",
                "Fake Information",
                "Section 102(1)(ca)",
                "Section 52(1A)",
                "Purposive Interpretation",
                "Voter's Right to Know",
                "Decriminalization of Politics",
                "Regulatory Offence",
                "Substantive Offence",
                "Political Protest",
                "Nomination Form",
            ],
            "legal_concepts": [
                "Purity of Elections",
                "Voter's Right to Information",
                "Purposive Statutory Interpretation",
                "Corrupt Practice in Election Law",
                "Doctrine of Ultra Vires",
                "Undue Influence",
            ],
            "acts_referred": [
                "Kerala Panchayat Raj Act, 1994",
                "Kerala Panchayat Raj (Conduct of Election) Rules, 1995",
                "Kerala Police Act, 1961",
                "Representation of the People Act, 1951",
                "Indian Penal Code, 1860",
                "Tamil Nadu Panchayats Act, 1994",
                "Constitution of India",
            ],
        },
    }
]
