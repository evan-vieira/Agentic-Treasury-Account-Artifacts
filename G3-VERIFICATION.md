# G3 — licensing, reproduction and citation

**Historical checkpoint:** G3 at public commit
`24487fc846df08bf5d882dc929a51b33698c3a11`, dated 9 October 2026. The results below
describe that snapshot. Subsequent G12 editorial changes are recorded in
[DISTRIBUTION-CHANGES.json](DISTRIBUTION-CHANGES.json). G3 was based on public release `v1.0`
at commit `514d0fedccfc146ccb775eb2d4dda1729a60e43c`.

The scope is distribution metadata. No frozen experimental file or result was
edited, and no experimental version was incremented. The historical release tag
is preserved. A fresh archive and root manifest are required for this revision.

## License and citation decisions

- MIT applies to software and schemas; CC BY 4.0 applies to data/documentation,
  with every project file enumerated in `LICENSE-MAP.json`.
- The full texts are supplied under `LICENSES/`.
- Separate software/data CFF records avoid representing these licenses as an OR
  choice for the same file. Dates reflect the verified public release date.
- ORCID and DOI are omitted because no verified identifier was supplied.
- Dataverse component terms mirror the MIT and CC BY 4.0 file scopes.

## Validation

Executed with **Python 3.12.14 / PyYAML 6.0.3**, without model API calls:

| Check | Result |
| --- | --- |
| Root inventory | 944 files; 943 covered entries plus the root manifest itself. |
| Frozen Phase A | 44/44, 7/7 and 26/26 entries; 470 D01 and 50 D02 records. |
| Frozen Phase B | 837 entries; 29 inputs; eight final cases; 32 responses; seven proposals; one abstention; four reconciliations; tamper rejection retained. |
| Design check | 10 schemas, six contracts, six layers, 14 invariants, 33 reason codes. |
| Offline tests | 13/13 Phase A and 34/34 Phase B. |
| Isolated D01/D02 replays | Summary contents matched after excluding only `started_at`, `completed_at` and `python`; the D01 case-summary CSV matched byte-for-byte. |
| Citation metadata | Both CFF files validated against the official CFF 1.2.0 JSON schema. |
| Licensing coverage | 942 project files mapped: 45 MIT and 897 CC BY 4.0; two standard license texts listed separately. |
| Evidence preservation | All 897 files under `phase-a/` and `phase-b/` remain byte-identical to the base release. |

No model experiment was rerun and these preparation replays do not establish
independent external reproduction. The complete G3 file snapshot was screened again with Gitleaks 8.24.2
and the complementary G2 patterns. The 306 Gitleaks findings were identical
to the previously verified synthetic idempotency hashes; no new credential
finding was identified. The known organization identifier and seven local-path
logs remain disclosed in `VERIFICATION.md`. Public Git authorship metadata is
outside the archive. The earlier G2 archive checksum does not identify this
new package; its SHA-256 is provided with the final download.

