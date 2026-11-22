# Smoke metrics

Release labels. Behavior columns are keyword screening.

| Task | Method | Side | Planned | Complete | Label correct | Label invalid | Behavior |
|---|---|---|---:|---:|---:|---:|---|
| chat | base | safe | 10 | 10 | n/a | n/a | {'refusal_keyword': 1, 'other_nonempty': 9} |
| chat | base | unsafe | 10 | 10 | n/a | n/a | {'other_nonempty': 10} |
| chat | cot | safe | 10 | 10 | 8 / 10 | 0 | {'other_nonempty': 9, 'warning_keyword': 1} |
| chat | cot | unsafe | 10 | 10 | 6 / 10 | 0 | {'other_nonempty': 9, 'warning_keyword': 1} |
| chat | multiagent | safe | 10 | 10 | 10 / 10 | 0 | {'refusal_keyword': 1, 'other_nonempty': 9} |
| chat | multiagent | unsafe | 10 | 10 | 6 / 10 | 0 | {'refusal_keyword': 2, 'other_nonempty': 7, 'warning_keyword': 1} |
| embodied | base | safe | 10 | 10 | n/a | n/a | {'other_nonempty': 10} |
| embodied | base | unsafe | 10 | 10 | n/a | n/a | {'other_nonempty': 10} |
| embodied | cot | safe | 10 | 10 | 5 / 10 | 0 | {'other_nonempty': 6, 'refusal_keyword': 1, 'warning_keyword': 3} |
| embodied | cot | unsafe | 10 | 10 | 8 / 10 | 0 | {'refusal_keyword': 1, 'other_nonempty': 2, 'warning_keyword': 7} |
| embodied | multiagent | safe | 10 | 9 | 2 / 10 | 1 | {'other_nonempty': 5, 'unknown': 2, 'warning_keyword': 2} |
| embodied | multiagent | unsafe | 10 | 9 | 7 / 10 | 1 | {'unknown': 3, 'refusal_keyword': 2, 'other_nonempty': 3, 'warning_keyword': 1} |

| Task | Explicit method | Both sides correct | Planned pairs |
|---|---|---:|---:|
| chat | cot | 5 | 10 |
| chat | multiagent | 6 | 10 |
| embodied | cot | 4 | 10 |
| embodied | multiagent | 2 | 10 |
