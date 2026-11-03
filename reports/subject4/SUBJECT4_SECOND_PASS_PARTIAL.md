# Partial second-pass machine review

Status: incomplete. This is a second automated opinion, not a completed human or independent verification. Models can misread the Chinese, fail to notice previous edits, or make unsafe changes. No decisions in this file have been automatically applied.

Records with findings checked: 64 of 261. Decisions: 112 of 393.

Requests stopped after malformed responses and free-provider rate limits. Records without a decision remain unresolved.

## trllm_subj4_1
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **reject**. The English already conveys that flight followed the rear-end collision; adding "and after that" is unnecessary and changes wording without correcting meaning.
- Finding 2 (options_en): **already_present**. The supplied English options already use periods and spaces, not Chinese enumeration commas.

## trllm_subj4_2
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (options_en): **already_present**. The supplied English options already use periods and spaces, not Chinese enumeration commas.

## trllm_subj4_3
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (options_en): **already_present**. The supplied English options already use periods and spaces, not Chinese enumeration commas.

## trllm_subj4_4
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (options_en): **already_present**. The supplied English options already use periods and spaces, not Chinese enumeration commas; no change needed.

## trllm_subj4_5
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (options_en): **already_present**. The supplied English options already use periods and spaces, not Chinese enumeration commas; no change needed.

## trllm_subj4_6
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **apply**. 沿河县 should be Yanhe County, not Cengong County.
  Suggested replacement: Luo drove a large sleeper bus (carrying 44 people, rated capacity 44 people). When reaching kilometer 58 plus 500 meters of County Road 540 in Yanhe County, the vehicle was traveling at 44 kilometers per hour on an icy road surface, causing the motor vehicle to skid and roll off the highway, resulting in 15 deaths and 27 injuries. What was Luo's main illegal act?
- Finding 2 (options_en): **already_present**. The supplied English options already use periods and spaces, not Chinese enumeration commas; no change needed.

## trllm_subj4_7
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **reject**. Current English already matches the suggested corrected location; no change needed.
- Finding 2 (options_en): **already_present**. Options already use standard English punctuation with periods.

## trllm_subj4_8
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (options_en): **already_present**. Options already use standard English punctuation with periods.

## trllm_subj4_9
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (options_en): **already_present**. Options already use standard English punctuation with periods.

## trllm_subj4_10
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (options_en): **already_present**. The English options already use standard English punctuation (periods after labels), so the suggested replacement is identical to the current text.

## trllm_subj4_11
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (options_en): **reject**. The suggestion merely retains the Chinese enumeration marks (、) that the issue identifies as a problem; it does not remove or replace them with standard punctuation.

## trllm_subj4_12
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (options_en): **reject**. The suggestion merely retains the Chinese enumeration marks (、) that the issue identifies as a problem; it does not remove or replace them with standard punctuation.

## trllm_subj4_13
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (options_en): **already_present**. The English options already contain the exact suggested text with Chinese enumeration marks; no change is needed.

## trllm_subj4_14
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (options_en): **already_present**. The English options already contain the exact suggested text with Chinese enumeration marks; no change is needed.

## trllm_subj4_15
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (options_en): **already_present**. The English options already contain the exact suggested text with Chinese enumeration marks; no change is needed.

