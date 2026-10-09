# Dataverse deposit settings — G3 revision

Use the new `Agentic-Treasury-Account-Artifacts-v1.0-G3-2026-10-09.tar.gz`
snapshot. Keep it compressed. It supersedes the earlier deposit candidate but
does not replace or move the historical GitHub `v1.0` tag. The dataset description
must identify the **new public commit and this archive's SHA-256**, supplied
alongside the archive after packaging, rather than claiming it is byte-identical
to the old tag. Experimental version labels remain unchanged.

## License field

In **Edit → Terms → License**, choose **Custom Dataset Terms** and paste the
complete contents of [DATAVERSE-TERMS.txt](DATAVERSE-TERMS.txt) into Terms of Use.
This specifies MIT for software and CC BY 4.0 for data/documentation. Do not
leave the dataset at CC0 or apply CC BY indiscriminately to the mixed archive.
Remove the earlier proposed “All rights reserved” text if it was entered.
Keep downloads public and unrestricted. Do not add extra reuse restrictions.

The custom field is a component-license statement, not a new proprietary license.
If the collection does not offer custom terms, resolve that configuration before
publishing this mixed archive. The user guide documents the custom-terms option:
https://guides.dataverse.org/en/latest/user/dataset-management.html#custom-terms-of-use-for-datasets

## Citation fields

- Author: Vieira, Evandro Camilo; affiliation: Addly.
- Title: Agentic Treasury Account: Code, Synthetic Data and D01–D03 Evaluation Artifacts — v1.0 (G3 distribution revision).
- Description: identify the new public commit and archive SHA-256, the preservation
  of D01–D03 records, and the component license scope above.
- Do not invent an ORCID or DOI. The release date in the CFF files records the
  verified public release date, 9 October 2026; it is not a claim of Dataverse publication.

After the dataset is actually published, reconcile its DOI and exact public
commit with the manuscript and project references. A DOI has not been inserted
into this distribution because none has been verified.
