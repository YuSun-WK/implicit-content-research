# TriggerBench CSV audit

Revision: `3ac26e778db94a282711f463f22ba6db99643bee`
CSV files: 36
Rows: 5600
Pairs: 2800; valid: 2800; invalid: 0

## Valid pairs by split/category

- test/ethical_violations: 97
- test/illegal_activities: 96
- test/misinformation: 95
- test/offensiveness: 95
- test/physical_harm: 81
- test/privacy: 100
- test/property_damage: 100
- test/religion_belief: 90
- test/violence: 114
- train/ethical_violations: 236
- train/illegal_activities: 229
- train/misinformation: 222
- train/offensiveness: 206
- train/physical_harm: 240
- train/privacy: 203
- train/property_damage: 205
- train/region_belief: 150
- train/violence: 241

## Issues


## Warnings

- safe_index_differs_from_image_filename: 442
- unsafe_category_annotation_differs_from_file: 297
- unsafe_index_differs_from_image_filename: 442
- Train/Test exact text overlap: 0 unique texts
- Repeated text pair IDs within split: {'train': 1, 'test': 0}
- Image presence checks use repository filenames. Image byte integrity and exact image duplicates require downloaded image bytes.
