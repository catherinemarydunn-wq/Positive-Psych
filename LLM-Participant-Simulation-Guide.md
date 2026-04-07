# LLM-Based Participant Simulation for the Mini Inquiry Project

## Purpose

The Mini Inquiry Project (CLO 6) asks students to design and conduct a small inquiry using AI tools. This guide describes a method for that inquiry: building a simulation that generates synthetic participant responses to well-being survey items. Students define participant profiles, design an instrument, and either adapt a reference Python script or have an LLM write one for their specific research question. The simulation produces a CSV dataset that students then analyse and report on.

This method teaches the full research workflow (operationalisation, measurement, simulation, analysis, interpretation) without requiring ethics approval, participant recruitment, or data collection infrastructure.

## What this is (and what it is not)

**This is a methods exercise.** The simulated data reflects modelling assumptions that the student makes explicit in code, not the psychology of actual humans. Any "findings" are hypotheses worth testing with real participants, not conclusions about human well-being.

**The learning targets are:**
- Translating a research question into measurable variables
- Designing participant profiles with characteristics that could plausibly influence responses
- Constructing survey items that operationalise a construct
- Using an LLM to build or adapt a simulation (code as a tool, not an end in itself)
- Recognising patterns in data and reasoning about what they might mean
- Articulating the limitations of a data source honestly

**This is not empirical research on human psychology.** The word "inquiry" is deliberate. Students are not conducting experiments, and the report should not claim to have discovered facts about people. The correct framing is: "Given these modelling assumptions, the simulation produced these patterns. Here is what that suggests we should investigate with real participants."

## The workflow

### Step 1: Define a research question

Start with a question that connects two things: a positive psychology concept from the course and a characteristic that varies across people.

**Examples:**
- Does the relationship between gratitude practice and reported well-being differ by cultural background?
- Do younger and older adults report different levels of flow in academic vs. leisure activities?
- Does growth mindset predict different responses to setback scenarios across education levels?

The question should be specific enough to operationalise. "Is happiness good?" is not a research question. "Do people who score higher on hedonic adaptation report lower satisfaction with repeated positive events?" is.

### Step 2: Design participant profiles

Define 20–40 participant profiles, each with characteristics relevant to your research question. Profiles are stored as individual YAML files, one per participant.

**Example profile (`participants/P01.yaml`):**

```yaml
participant_id: P01
age: 21
gender: Female
cultural_background: South Korean, studying in Canada for 2 years
education: Undergraduate (second year)
wellbeing_baseline: moderate
gratitude_practice: daily_journaling
gratitude_duration_months: 3
random_seed: 48291
```

**Design principles:**
- Vary the characteristic you are studying (your independent variable) systematically across profiles. If you are studying cultural background, include profiles from at least 3–4 backgrounds. If you are studying gratitude practice, include a clear split between practice and no-practice groups.
- Keep other characteristics balanced. Do not make all your gratitude-journaling participants young women and all your non-journaling participants older men.
- Use realistic, specific details. "East Asian" is too broad. "South Korean, grew up in Seoul, studying in Canada for 2 years" forces you to think about what "cultural background" actually means in your study.
- Include 2–3 characteristics beyond your main variable (age, education, cultural background, life stage) to make profiles realistic.
- Give each participant a unique `random_seed` for reproducibility.

**Why this matters:** In real research, participant characteristics influence responses. Defining profiles explicitly makes those assumptions visible. The YAML format keeps participant metadata separate from the simulation logic, so you can change your effect model without redefining your participants.

### Step 3: Design your instrument

Write 5–8 survey items that measure the construct you are studying. Use a consistent response scale (e.g., 1–7 Likert, where 1 = strongly disagree and 7 = strongly agree).

**Example items (for a gratitude and well-being inquiry):**
1. I frequently feel thankful for the people in my life. (1–7)
2. When something good happens, I tend to take it for granted. (1–7, reverse-scored)
3. I feel satisfied with my life overall. (1–7)
4. I often compare my situation to people who have more than me. (1–7, reverse-scored)
5. I experience positive emotions (joy, contentment, hope) on most days. (1–7)

Store items in a CSV file (`items/survey_items.csv`) with columns for `item_id`, `item_text`, `construct`, and `reverse_scored`.

**Design principles:**
- Include at least one reverse-scored item (a check that the model produces internally consistent responses, not just all 7s).
- Each item should measure one thing. "I feel grateful and happy" conflates two constructs.

### Step 4: Build the simulation

This is where the LLM interaction happens. You have two options:

