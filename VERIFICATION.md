# Export verification record

Prepared on **9 October 2026**. Verification environment: **Python 3.12.14; PyYAML 6.0.3**.

| Check | Result |
| --- | --- |
| Source selection | 928 source files selected by exact Git blob identity from source snapshot `6fcd42d057317a6b815fd6513316e0213416a440`; reviewer-facing navigation is adapted separately. |
| D01/D02 archive integrity | 44 delivery files, seven supplementary files and 26 original fixtures matched their original manifests. Raw record counts: 470 D01; 50 D02. |
| D03 archive integrity | All 837 manifest entries and 29 frozen inputs matched. Eight final cases, 32 raw responses, seven proposals, one abstention, four simulated reconciliations and the separate tamper result were checked. |
| Design integrity | Ten proposed schemas, six agent contracts, six layers, fourteen sourced invariants and 33 observed reason codes passed the existing check. |
| Phase A software tests | 13/13 passed. |
| Phase B offline software tests | 34/34 passed, with mocked network transport. No model API calls. |
| Isolated D01 replay | All summary fields matched after excluding run timestamps and interpreter metadata; the 47-row case-summary CSV matched byte-for-byte. |
| Isolated D02 replay | All summary fields matched after excluding run timestamps and interpreter metadata. Replayed under Python 3.12.14; original D02 used Python 3.13.5. |
| Distribution content | No manuscript DOCX/PDF, source-delivery ZIPs, private Git history, `.env` file or Word lock file is included. |
| Credential/privacy screening | No real credential or private-key pattern was detected in the selected files. Three long credential-assignment matches were the literal `offline-test-placeholder` in archived transport tests. No email addresses were found in the artifact files. Saved response-header names were reviewed; they comprise dates, content type, rate-limit fields and request IDs. |

The archive files were not overwritten by the preparation replays; new replay outputs were produced outside the distribution. Earlier Phase B failures remain included. These preparation checks are performed as part of packaging and **do not constitute independent external reproduction, a new model experiment, or evidence of production security**.

The root manifest and public-artifact verifier cover the final file inventory. Markdown links were checked against the distribution. The credential scan is a bounded pattern/content review of this new export, not a guarantee against every possible disclosure and not a claim that the private repository's full history was scanned.
