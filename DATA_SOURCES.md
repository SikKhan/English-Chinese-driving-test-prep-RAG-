# Chinese driving test data sources

Retrieved 2026-10-28 for research and review.

## Subject 1

`subject1-source/` is a copy of https://github.com/AgostonBodoAiGaoShi/china-drivers-license-subject1-en including the bilingual JSON, CSV, 787 images, LICENSE and SOURCES.md. The JSON contains 2,545 records. Its maintainers describe an unofficial 2022-derived question set and machine-assisted English translations. It is not verified as a current official exam bank. The repository declares MIT, but upstream ownership and the exam images' rights are not independently verified; do not assume the repo license resolves third-party rights.

## National traffic law materials

`chinese-traffic-laws/sources.json` records the source URL, download date and SHA-256 for each document. The HTML files are original downloads. The corresponding text files are automatically extracted and include site navigation; they have not been cleaned or checked article by article. The compulsory insurance PDF is an entire 2019 government gazette supplement, not a standalone extract; the regulation appears within it. The driving licence rules are the 2025 consolidated text with the amendment decision included.

These eight documents are a starting collection, not an exhaustive list of every potentially relevant national and local rule, standard or subsequent amendment. They have not been checked against the latest authoritative legal database. Confirm in-force versions, article completeness, local rules, and usage rights before using for answers or publishing.

## Machine translations (2026-11-03)

`chinese-traffic-laws/translations/` contains bilingual JSON chunks made from the eight local text extracts using the same OpenRouter model as the Subject 4 translation, `nvidia/nemotron-3.5-super-vl:free`. Each chunk retains its source text, model, source file hash and review flag. The HTML extracts include website navigation; chunks can split sentences, articles and other context. These are unreviewed machine translations, not official legal translations. They have not been checked for completeness, legal accuracy or current validity.

For the compulsory insurance regulation, `compulsory-insurance-regulation-2019.txt` was extracted from PDF pages 243–247 (PDF page numbering) with PyMuPDF, processing the two columns in reading order. All 46 article labels were detected, but extraction and translation have not been checked line by line against the PDF. The original PDF remains the authoritative local source for this extract.
