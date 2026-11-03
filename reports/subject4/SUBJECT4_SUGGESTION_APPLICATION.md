# Subject 4 suggestion application

The model review contains demonstrably incorrect suggestions as well as valid ones. Only source-checked corrections and option punctuation changes that preserve the option text were applied. All other suggestions remain in the machine findings report for individual review. No answer keys or Chinese source claims were changed. Translation-review and source-review flags remain set.

## Applied changes

- **trllm_subj4_6**: question_en: Cengong County -> Yanhe County; options_en: standardized option label punctuation
- **trllm_subj4_7**: question_en: the Hunan Tou section of Hulou Road in Qianling Village, Qidu Town -> the Hunantou section of Qianling Village, Sidu Town; options_en: standardized option label punctuation
- **trllm_subj4_18**: question_en: driving in reverse -> driving against traffic; options_en: Bus driving in reverse -> Bus driving against traffic
- **trllm_subj4_86**: question_en: driving hero cars, risky cars, spite cars, and cars with defects -> show-off driving, reckless driving, spiteful driving, and driving a vehicle with defects
- **trllm_subj4_125**: options_en: May park随意 as long as it is convenient to leave -> May park anywhere as long as it is convenient to leave
- **trllm_subj4_673**: options_en: place it outside 50 meters behind the vehicle -> place it more than 50 meters behind the vehicle
- **trllm_subj4_1**: options_en: standardized option label punctuation
- **trllm_subj4_2**: options_en: standardized option label punctuation
- **trllm_subj4_3**: options_en: standardized option label punctuation
- **trllm_subj4_4**: options_en: standardized option label punctuation
- **trllm_subj4_5**: options_en: standardized option label punctuation
- **trllm_subj4_8**: options_en: standardized option label punctuation
- **trllm_subj4_9**: options_en: standardized option label punctuation
- **trllm_subj4_10**: options_en: standardized option label punctuation
- **trllm_subj4_142**: options_en: standardized option label punctuation
- **trllm_subj4_143**: options_en: standardized option label punctuation
- **trllm_subj4_144**: options_en: standardized option label punctuation
- **trllm_subj4_402**: options_en: standardized option label punctuation

## Examples of suggestions not applied

- 227: The Chinese says neck, but the model suggested head.
- 253: The Chinese says consistent; the model suggested not consistent.
- 461 and 781: The suggestions reverse the sequence stated in Chinese.
- 611, 646, 681, 766 and 891: The suggestions reverse the direction or rule in the source.
- 211, 601 and 778: Suggested option changes add negations absent from the source.
- 862: The source says downwind, while the model suggested upwind.
- Several suggestions propose changing answer keys or revealing the answer in a true/false question; these require independent source verification.

Applied changes to 18 records. The complete machine output remains in reports/subject4/SUBJECT4_MODEL_FINDINGS.md and reports/subject4/subject4_review_results.json. A backup of the dataset before these changes is stored in data/subject4/backups/subject4_translations_before_suggestion_application.json.
