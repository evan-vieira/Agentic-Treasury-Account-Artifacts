# Export verification record

Prepared on **9 October 2026**; retained-metadata clarification added on the same date. Original packaging verification environment: **Python 3.12.14; PyYAML 6.0.3**.

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
| Credential/privacy screening | No real credential or private-key pattern was detected in the original bounded review of selected files. Three long credential-assignment matches were the literal `offline-test-placeholder` in archived transport tests. No email addresses were found in the artifact files; Git commit metadata is a separate surface. Saved response-header names comprise dates, content type, rate-limit fields and request IDs. Organization and local-path identifiers are retained as documented below. This is not a claim that all identifying metadata has been removed. |

The archive files were not overwritten by the preparation replays; new replay outputs were produced outside the distribution. Earlier Phase B failures remain included. These preparation checks are performed as part of packaging and **do not constitute independent external reproduction, a new model experiment, or evidence of production security**.

The root manifest and public-artifact verifier cover the final file inventory. Markdown links were checked against the distribution. The credential scan is a bounded pattern/content review of this new export, not a guarantee against every possible disclosure and not a claim that the private repository's full history was scanned.

## Known identifying metadata retained in the frozen record

The distribution preserves the following metadata in the original experimental files. These identifiers are not API keys or passwords, but they identify an organization or a local execution environment. Their presence is disclosed explicitly; the archive is not an anonymized dataset.

- **Organization identifier:** the HTTP 429 error message in the [Phase B v1.0 B04 raw response](phase-b/v1.3/prior-runs/v1.0/ata-phase-b/runs/20260924T022249819508Z/B04/1-liquidity_and_cash_position-response.raw.json) includes an OpenAI organization identifier. The value is not repeated here. The response records the rate-limit failure that interrupted that development run.
- **Local execution paths:** seven saved standard-output logs contain an absolute path with a local username and the working-directory hierarchy. The files are listed below. They are historical log text, not required installation paths.
- **Git author metadata:** public commits include author and committer identity fields, including an email address. These fields are outside the file manifest; the statement about email addresses in artifact files does not apply to Git commit metadata.

| Archived version | Logs containing the local path |
| --- | --- |
| v1.0 | [run.stdout.txt](phase-b/v1.3/prior-runs/v1.0/ata-phase-b/execution-logs/run.stdout.txt) |
| v1.1 | [run.stdout.txt](phase-b/v1.3/prior-runs/v1.1/ata-phase-b/execution-logs/run.stdout.txt), [resume-verification.stdout.txt](phase-b/v1.3/prior-runs/v1.1/ata-phase-b/execution-logs/resume-verification.stdout.txt) |
| v1.2 | [run.stdout.txt](phase-b/v1.3/prior-runs/v1.2/ata-phase-b/execution-logs/run.stdout.txt), [resume-verification.stdout.txt](phase-b/v1.3/prior-runs/v1.2/ata-phase-b/execution-logs/resume-verification.stdout.txt) |
| v1.3 (D03) | [run.stdout.txt](phase-b/v1.3/ata-phase-b/execution-logs/run.stdout.txt), [resume-verification.stdout.txt](phase-b/v1.3/ata-phase-b/execution-logs/resume-verification.stdout.txt) |

The preservation decision is to **retain and disclose** these identifiers. The raw response, all seven logs, the 837-entry Phase B manifest, and the D01/D02 records remain byte-identical to the initial public artifact snapshot `83c935936ac57791c8ad5cb73b435e84d40679cd`. No metadata redaction, experimental rerun or change to reported outcomes is part of this clarification.

## Documentation correction and integrity

This update adds the public repository URLs to `CITATION.cff`, removes the unused private-paper path rule from `.gitattributes`, and documents the retained metadata above. `SOURCE_PROVENANCE.json` marks the adapted attributes file and records its new export hash. The root `MANIFEST-SHA256.json` is regenerated for the changed distribution files; the frozen experiment manifests are unchanged. Artifact and experiment version labels are preserved.

After the correction, read-only verification passed for all 935 root-manifest entries, the 44/7/26 Phase A manifest entries and 470/50 raw records, the 837 Phase B entries and final-case inventory, and the design schema/contract inventory. Git file comparison confirmed that only five root metadata/documentation files changed; all experimental files retain their original bytes.

At the earlier metadata correction, the release tag, archival DOI and reuse
license were still pending. Subsequently, `v1.0` was published at commit
`514d0fedccfc146ccb775eb2d4dda1729a60e43c` on 9 October 2026. This G3 revision
adds MIT/CC BY 4.0 component licensing as defined in [LICENSE.md](LICENSE.md).
The DOI remains pending; no ORCID has been inferred. The original packaging
test and replay results above remain historical results of that preparation.
The new G3 checks are recorded separately in [G3-VERIFICATION.md](G3-VERIFICATION.md).
