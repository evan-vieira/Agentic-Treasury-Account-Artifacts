# License scope

License grants introduced with G3 on **9 October 2026** and retained in this distribution.

This research compendium applies different licenses to different files. It does
not offer a choice of MIT or CC BY for every file. [LICENSE-MAP.json](LICENSE-MAP.json)
enumerates the applicable license for every project file in this distribution.

| Material | License | Exact scope |
| --- | --- | --- |
| Research software, tests, machine-readable schemas and dependency declarations | [MIT](LICENSES/MIT.txt) | Every `*.py`, `*.schema.json` and `requirements.txt` file, plus root `.gitattributes` and `.gitignore`. This includes the preserved copies under earlier Phase B runs. |
| Synthetic data, fixtures, experiment records, prompts saved as data, reports, architecture documentation and citation/provenance metadata | [CC BY 4.0](LICENSES/CC-BY-4.0.txt) | All other project files, as enumerated in the map. Prompts embedded in Python source follow that source file's MIT license. |

The standard license texts in `LICENSES/` are reproduced as legal instruments;
they are listed separately from project-authored files in the map. Their inclusion
does not assert authorship of those texts. Third-party dependencies obtained
separately retain their own licenses. Referenced publications and external
services are not relicensed by this compendium.

MIT permits software reuse, modification and redistribution, including commercial
use, subject to its copyright and permission notices. CC BY 4.0 permits sharing
and adaptation, including commercial use, with appropriate credit, a license link
and an indication of changes. The full license texts govern; no additional
noncommercial or research-only restriction is imposed.

For the data and documentation, credit **Evandro Camilo Vieira (Addly)** and cite
the research compendium title, version and exact public commit. Add the dataset
DOI when one has actually been assigned and published. Citation metadata for the
software is in [CITATION.cff](CITATION.cff), and metadata for the data/evaluation
record is in [citation/DATA-CITATION.cff](citation/DATA-CITATION.cff).

These grants cover rights held in the included research artifacts. They do not
extend to the separately supplied manuscript, private development history,
external publications, trademarks, privacy or publicity rights. Factual
material and uses already exempt from copyright remain unaffected. Licensing
does not transfer ownership or state how ownership is allocated between the
author, contributors and a funding organization.

The earlier `v1.0` tag at commit `514d0fedccfc146ccb775eb2d4dda1729a60e43c` remains
an unchanged historical distribution. G3 introduced the license grant and metadata.
Release tag `v1.0-dataverse.1` retains those grants and restores exact frozen
evidence identity after the G12 editorial revision; see
[DISTRIBUTION-CHANGES.json](DISTRIBUTION-CHANGES.json). Use this tagged
snapshot for the Dataverse deposit; do not describe the old archive as containing
these license files. Historical statements that a license was pending describe
the state when those records were written.
