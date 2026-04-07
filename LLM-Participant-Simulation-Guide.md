# LLM-Based Participant Simulation for the Mini Inquiry Project

## Purpose

The Mini Inquiry Project (CLO 6) asks students to design and conduct a small inquiry using AI tools. This guide describes a method for that inquiry: building a simulation that generates synthetic participant responses to well-being survey items. Students specify a research design (what characteristics to vary, what distributions, what effects to model), then use an LLM to generate participant profiles and write or adapt a Python simulation script. The simulation produces a CSV dataset that students then analyse and report on.

This method teaches the full research workflow (operationalisation, measurement, simulation, analysis, interpretation) without requiring ethics approval, participant recruitment, or data collection infrastructure.

## What this is (and what it is not)

**This is a methods exercise.** The simulated data reflects modelling assumptions that the student makes explicit in code, not the psychology of actual humans. Any "findings" are hypotheses worth testing with real participants, not conclusions about human well-being.

**The learning targets are:**
- Translating a research question into measurable variables
- Specifying a participant population: what characteristics matter, what their distributions should look like, and why
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

### Step 2: Specify the participant design

Decide what characteristics your simulated participants should have and how those characteristics should be distributed. You are not writing individual profiles; you are specifying the population, and the LLM will generate the profiles.

**What to specify:**
- **Sample size.** Choose a number large enough for your analysis to be meaningful. With code, there is no practical cost to generating 200 or 500 participants. Ask the LLM what sample size gives adequate statistical power for the effect size you expect.
- **Characteristics and distributions.** Which demographic and psychological variables matter for your research question? What should their distributions look like?
- **Your independent variable.** How should participants be split across conditions?

**Example specification (for a gratitude × cultural background inquiry):**

> Generate 300 participant profiles as YAML files. Each participant should have:
> - `participant_id` (P001–P300)
> - `age` (18–55, skewed toward 20s — university population)
> - `gender` (55% female, 43% male, 2% non-binary)
> - `cultural_background` (equal thirds: East Asian international students in Canada, South Asian international students in Canada, Canadian-born — with specific nationalities and years-in-Canada details, not just region labels)
> - `education` (all undergraduate, years 1–4 uniformly distributed)
> - `wellbeing_baseline` (low / moderate / high, distributed 20% / 60% / 20%)
> - `gratitude_practice` (half daily_journaling, half none — balanced across cultural backgrounds)
> - `gratitude_duration_months` (1–6 for journaling participants, 0 for others)
> - `random_seed` (unique integer per participant)

**The student's job is the design, not the data entry.** Deciding that cultural background should be split into equal thirds (rather than proportional to the actual student body) is a design choice that needs justifying. Deciding that well-being baseline should be 20/60/20 is a modelling assumption. These decisions are where the learning happens. Generating 300 YAML files from that specification is mechanical work that the LLM does.

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

Use an LLM to write or adapt a Python script that generates ratings. Two options:

**Option A: Adapt the reference script.** A reference implementation (`simulate_wellbeing.py`) is provided with this guide. Ask an LLM to modify the effect model to match your research question. For example: "I want cultural_background to influence the base rating for gratitude items. Participants from collectivist backgrounds should show a smaller effect of individual gratitude practice. How should I change the `compute_base_rating` function?"

**Option B: Have the LLM write a script from scratch.** Describe your research question, your participant design, and your survey items. Give it the reference script as an example of the architecture you want.

**Either way, the script should:**
1. Load participant profiles from YAML files
2. Load survey items from CSV
3. Compute a base rating for each participant–item pair using explicit effect assumptions (e.g., gratitude practice adds +0.8 to satisfaction items; older participants rate 0.01 lower per year)
4. Add participant-level random effects (consistent across items for each participant) and residual noise (trial-by-trial variability)
5. Constrain ratings to the 1–7 scale
6. Output a CSV with one row per participant–item pair, including participant demographics and ratings

**Critical principle:** The effect assumptions (Step 4.3) are the model's claims about the world. Students must state them explicitly, not hide them inside the code. A good simulation makes its assumptions visible so they can be questioned.

**Reproducibility:** Running the script with the same random seed must produce identical output. Record the seed, the LLM and version used to write or adapt the code, and any prompts given.

### Step 5: Analyse the output

The simulation produces a CSV file. Use a spreadsheet, or ask the LLM to help with analysis and visualisation. The data is standard tabular data; any tool works.

**Analysis:**
- Mean ratings by group (e.g., gratitude-practice vs. no-practice)
- Mean ratings by item (do reverse-scored items behave as expected?)
- Comparisons across your independent variable (e.g., does cultural background moderate the gratitude effect?)
- With an adequate sample size, basic statistical tests (t-test, ANOVA, or a simple regression) are feasible. Ask the LLM to run them and explain the output.

**The interesting question is not "what does the data show?" but "what did I assume, and what would change if I assumed differently?"** Change one effect parameter and rerun. Does the pattern hold? This is what simulation is for: testing the sensitivity of conclusions to assumptions.

### Step 6: Report

The inquiry report should include:

1. **Research question** (1–2 sentences)
2. **Method** — Describe your participant design (characteristics, distributions, sample size, and why), your instrument, your effect model (what you assumed and why), and your simulation procedure. Specify the LLM used, the random seed, and the number of participants.
3. **Results** — Present your data (summary tables and/or figures) and describe the patterns.
4. **Discussion** — What do the patterns suggest? What assumptions drive the result? What would you do differently with real participants?
5. **Limitations** — This section is not optional. At minimum, address:
   - The data reflects the effect model you built, not human psychology. Different assumptions produce different patterns.
   - If you used an LLM to help set effect sizes, those reflect the LLM's training data, which may encode stereotypes or inaccuracies.
   - The simulation cannot surprise you the way real data can. It confirms or disconfirms the internal logic of your model, not a hypothesis about the world.

## Connection to course learning outcomes

| CLO | How the simulation addresses it |
|---|---|
| 1 (Theoretical frameworks) | Students operationalise a framework (PERMA, SDT, broaden-and-build, etc.) into survey items and explicit effect assumptions. |
| 3 (Academic texts) | The report requires citing course readings to justify the research question, the effect model, and the interpretation. |
| 4 (Disciplinary terminology) | Participant design specifications, survey items, and effect-model descriptions require accurate use of terms (well-being, hedonic adaptation, self-efficacy, etc.). |
| 5 (Academic discussion) | The 5-minute presentation requires supporting claims with evidence from the simulated data. |
| 6 (Design and conduct inquiry) | The entire workflow. |
| 7 (Well-being practices) | Students who study a well-being practice (gratitude, mindfulness, etc.) must understand it well enough to specify how it should influence responses. |

## Provenance

This simulation method is adapted from an agent-based participant simulation workflow used in experimental linguistics (Reynolds, 2025, unpublished), where synthetic participant profiles with demographic characteristics generate judgment data for experimental design checking. The original uses Python and YAML profiles to produce 3,672 observations from 102 participants in a Latin-square design.

The methodological principle is the same: participant characteristics are defined explicitly and separately from the effect model, making assumptions visible and the simulation reproducible. The key difference is epistemological: in the original, simulated data debugs experimental designs before collecting human data; here, it teaches the research workflow itself.
