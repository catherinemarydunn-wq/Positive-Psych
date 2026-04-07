# LLM-Based Participant Simulation for the Mini Inquiry Project

## Purpose

The Mini Inquiry Project (CLO 6) asks students to design and conduct a small inquiry using AI tools. This guide describes a method for that inquiry: using an LLM to simulate participant responses to well-being survey items. Students define participant profiles, design a survey instrument, prompt the LLM to generate responses, and analyse the resulting data.

This method teaches the full research workflow (operationalisation, measurement, analysis, interpretation) without requiring ethics approval, participant recruitment, or data collection infrastructure.

## What this is (and what it is not)

**This is a methods exercise.** The simulated data reflects patterns in the LLM's training corpus, not the psychology of actual humans. Any "findings" are hypotheses worth testing with real participants, not conclusions about human well-being.

**The learning targets are:**
- Translating a research question into measurable variables
- Designing participant profiles with characteristics that could plausibly influence responses
- Constructing survey items that operationalise a construct
- Recognising patterns in data and reasoning about what they might mean
- Articulating the limitations of a data source honestly

**This is not empirical research on human psychology.** The word "inquiry" is deliberate. Students are not conducting experiments, and the report should not claim to have discovered facts about people. The correct framing is: "If participants with these characteristics responded this way, what would that suggest, and what would we need to check with real people?"

## The workflow

### Step 1: Define a research question

Start with a question that connects two things: a positive psychology concept from the course and a characteristic that varies across people.

**Examples:**
- Does the relationship between gratitude practice and reported well-being differ by cultural background?
- Do younger and older adults report different levels of flow in academic vs. leisure activities?
- Does growth mindset predict different responses to setback scenarios across education levels?

The question should be specific enough to operationalise. "Is happiness good?" is not a research question. "Do people who score higher on hedonic adaptation report lower satisfaction with repeated positive events?" is.

### Step 2: Design participant profiles

Define 8–12 participant profiles, each with characteristics relevant to your research question. The characteristics should be ones that could plausibly influence responses.

**Template:**

```
Participant ID: P01
Age: 21
Gender: Female
Cultural background: South Korean, studying in Canada for 2 years
Education: Undergraduate (second year)
Well-being baseline: Moderate (PERMA score ~6/10)
Relevant characteristic: [the variable you are studying, e.g., "practises daily gratitude journaling for 3 months"]
```

**Design principles:**
- Vary the characteristic you are studying (your independent variable) systematically across profiles. For example, if you are studying cultural background, ensure you have profiles from at least 3–4 backgrounds.
- Keep other characteristics balanced. Do not make all your gratitude-journaling participants young women and all your non-journaling participants older men.
- Use realistic, specific details. "East Asian" is too broad. "South Korean, grew up in Seoul, studying in Canada for 2 years" gives the LLM something concrete to work with, and it forces you to think about what "cultural background" actually means in your study.
- Include 2–3 characteristics beyond your main variable (age, education, cultural background, life stage) to make profiles realistic. You do not need to analyse all of them.

**Why this matters:** In real research, participant characteristics influence responses. Defining profiles explicitly makes those assumptions visible and testable. If all your simulated participants are identical except for one variable, the simulation is too clean to teach you anything about the messiness of real data.

### Step 3: Design your instrument

Write 5–8 survey items that measure the construct you are studying. Use a consistent response scale (e.g., 1–7 Likert, where 1 = strongly disagree and 7 = strongly agree).

**Example items (for a gratitude and well-being inquiry):**
1. I frequently feel thankful for the people in my life. (1–7)
2. When something good happens, I tend to take it for granted. (1–7, reverse-scored)
3. I feel satisfied with my life overall. (1–7)
4. I often compare my situation to people who have more than me. (1–7, reverse-scored)
5. I experience positive emotions (joy, contentment, hope) on most days. (1–7)

**Design principles:**
- Include at least one reverse-scored item (a "check" that the responses are consistent, not just all 7s).
- Write items at a language level your simulated participants would understand.
- Each item should measure one thing. "I feel grateful and happy" conflates two constructs.

### Step 4: Run the simulation

For each participant profile, prompt the LLM to respond to your survey items in character. Use a structured prompt that separates the participant description from the task.

**Prompt template:**

```
You are simulating a research participant for a methods exercise.
This is not real data. The purpose is to practise research design
and analysis.

PARTICIPANT PROFILE:
[Paste the full profile from Step 2]

TASK:
Respond to each survey item below using the scale provided
(1 = strongly disagree, 7 = strongly agree). Respond as this
participant would, given their background, experiences, and
current life situation. Provide only the numeric rating for
each item.

SURVEY ITEMS:
[Paste your items from Step 3]

After providing ratings, write 2–3 sentences explaining the
reasoning behind the responses, from the participant's
perspective.
```

