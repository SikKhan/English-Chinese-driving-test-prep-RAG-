# Subject 4 translation review — 2026-11-02

## Scope and status

The dataset contains 904 bilingual records. This is a preliminary review, not a completed line-by-line review. All 904 records retain `translation_review_required: true`; no translation or answer was changed. Automated checks found no empty question, options, or answer fields. A basic digit comparison flagged six records; manual inspection shows that at least four are formatting or Chinese-number conversion differences, so such differences alone do not establish an error.

## Records needing repair or attention

- `trllm_subj4_25`: The Chinese question is split across the question and options fields. The English question contains the whole scenario, and the English options are separately repeated. Restore the Chinese field boundary before ingestion.
- `trllm_subj4_27`: A chapter heading is stored as the question; the actual statement is in the options fields. The English heading incorrectly makes “192 questions” into “Question 192”. Restore the statement as the question and correctly represent the true/false choices.
- `trllm_subj4_196`, `trllm_subj4_274`, `trllm_subj4_289`, `trllm_subj4_295`: The Chinese question is split into the options field. For 289 and 295, Chinese fragments also remain in the English options field. Reassemble and clean the fields.
- `trllm_subj4_437`: The question is duplicated in both options fields, with Chinese remaining in the English field. Remove the duplicated prompt after verifying field boundaries.
- `trllm_subj4_467`: The Chinese options contain line breaks within words; the English options appear to have preserved their meaning. Normalize only after comparing to the source.
- `trllm_subj4_517`: The Chinese source omits the D option label; English adds it. The apparent interpretation is plausible but requires source verification before treating the label as confirmed.
- `trllm_subj4_689`: Both options fields contain a trailing Chinese fragment, `参考`. Remove it only after checking the original source and whether any content is missing.
- `trllm_subj4_1`: The prompt asks for the driver's “main illegal act” in the singular, but the recorded answer is ABD. The Chinese phrasing can support a plural question; “main illegal acts” would make the multiple-answer format clearer.

## Additional notes

The source-review flags identify the ten records listed above, but they do not guarantee that all other records are free of source or translation problems. The digit comparison also flagged 1, 11, 13, 15, 610 and 806; examples include English clock formatting, Arabic numerals for Chinese numerals, and an explicit conversion of 百毫升 to 100 milliliters. These require contextual judgment, not automatic replacement. This review did not verify legal accuracy, current rules, image dependencies, every answer key, or every translation.
