A named entity recognition model for chemical entities.

| Feature | Description |
| --- | --- |
| **Name** | `en_chem_ner` |
| **Version** | `0.1.0` |
| **spaCy** | `>=3.7.5,<3.8.0` |
| **Default Pipeline** | `tok2vec`, `ner` |
| **Components** | `tok2vec`, `ner` |
| **Vectors** | 0 keys, 0 unique vectors (0 dimensions) |
| **Sources** | n/a |
| **License** | `MIT` |
| **Author** | [Dinga Wonanke]() |

### Label Scheme

<details>

<summary>View label scheme (1 labels for 1 components)</summary>

| Component | Labels |
| --- | --- |
| **`ner`** | `CHEMICAL` |

</details>

### Accuracy

| Type | Score |
| --- | --- |
| `ENTS_F` | 91.45 |
| `ENTS_P` | 91.40 |
| `ENTS_R` | 91.50 |
| `TOK2VEC_LOSS` | 75815.27 |
| `NER_LOSS` | 124867.54 |