---
title: Wikipedia Governance Literature Review Agent Workflow
author: Dylan Boswell
date: 2025-10-28
description: Automated workflow for analyzing research on how freedom of speech laws influence Wikipedia editing activity across languages and countries.
prerequisites:
  - pdftotext command-line tool installed
  - PDF files in literature/ folder
  - paper/references.bib file exists (or will be created)
  - AI agent with file system access
---

# Wikipedia Governance Literature Review Agent Workflow

## Overview

This workflow defines how an AI agent should automatically process and summarize academic literature relevant to **the relationship between freedom of speech laws and Wikipedia editing behavior across countries and languages**. It extracts, analyzes, and integrates insights from research articles to support your project on Wikipedia Governance.

## Input

- All PDF files in the `literature/` folder (academic papers, reports, or working papers)
- Each file should relate to at least one of these topics:
  - Wikipedia editing patterns or community behavior
  - Government regulation, censorship, or freedom of expression
  - Cross-linguistic or cross-national online participation
  - Information access, governance, or policy analysis

## Output

Create or update:

- [`literature/literature-review.md`](literature/literature-review.md): structured summaries emphasizing connections between freedom of speech and Wikipedia activity.
- [`paper/references.bib`](paper/references.bib): properly formatted BibTeX entries.

---

## Instructions

For each **new** PDF article in the `literature/` folder:

### 1. Convert PDF to Text

- Use the `pdftotext` command-line tool to convert `name.pdf` → `name.txt`
- Store the text file in the same folder.

### 2. Extract Key Information

Add a new section to `literature-review.md` containing the following structured fields:

- **Google Scholar Link**: Search link with the full article title.
- **Summary (2–3 sentences)**: Describe the _main argument or contribution_ of the article. Focus on how it relates to:

  - Freedom of expression, censorship, or digital rights
  - Wikipedia or other collaborative online platforms
  - Cross-country/language comparisons of online participation

- **Research Focus (1–2 sentences)**: Specify whether the paper primarily studies:

  - Government or institutional regulation
  - User/community behavior on Wikipedia or similar platforms
  - Data-driven measurement (e.g., edit counts, user demographics, policy impact)
  - Theoretical frameworks (e.g., governance, digital democracy, or information inequality)

- **Methodology (2–3 sentences)**: Summarize:

  - Research design (quantitative, qualitative, or mixed)
  - Data sources (Wikipedia dumps, policy indices, etc.)
  - Country/language scope (e.g., “English vs. Arabic Wikipedia,” or “countries with high vs. low press freedom”)

- **Findings (2–3 sentences)**: Focus on results that connect:

  - Freedom of speech conditions → Wikipedia participation rates
  - Censorship or regulation → editing activity or bias
  - Country/language characteristics → content production and governance

- **Relevance to Our Research (1–2 sentences)**: Explicitly explain _how this paper informs or contrasts_ with the project’s question on freedom of speech and Wikipedia editing.

- **Evaluation (1–5 scale + 1 sentence justification)**: Rate paper’s importance and credibility for this topic. Consider:

  - Quality of data/methods
  - Relevance to the research question
  - Clarity of argument and reproducibility

- **Resources**: List available supplementary links:
  - Code repositories (GitHub, OSF, etc.)
  - Datasets or public repositories
  - Project websites
  - Policy indices (e.g., Freedom House, V-Dem)

### 3. Create BibTeX Entry

- Generate and append a proper BibTeX entry to `paper/references.bib`.
- Format:
  - Entry type: `@article`, `@inproceedings`, or `@book`
  - Fields: `author`, `title`, `year`, `journal` or `booktitle`, `publisher`
  - Title format:  
    `title = {\href{https://scholar.google.com/scholar?q=TITLE}{TITLE}}`
  - Citation key: `firstauthorlastnameYEARkeyword`
  - Maintain alphabetical order and avoid duplicates.

### 4. Formatting

- Use consistent Markdown headers.
- Use `---` separators between articles.
- Include all required fields, even if “Not specified” for missing data.

---

## Constraints

- Only summarize _new_ PDFs (check if already in literature-review.md).
- Ensure each section explicitly connects to **freedom of speech** or **Wikipedia editing**.
- Keep summaries concise and analytical (no more than 12 sentences per article).
- Preserve prior entries and maintain alphabetical order.

---

## Expected Output Format

```markdown
## [Article Title] (Year)

**Authors**: [Author names]  
**Google Scholar**: [Link to search]

**Summary**: [2–3 sentences on main contribution related to freedom of speech/Wikipedia]  
**Research Focus**: [Topic focus, e.g., censorship, participation, regulation]  
**Methodology**: [Approach, data, and scope]  
**Findings**: [Key cross-country or linguistic findings]  
**Relevance to Our Research**: [How it connects to our central question]  
**Evaluation**: [Rating 1–5]/5 — [1 sentence justification]

**Resources**:

- Code: [link if available]
- Data: [link if available]
- Policy Index: [Freedom House/V-Dem reference if applicable]
- Project: [link if available]

---
```

---

## Verification Checklist

- [ ] Each PDF has a corresponding `.txt` file.
- [ ] Each summary explicitly addresses freedom of speech and Wikipedia.
- [ ] Relevance section is present for every entry.
- [ ] BibTeX entries are valid and alphabetized.
- [ ] Markdown file is properly formatted and renders without errors.
- [ ] No duplicate summaries or citations.
- [ ] All titles link to Google Scholar searches.