**Option A: Adapt the reference script.** A reference implementation (`simulate_wellbeing.py`) is provided with this guide. It loads YAML participant profiles, reads survey items from CSV, and generates ratings based on participant characteristics. Ask an LLM to help you modify the effect model to match your research question. For example: "I want cultural_background to influence the base rating for gratitude items. Participants from collectivist backgrounds should show a smaller effect of individual gratitude practice. How should I change the `compute_base_rating` function?"

**Option B: Have the LLM write a script from scratch.** Describe your research question, your participant profiles, and your survey items to the LLM and ask it to produce a Python script that generates simulated responses. Give it the reference script as an example of the structure you want.

**Either way, the script should:**
1. Load participant profiles from YAML files
2. Load survey items from CSV
3. Compute a base rating for each participant-item pair using explicit effect assumptions (e.g., gratitude practice adds +0.8 to satisfaction items; older participants rate 0.01 lower per year)
4. Add participant-level random effects (consistent across items for each participant) and residual noise (trial-by-trial variability)
5. Constrain ratings to the 1–7 scale
6. Output a CSV with one row per participant-item pair, including participant demographics and ratings

**Critical principle:** The effect assumptions (Step 4.3) are the model's claims about the world. Students must state them explicitly, not hide them inside the code. A good simulation makes its assumptions visible so they can be questioned.

**Reproducibility:** Running the script with the same random seed should produce identical output. Record the seed, the LLM and version used to write or adapt the code, and any prompts you gave it.

### Step 5: Analyse the output

The simulation produces a CSV file. Open it in a spreadsheet or use the LLM to help you summarise it.

**Basic analysis:**
- Calculate mean ratings by group (e.g., gratitude-practice vs. no-practice)
- Calculate mean ratings by item (do reverse-scored items behave as expected?)
- Compare means across your independent variable (e.g., does cultural background moderate the gratitude effect?)
- Look for surprises: patterns you did not build into the effect model, or effects that are larger or smaller than you expected

**If you want to go further** (not required), ask an LLM to help you run a simple statistical test or produce a plot. The data is in CSV, so standard tools work.

**The interesting question is not "what does the data show?" but "what did I assume, and what would change if I assumed differently?"** Try changing one effect parameter and rerunning the simulation. Does the pattern hold? This is what the simulation is for: testing the sensitivity of your conclusions to your assumptions.

### Step 6: Report

The inquiry report should include:

1. **Research question** (1–2 sentences)
2. **Method** — Describe your participant profiles, your instrument, your effect model (what you assumed and why), and your simulation procedure. Specify the LLM used to build or adapt the code, the random seed, and the number of participants.
3. **Results** — Present your data (a summary table and/or a figure) and describe the patterns.
4. **Discussion** — What do the patterns suggest? What assumptions drive the result? What would you do differently if you were designing a study with real participants?
5. **Limitations** — This section is not optional. At minimum, address:
   - The data reflects the effect model you built, not human psychology. Different assumptions would produce different patterns.
   - If you used an LLM to help set effect sizes, those reflect the LLM's training data, which may encode stereotypes or inaccuracies.
   - With 20–40 simulated participants and explicit effect assumptions, the simulation cannot surprise you in the way real data can. It confirms or disconfirms the internal logic of your model, not a hypothesis about the world.

## Connection to course learning outcomes

| CLO | How the simulation addresses it |
|---|---|
| 1 (Theoretical frameworks) | Students operationalise a framework (PERMA, SDT, broaden-and-build, etc.) into survey items and explicit effect assumptions. |
| 3 (Academic texts) | The report requires citing course readings to justify the research question, the effect model, and the interpretation. |
| 4 (Disciplinary terminology) | Participant profiles, survey items, and effect-model descriptions require accurate use of terms (well-being, hedonic adaptation, self-efficacy, etc.). |
| 5 (Academic discussion) | The 5-minute presentation requires supporting claims with evidence from the simulated data. |
| 6 (Design and conduct inquiry) | The entire workflow. |
| 7 (Well-being practices) | Students who study a well-being practice (gratitude, mindfulness, etc.) must understand it well enough to specify how it should influence responses. |

## Provenance

This simulation method is adapted from an agent-based participant simulation workflow used in experimental linguistics (Reynolds, 2025, unpublished), where synthetic participant profiles with demographic characteristics generate judgment data for experimental design checking. The original uses Python and YAML profiles to produce 3,672 observations from 102 participants in a Latin-square design.

The methodological principle is the same: participant characteristics are defined explicitly and separately from the effect model, making assumptions visible and the simulation reproducible. The key difference is epistemological: in the original, simulated data debugs experimental designs before collecting human data; here, it teaches the research workflow itself.