**Important:**
- Run each participant in a **separate conversation** so that earlier participants' responses do not influence later ones.
- **Save the full exchange** (your prompt and the LLM's response) for each participant. This is your raw data, and it makes your simulation reproducible. Anyone with the same prompt and the same model should get a similar (though not identical) result.
- Record which LLM and version you used (e.g., "Claude Sonnet 4, April 2026"). Model version matters for reproducibility.

### Step 5: Compile and analyse

Enter your simulated responses into a table (spreadsheet or by hand).

| Participant | Age | Cultural background | Gratitude practice | Item 1 | Item 2 | Item 3 | ... | Mean score |
|---|---|---|---|---|---|---|---|---|
| P01 | 21 | South Korean | Yes (3 months) | 6 | 2 | 5 | ... | 5.2 |
| P02 | 45 | Canadian | No | 4 | 5 | 4 | ... | 3.6 |

**Analysis (keep it simple):**
- Calculate mean scores for each participant across items (remembering to reverse-score where needed).
- Compare means across groups (e.g., gratitude-practice group vs. no-practice group).
- Look for patterns: Do participants from certain backgrounds respond differently? Do the reverse-scored items behave as expected?
- Note any surprises: responses that seem inconsistent with the profile, or patterns you did not predict.

You are not expected to run statistical tests. Describe what you see in the data and reason about what it might mean.

### Step 6: Report

The inquiry report should include:

1. **Research question** (1–2 sentences)
2. **Method** — Describe your participant profiles, your instrument, and your simulation procedure. Be specific: which LLM, how many participants, what characteristics you varied.
3. **Results** — Present your data (a table is fine) and describe the patterns you observed.
4. **Discussion** — What do the patterns suggest? What are at least two reasons the simulated data might not match what real participants would say? What would you do differently if you were designing a study with real participants?
5. **Limitations** — This section is not optional. At minimum, address:
   - The LLM's responses reflect its training data, not actual human psychology.
   - Cultural representations in the training data may be stereotyped or inaccurate.
   - With 8–12 simulated participants, no pattern is reliable. This is a pilot, not a study.

## Connection to course learning outcomes

| CLO | How the simulation addresses it |
|---|---|
| 1 (Theoretical frameworks) | Students must operationalise a framework (PERMA, SDT, broaden-and-build, etc.) into measurable survey items. |
| 3 (Academic texts) | The report requires citing course readings to justify the research question and interpret findings. |
| 4 (Disciplinary terminology) | Participant profiles and survey items require accurate use of terms (well-being, hedonic adaptation, self-efficacy, etc.). |
| 5 (Academic discussion) | The 5-minute presentation requires supporting claims with evidence from the simulated data. |
| 6 (Design and conduct inquiry) | The entire workflow. |
| 7 (Well-being practices) | Students who study a well-being practice (gratitude, mindfulness, etc.) must understand it well enough to simulate plausible responses to it. |

## Worked example (abbreviated)

**Research question:** Do simulated participants who practise daily gratitude journaling report higher life satisfaction than those who do not, and does this differ between participants from individualist and collectivist cultural backgrounds?

**Profiles (4 of 10):**

- **P01:** 21, female, South Korean (in Canada 2 years), undergraduate, moderate well-being, gratitude journaling 3 months
- **P02:** 21, male, Canadian, undergraduate, moderate well-being, no gratitude practice
- **P03:** 34, female, Japanese (in Canada 5 years), graduate student, moderate well-being, gratitude journaling 3 months
- **P04:** 33, male, Canadian, employed, moderate well-being, no gratitude practice

**Three of five survey items:**
1. I frequently feel thankful for the people in my life. (1–7)
2. When something good happens, I tend to take it for granted. (1–7, reverse-scored)
3. I feel satisfied with my life overall. (1–7)

**What to look for:** Does the LLM produce higher satisfaction scores for the journaling participants? Does it produce different patterns for the South Korean and Japanese participants than for the Canadian participants? If so, are those differences plausible, stereotyped, or arbitrary? That interpretive question is the point of the exercise.

## Provenance

This simulation method is adapted from an agent-based participant simulation workflow used in experimental linguistics (Reynolds, 2025, unpublished), where synthetic participant profiles with demographic characteristics are used to generate judgment data for experimental design checking. The original implementation uses Python and YAML profiles; this adaptation uses conversational LLM prompting to make the method accessible to language learners.

The methodological principle is the same: participant characteristics are defined explicitly and separately from the response-generation process, making assumptions visible and the simulation reproducible. The key difference is epistemological: in the original, simulated data is used to debug experimental designs before collecting human data; here, it is used to teach the research workflow itself.