## trllm_subj4_16
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **reject**. The Chinese option A states 陶某客车超员 (Tao's bus was overloaded), so translating it as "Tao's bus was overloaded" is faithful; changing to "carried 33 people" would alter the answer option.
- Finding 2 (option label): **reject**. The enumeration mark is a stylistic choice retained in the current English; it is not an error requiring correction and does not affect meaning.

## trllm_subj4_17
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (option label): **reject**. The enumeration mark is a stylistic choice retained in the current English; it is not an error requiring correction and does not affect meaning.

## trllm_subj4_18
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **already_present**. The current English already uses "driving against traffic" in both the question and option D, matching the suggested correction.
- Finding 2 (option D): **already_present**. The current English already uses "Bus driving against traffic" for option D, matching the suggested correction.
- Finding 3 (option label): **reject**. The enumeration mark is a stylistic choice retained in the current English; it is not an error requiring correction and does not affect meaning.

## trllm_subj4_19
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **already_present**. The English question already faithfully translates the Chinese text; no correction is needed.
- Finding 2 (option label): **reject**. The enumeration mark is intentionally retained in the English options and matches the source style; removing it is not required.

## trllm_subj4_20
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **already_present**. The English question already accurately reflects the Chinese source; no change is required.
- Finding 2 (option label): **reject**. The enumeration mark is intentionally retained in the English options and matches the source style; removing it is not required.

## trllm_subj4_21
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **apply**. The Chinese term 低速载货机动车 is a specific vehicle category; "low-speed cargo vehicle" is more precise than "low-speed cargo motor vehicle".
  Suggested replacement: Shi was driving a low-speed cargo vehicle carrying 4.05 tons of cargo (rated load 1.2 tons). While traveling on Provincial Road 314 at kilometer 51 plus 260 meters in Ningjin County, he crossed the centerline to overtake a motor vehicle traveling in the same direction ahead and collided head-on with a medium-sized passenger bus (carrying 12 people, rated capacity 11 people) traveling normally in the opposite direction, causing 10 deaths and 2 injuries. What are the illegal acts in this accident?
- Finding 2 (option A): **reject**. The English options intentionally omit the enumeration mark; adding it is not required.
- Finding 3 (option B): **reject**. The English options intentionally omit the enumeration mark; adding it is not required.
- Finding 4 (option C): **reject**. The English options intentionally omit the enumeration mark; adding it is not required.
- Finding 5 (option D): **reject**. The English options intentionally omit the enumeration mark; adding it is not required.

## trllm_subj4_22
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **reject**. Chinese source does not contain an enumeration mark after 贾某; English is faithful.
- Finding 2 (option A): **already_present**. English option A already contains the enumeration mark after A.
- Finding 3 (option B): **already_present**. English option B already contains the enumeration mark after B.
- Finding 4 (option C): **already_present**. English option C already contains the enumeration mark after C.
- Finding 5 (option D): **already_present**. English option D already contains the enumeration mark after D.

## trllm_subj4_23
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **reject**. Chinese source does not contain an enumeration mark after 陈某; English is faithful.
- Finding 2 (option A): **already_present**. English option A already contains the enumeration mark after A.
- Finding 3 (option B): **already_present**. English option B already contains the enumeration mark after B.
- Finding 4 (option C): **already_present**. English option C already contains the enumeration mark after C.
- Finding 5 (option D): **already_present**. English option D already contains the enumeration mark after D.

## trllm_subj4_24
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **reject**. Chinese source does not contain an enumeration mark after 刘某; English is faithful.
- Finding 2 (option A): **already_present**. English option A already contains the enumeration mark after A.
- Finding 3 (option B): **already_present**. English option B already contains the enumeration mark after B.
- Finding 4 (option C): **already_present**. English option C already contains the enumeration mark after C.
- Finding 5 (option D): **already_present**. English option D already contains the enumeration mark after D.

## trllm_subj4_25
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **reject**. The Chinese source does not contain an enumeration mark after 魏某; the English correctly omits it.
- Finding 2 (option A): **already_present**. The English option A already includes the enumeration mark "A、".
- Finding 3 (option B): **already_present**. The English option B already includes the enumeration mark "B、".
- Finding 4 (option C): **already_present**. The English option C already includes the enumeration mark "C、".
- Finding 5 (option D): **already_present**. The English option D already includes the enumeration mark "D、".

## trllm_subj4_26
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **already_present**. The English question already contains the sentence describing Chen's illegal acts.

## trllm_subj4_29
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **reject**. The English question does not retain "69、"; no change needed.

## trllm_subj4_31
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (option label A): **already_present**. The English option A already contains the enumeration comma after the label.
- Finding 2 (option label B): **already_present**. The English option B already contains the enumeration comma after the label.
- Finding 3 (option label C): **already_present**. The English option C already contains the enumeration comma after the label.
- Finding 4 (option label D): **already_present**. The English option D already contains the enumeration comma after the label.

## trllm_subj4_32
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (option label A): **already_present**. The English option A already contains the enumeration comma after the label.
- Finding 2 (option label B): **already_present**. The English option B already contains the enumeration comma after the label.
- Finding 3 (option label C): **already_present**. The English option C already contains the enumeration comma after the label.
- Finding 4 (option label D): **already_present**. The English option D already contains the enumeration comma after the label.

## trllm_subj4_33
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (option label A): **already_present**. The English option A already contains the enumeration comma after the label.
- Finding 2 (option label B): **already_present**. The English option B already contains the enumeration comma after the label.

## trllm_subj4_34
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (option label A): **already_present**. English option A already contains the enumeration comma after the label.
- Finding 2 (option label B): **already_present**. English option B already contains the enumeration comma after the label.

## trllm_subj4_35
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (option label A): **already_present**. English option A already contains the enumeration comma after the label.
- Finding 2 (option label B): **already_present**. English option B already contains the enumeration comma after the label.

## trllm_subj4_36
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (option C): **already_present**. English option C already includes "Try to" corresponding to Chinese "尽量".

## trllm_subj4_37
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **already_present**. The English question already contains "this situation"; the suggestion is identical to the current text.

## trllm_subj4_38
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **already_present**. The English question already contains "this situation"; the suggestion is identical to the current text.

## trllm_subj4_46
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **already_present**. The English question already contains "should" corresponding to 应当; the suggestion is identical to the current text.

## trllm_subj4_64
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (option C): **already_present**. The English option C already matches the suggested text exactly; the em dash omission is a minor typographical artifact with no meaning change.

## trllm_subj4_71
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **reject**. The finding itself states no material discrepancy and provides no suggestion; the English translation faithfully conveys the original meaning.

## trllm_subj4_73
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **reject**. The finding itself states no material discrepancy and provides no suggestion; the English translation faithfully conveys the original meaning.

## trllm_subj4_75
Reviewer: nvidia/nemotron-3.5-super-vl:free

- Finding 1 (question_en): **already_present**. The English question and options already match the Chinese meaning; the noted comma and "give way" vs "yield" are minor stylistic differences with no material discrepancy.

## trllm_subj4_76
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (question_en): **reject**. The English text already includes "may", which corresponds to the Chinese modal particle "可". The translation is accurate.

## trllm_subj4_86
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (question_en): **reject**. The English translation "show-off driving, reckless driving, spiteful driving" accurately reflects the Chinese idioms. No meaningful omission or error.

## trllm_subj4_89
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (option_en D): **reject**. The English option D already includes the condition "when safety is ensured". The Chinese option also implies safety, but the English text is not omitting the green light condition; it rephrases the safety condition. The issue description is incorrect.

## trllm_subj4_97
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (question_en): **apply**. The Chinese text "不—致" contains a typographical space, but the intended meaning "inconsistent" is correctly conveyed in the English translation. Applying the suggestion cleans up the source text without altering the question's meaning.
  Suggested replacement: When the tire pressures of all wheels of a car are inconsistent, what consequences are likely to occur?

## trllm_subj4_101
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (question_en): **reject**. The Chinese term "公路" (highway/public road) is contextually implied by "在公路上行走" (walking on the road), and omitting it does not change the core traffic safety meaning. The English translation is faithful to the original intent.

## trllm_subj4_103
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (option C): **apply**. The Chinese options "示廓灯" and "后位灯" are partially translated; "示廓灯" is explicitly missing in the English. Applying the suggestion ensures the complete and accurate translation of both terms as specified in the original Chinese.
  Suggested replacement: Turn on the clearance lights and rear position lights

## trllm_subj4_106
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (options_en A): **reject**. The suggestion adds Chinese enumeration comma '、' after label A, but the current English options do not use this formatting. Applying would introduce inconsistent formatting not present in the current English text.
- Finding 2 (options_en B): **reject**. The suggestion adds Chinese enumeration comma '、' after label B, but the current English options do not use this formatting. Applying would introduce inconsistent formatting not present in the current English text.
- Finding 3 (options_en C): **reject**. The suggestion adds Chinese enumeration comma '、' after label C, but the current English options do not use this formatting. Applying would introduce inconsistent formatting not present in the current English text.
- Finding 4 (options_en D): **reject**. The suggestion adds Chinese enumeration comma '、' after label D, but the current English options do not use this formatting. Applying would introduce inconsistent formatting not present in the current English text.

## trllm_subj4_108
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (options_en C): **reject**. The suggestion adds Chinese enumeration comma '、' after labels A and B, but the current English options do not use this formatting. Applying would introduce inconsistent formatting not present in the current English text.
- Finding 2 (options_en A, B, C, D): **apply**. The suggestion provides the exact complete replacement for all four options, adding the Chinese enumeration comma '、' after each label as present in the source Chinese, while preserving the English content.
  Suggested replacement: A、Park in designated locations; B、Prohibit parking on sidewalks; C、When temporarily parking on the road, do not obstruct the passage of other motor vehicles and pedestrians; D、May park in non-motor vehicle lanes

## trllm_subj4_109
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (options_en A, B): **reject**. The suggestion adds Chinese enumeration comma '、' after labels A and B, but the current English options do not use this formatting. Applying would introduce inconsistent formatting not present in the current English text.

## trllm_subj4_110
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (options_en A, B): **reject**. The English options A and B are direct translations of the Chinese labels. The source Chinese uses enumeration commas '、' after labels, which is standard Chinese formatting but not typically replicated in English option formatting. The suggestion 'A、True; B、False' replicates the Chinese comma style, which is unnecessary and inconsistent with English conventions.

## trllm_subj4_111
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (option C): **apply**. The English option C omits the word 'left' which is explicitly present as '左' in the Chinese source '左后方'. The translation 'situation to the rear' loses this specific directional information.
  Suggested replacement: Carefully observe the situation to the left rear

## trllm_subj4_113
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (option C): **reject**. The issue claims punctuation inconsistency between the English colon and Chinese enumeration comma. However, the English options A and B use colons (:) while C uses a Chinese enumeration comma (、). The suggestion to replace C's label with a colon would alter the option label text 'C：Park on a mountain road section prone to falling rocks' to 'C: Park on a mountain road section prone to falling rocks', which is a trivial punctuation change not substantively required and does not improve accuracy. The original English labeling is acceptable.

## trllm_subj4_114
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (option B): **reject**. Punctuation difference (、 vs :) is a formatting inconsistency, not a substantive error in the English translation or content.

## trllm_subj4_116
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (options_en B): **apply**. Option label punctuation differs from the source: source uses 'B：', translation uses 'B、'.
  Suggested replacement: B：Within parking spaces marked on the road
- Finding 2 (options_en C): **apply**. Option label punctuation differs from the source: source uses 'C：', translation uses 'C、'.
  Suggested replacement: C：Pedestrian crosswalk
- Finding 3 (options_en D): **apply**. Option label punctuation differs from the source: source uses 'D：', translation uses 'D、'.
  Suggested replacement: D：Construction section

## trllm_subj4_117
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (options_en A): **apply**. Option label punctuation differs from the source: source uses 'A：', translation uses 'A：' (matches), but options B, C, D use '、' instead of '：'. The finding notes a mismatch for B, C, D; applying the colon fix to A is consistent with correcting the pattern.
  Suggested replacement: A：Pedestrian crosswalk
- Finding 2 (options_en B): **apply**. Option label punctuation differs from the source: source uses 'B：', translation uses 'B、'.
  Suggested replacement: B：Parking lot
- Finding 3 (options_en C): **apply**. Option label punctuation differs from the source: source uses 'C：', translation uses 'C、'.
  Suggested replacement: C：Mountain road sections prone to landslides or mudslides
- Finding 4 (options_en D): **apply**. Option label punctuation differs from the source: source uses 'D：', translation uses 'D、'.
  Suggested replacement: D：Within parking spaces marked on the road

## trllm_subj4_118
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (options_en B): **apply**. Source uses 'B：', translation uses 'B、'.
  Suggested replacement: B：The vehicle body must not extend beyond the parking space
- Finding 2 (options_en C): **apply**. Source uses 'C：', translation uses 'C、'.
  Suggested replacement: C：Turn off the circuit
- Finding 3 (options_en D): **apply**. Source uses 'D：', translation uses 'D、'.
  Suggested replacement: D：Lock the doors

## trllm_subj4_121
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (question_en): **reject**. The suggestion adds '机动车' (motor vehicles) which changes the meaning; the original Chinese does not specify motor vehicles, and the English 'Motor vehicles' is an addition not present in the source.

## trllm_subj4_122
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (question_en): **reject**. The suggestion changes '社会车辆' (social vehicles) to 'Private vehicles', which reverses the meaning. The original Chinese '社会车辆' refers to social/public vehicles, not private ones.

## trllm_subj4_123
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (option C): **apply**. The original Chinese "不得停车" means "must not park". The current English "Do not park" is a valid translation but "Must not park" is more precise for the regulatory meaning.
  Suggested replacement: Must not park within 50 meters of an intersection

## trllm_subj4_125
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (option B): **reject**. The suggestion "May park随意 as long as it is convenient to leave" introduces untranslated Chinese characters, which violates the requirement to preserve or properly translate text. The current English "May park anywhere as long as it is convenient to leave" is already a complete and accurate translation of the Chinese "只要出去方便，可随意停放".

## trllm_subj4_131
Reviewer: nvidia/nemotron-3.5-lightning:free

- Finding 1 (options_en): **already_present**. The English options already accurately reflect the Chinese: "press hard" corresponds to "重踏" (press heavily) and "press lightly" corresponds to "轻踏" (press lightly). No material discrepancy exists; the suggestion "No change required" correctly identifies this.

## trllm_subj4_142
Reviewer: xingchen-agi/xing4.0-29b-a4b:free

- Finding 1 (options_en): **reject**. The issue is a formatting/punctuation concern (Chinese enumeration commas vs English periods), not a substantive content error. The English options are faithful translations of the Chinese options and do not alter any answer or meaning.

## trllm_subj4_143
Reviewer: xingchen-agi/xing4.0-29b-a4b:free

- Finding 1 (options_en): **reject**. Same formatting concern; no substantive content change. English options faithfully preserve the original Chinese meaning and answer.

## trllm_subj4_144
Reviewer: xingchen-agi/xing4.0-29b-a4b:free

- Finding 1 (options_en): **reject**. Same formatting concern; no substantive content change. English options faithfully preserve the original Chinese meaning and answer.

## Remaining records

- trllm_subj4_151: 1 findings
- trllm_subj4_155: 2 findings
- trllm_subj4_161: 1 findings
- trllm_subj4_176: 1 findings
- trllm_subj4_177: 1 findings
- trllm_subj4_181: 1 findings
- trllm_subj4_187: 1 findings
- trllm_subj4_191: 4 findings
- trllm_subj4_192: 2 findings
- trllm_subj4_211: 1 findings
- trllm_subj4_221: 2 findings
- trllm_subj4_222: 1 findings
- trllm_subj4_223: 1 findings
- trllm_subj4_224: 1 findings
- trllm_subj4_225: 1 findings
- trllm_subj4_227: 1 findings
- trllm_subj4_230: 1 findings
- trllm_subj4_231: 4 findings
- trllm_subj4_232: 1 findings
- trllm_subj4_233: 1 findings
- trllm_subj4_234: 1 findings
- trllm_subj4_235: 1 findings
- trllm_subj4_236: 2 findings
- trllm_subj4_237: 2 findings
- trllm_subj4_239: 2 findings
- trllm_subj4_241: 1 findings
- trllm_subj4_244: 1 findings
- trllm_subj4_253: 1 findings
- trllm_subj4_262: 1 findings
- trllm_subj4_266: 4 findings
- trllm_subj4_267: 2 findings
- trllm_subj4_268: 4 findings
- trllm_subj4_269: 2 findings
- trllm_subj4_270: 2 findings
- trllm_subj4_277: 4 findings
- trllm_subj4_283: 1 findings
- trllm_subj4_286: 1 findings
- trllm_subj4_287: 1 findings
- trllm_subj4_288: 1 findings
- trllm_subj4_289: 1 findings
- trllm_subj4_290: 1 findings
- trllm_subj4_297: 1 findings
- trllm_subj4_299: 1 findings
- trllm_subj4_306: 1 findings
- trllm_subj4_316: 1 findings
- trllm_subj4_317: 1 findings
- trllm_subj4_361: 3 findings
- trllm_subj4_362: 3 findings
- trllm_subj4_402: 1 findings
- trllm_subj4_404: 1 findings
- trllm_subj4_409: 1 findings
- trllm_subj4_416: 1 findings
- trllm_subj4_417: 1 findings
- trllm_subj4_419: 1 findings
- trllm_subj4_420: 1 findings
- trllm_subj4_424: 1 findings
- trllm_subj4_437: 1 findings
- trllm_subj4_439: 1 findings
- trllm_subj4_446: 1 findings
- trllm_subj4_451: 1 findings
- trllm_subj4_456: 4 findings
- trllm_subj4_459: 1 findings
- trllm_subj4_461: 1 findings
- trllm_subj4_462: 2 findings
- trllm_subj4_468: 1 findings
- trllm_subj4_471: 1 findings
- trllm_subj4_472: 1 findings
- trllm_subj4_476: 2 findings
- trllm_subj4_481: 1 findings
- trllm_subj4_482: 4 findings
- trllm_subj4_483: 1 findings
- trllm_subj4_484: 1 findings
- trllm_subj4_485: 1 findings
- trllm_subj4_486: 1 findings
- trllm_subj4_488: 1 findings
- trllm_subj4_489: 1 findings
- trllm_subj4_496: 2 findings
- trllm_subj4_497: 1 findings
- trllm_subj4_498: 1 findings
- trllm_subj4_499: 1 findings
- trllm_subj4_504: 2 findings
- trllm_subj4_505: 1 findings
- trllm_subj4_506: 2 findings
- trllm_subj4_509: 1 findings
- trllm_subj4_511: 1 findings
- trllm_subj4_514: 1 findings
- trllm_subj4_518: 1 findings
- trllm_subj4_521: 2 findings
- trllm_subj4_522: 2 findings
- trllm_subj4_524: 2 findings
- trllm_subj4_531: 1 findings
- trllm_subj4_536: 1 findings
- trllm_subj4_537: 4 findings
- trllm_subj4_538: 2 findings
- trllm_subj4_541: 1 findings
- trllm_subj4_542: 1 findings
- trllm_subj4_543: 2 findings
- trllm_subj4_544: 2 findings
- trllm_subj4_545: 2 findings
- trllm_subj4_546: 1 findings
- trllm_subj4_547: 1 findings
- trllm_subj4_548: 1 findings
- trllm_subj4_549: 1 findings
- trllm_subj4_551: 1 findings
- trllm_subj4_552: 1 findings
- trllm_subj4_562: 1 findings
- trllm_subj4_585: 1 findings
- trllm_subj4_601: 1 findings
- trllm_subj4_608: 2 findings
- trllm_subj4_611: 2 findings
- trllm_subj4_614: 2 findings
- trllm_subj4_626: 1 findings
- trllm_subj4_627: 4 findings
- trllm_subj4_628: 2 findings
- trllm_subj4_629: 1 findings
- trllm_subj4_630: 1 findings
- trllm_subj4_639: 1 findings
- trllm_subj4_646: 1 findings
- trllm_subj4_647: 1 findings
- trllm_subj4_656: 2 findings
- trllm_subj4_664: 1 findings
- trllm_subj4_666: 1 findings
- trllm_subj4_673: 4 findings
- trllm_subj4_676: 2 findings
- trllm_subj4_681: 2 findings
- trllm_subj4_682: 1 findings
- trllm_subj4_683: 1 findings
- trllm_subj4_686: 1 findings
- trllm_subj4_687: 1 findings
- trllm_subj4_688: 1 findings
- trllm_subj4_689: 1 findings
- trllm_subj4_691: 1 findings
- trllm_subj4_692: 1 findings
- trllm_subj4_693: 1 findings
- trllm_subj4_694: 1 findings
- trllm_subj4_695: 2 findings
- trllm_subj4_697: 1 findings
- trllm_subj4_698: 1 findings
- trllm_subj4_699: 1 findings
- trllm_subj4_706: 2 findings
- trllm_subj4_711: 1 findings
- trllm_subj4_721: 3 findings
- trllm_subj4_725: 2 findings
- trllm_subj4_731: 1 findings
- trllm_subj4_736: 1 findings
- trllm_subj4_741: 1 findings
- trllm_subj4_751: 3 findings
- trllm_subj4_752: 2 findings
- trllm_subj4_753: 4 findings
- trllm_subj4_754: 2 findings
- trllm_subj4_755: 4 findings
- trllm_subj4_757: 1 findings
- trllm_subj4_761: 1 findings
- trllm_subj4_766: 1 findings
- trllm_subj4_769: 1 findings
- trllm_subj4_778: 1 findings
- trllm_subj4_781: 1 findings
- trllm_subj4_784: 1 findings
- trllm_subj4_785: 1 findings
- trllm_subj4_791: 2 findings
- trllm_subj4_794: 1 findings
- trllm_subj4_795: 1 findings
- trllm_subj4_796: 1 findings
- trllm_subj4_801: 1 findings
- trllm_subj4_803: 2 findings
- trllm_subj4_805: 1 findings
- trllm_subj4_806: 1 findings
- trllm_subj4_807: 1 findings
- trllm_subj4_816: 1 findings
- trllm_subj4_826: 1 findings
- trllm_subj4_829: 1 findings
- trllm_subj4_830: 1 findings
- trllm_subj4_831: 1 findings
- trllm_subj4_833: 1 findings
- trllm_subj4_834: 1 findings
- trllm_subj4_836: 2 findings
- trllm_subj4_838: 2 findings
- trllm_subj4_840: 1 findings
- trllm_subj4_842: 1 findings
- trllm_subj4_844: 1 findings
- trllm_subj4_847: 1 findings
- trllm_subj4_853: 3 findings
- trllm_subj4_857: 1 findings
- trllm_subj4_861: 1 findings
- trllm_subj4_862: 1 findings
- trllm_subj4_869: 1 findings
- trllm_subj4_871: 1 findings
- trllm_subj4_876: 1 findings
- trllm_subj4_878: 1 findings
- trllm_subj4_880: 1 findings
- trllm_subj4_883: 1 findings
- trllm_subj4_886: 1 findings
- trllm_subj4_891: 1 findings
- trllm_subj4_896: 1 findings
- trllm_subj4_897: 1 findings
- trllm_subj4_902: 2 findings
- trllm_subj4_903: 1 findings
