# SWYNEX-Data-Cleaning-Preparation

Task 1 of the SWYNEX Technologies Data Analyst Internship: cleaning and preparing a public dataset with Python (pandas).

## Dataset
- **Titanic passenger data** (public), from https://github.com/datasciencedojo/datasets/blob/master/titanic.csv
- 891 rows x 12 columns

## Issues found
| Issue | Where | Count |
|---|---|---|
| Missing values | Age | 177 |
| Missing values | Cabin | 687 |
| Missing values | Embarked | 2 |
| Duplicate rows / duplicate PassengerIds | whole dataset | 0 / 0 |
| Wrong data types | Survived (0/1), Pclass, Sex, Embarked stored as numbers/text rather than bool/category | 4 columns |
| Inconsistent text | Checked casing and whitespace in Sex, Embarked, Name, Ticket, Cabin | none found; standardization applied as a safeguard |

## Steps taken
1. **Duplicates:** checked full-row and PassengerId duplicates; none existed, the check stays in the script.
2. **Age (177 missing):** extracted `Title` (Mr, Mrs, Miss, Master, Rare) from Name and filled each gap with the median age of that title. This is more accurate than one global median because Master means a boy and Mrs an adult. An `Age_Missing` flag preserves which values were imputed.
3. **Embarked (2 missing):** filled with the mode (`S`).
4. **Cabin (687 missing):** too sparse to impute, so added `Has_Cabin` (True/False) and filled with `Unknown`.
5. **Data types:** `Survived` to bool; `Pclass`, `Sex`, `Embarked`, `Title` to category; text columns trimmed; `Age` rounded to 1 decimal.
6. **Validation:** asserts confirm no nulls remain in Age, Embarked, Fare and no invalid values.

## Before vs after
| Metric | Before | After |
|---|---|---|
| Rows | 891 | 891 |
| Columns | 12 | 15 (added Age_Missing, Title, Has_Cabin) |
| Missing values | 866 | 0 |
| Duplicate rows | 0 | 0 |

## Files
- `data/raw_data.csv`: original
- `data/cleaned_data.csv`: cleaned output
- `cleaning.py`: full cleaning script (`python cleaning.py`)

## Tools
Python 3, pandas
