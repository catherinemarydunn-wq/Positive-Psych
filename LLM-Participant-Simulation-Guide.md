# LLM-Based Participant Simulation for the Mini Inquiry Project

## Purpose

The Mini Inquiry Project (CLO 6) asks students to design and conduct a small inquiry using AI tools. This guide describes a method for that inquiry: building a simulation that generates synthetic participant responses to well-being survey items. Students specify a research design (what characteristics to vary, what distributions, what effects to model, what analyses to run), then use an LLM to generate profiles, write simulation code, produce analyses, and draft descriptive sections of the report. The student's work is the design decisions, the evaluation of LLM output, and the interpretation.

This method teaches the full research workflow (operationalisation, measurement, simulation, analysis, interpretation) without requiring ethics approval, participant recruitment, or data collection infrastructure.

## What this is (and what it is not)

**This is a methods exercise.** The simulated data reflects modelling assumptions that the student makes explicit in code, not the psychology of actual humans. Any "findings" are hypotheses worth testing with real participants, not conclusions about human well-being.

**The learning targets are:**
- Translating a research question into measurable variables
- Specifying a participant population: what characteristics matter, what their distributions should look like, and why
- Specifying what constructs to measure and evaluating whether generated items actually measure them
- Specifying effect assumptions and justifying their direction and size from course readings
- Specifying prior beliefs about effects and justifying the choice of informative vs. vague priors
- Deciding what analytical questions to ask and interpreting posterior probabilities and credible intervals
- Evaluating and revising LLM-generated output at every stage (profiles, items, code, analysis, prose)
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
- **Sample size.** Choose a number large enough for your analysis to be meaningful. With code, there is no practical cost to generating 200 or 500 participants. Larger samples produce narrower credible intervals (more precise estimates). Ask the LLM what sample size gives useful precision for the effect size you expect.
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

Specify what your survey should measure, how, and why. The LLM generates the items; you make the design decisions.

**What to specify:**
- **Constructs.** Which psychological constructs does your research question require you to measure? (e.g., gratitude, life satisfaction, hedonic adaptation). Justify each from your course readings.
- **Scale.** What response format? (e.g., 1–7 Likert, where 1 = strongly disagree and 7 = strongly agree). Why that scale?
- **Item count.** How many items per construct? More items per construct = more reliable measurement, but the instrument gets longer. Ask the LLM what is standard for the constructs you are measuring.
- **Reverse-scored items.** Require at least some. These check that the model produces internally consistent responses, not just all 7s.
- **Item quality constraints.** Each item should measure one thing ("I feel grateful and happy" conflates two constructs). Items should be at a language level your simulated population would understand.

**Example specification (for a gratitude × cultural background inquiry):**

> Generate a survey instrument as a CSV file with columns for item_id, item_text, construct, and reverse_scored. I need items measuring two constructs: gratitude (8 items, including 2 reverse-scored) and life satisfaction (6 items, including 2 reverse-scored). Use a 1–7 Likert scale. Items should be written at a B2 English level. Base the items on established instruments (GQ-6 for gratitude, SWLS for satisfaction) but do not copy them verbatim.

**The student's job is the specification.** Deciding to measure gratitude and satisfaction (rather than, say, flow and meaning) is a design choice that follows from the research question. Deciding on 8 + 6 items with reverse scoring is a methodological choice. Writing 14 individual item stems is mechanical work the LLM handles. The student should review the generated items and revise any that are unclear, double-barrelled, or off-construct — that evaluation is the skill being practised.

Store items in a CSV file (`items/survey_items.csv`).

### Step 4: Build and run the simulation

Give the LLM your full design specification (research question, participant design, instrument, effect assumptions) and have it handle Steps 2–4 as a single workflow. If your LLM tool supports sub-agents (e.g., Copilot CLI's `/fleet` command), it can dispatch profile generation, script writing, and simulation execution as parallel subtasks. Otherwise, a single conversation with the reference script as context works fine.

**Two starting points:**

**Option A: Adapt the reference script.** A reference implementation (`simulate_wellbeing.py`) is provided with this guide. Ask the LLM to modify the effect model to match your research question. For example: "I want cultural_background to influence the base rating for gratitude items. Participants from collectivist backgrounds should show a smaller effect of individual gratitude practice. How should I change the `compute_base_rating` function?"

**Option B: Have the LLM write a script from scratch.** Describe your full design. Give it the reference script as an example of the architecture you want.

**Either way, the script should:**
1. Load participant profiles from YAML files
2. Load survey items from CSV
3. Compute a base rating for each participant–item pair using explicit effect assumptions (e.g., gratitude practice adds +0.8 to satisfaction items; older participants rate 0.01 lower per year)
4. Add participant-level random effects (consistent across items for each participant) and residual noise (trial-by-trial variability)
5. Constrain ratings to the 1–7 scale
6. Output a CSV with one row per participant–item pair, including participant demographics and ratings

**The student's job is the effect model specification, not the code.** Deciding that gratitude practice should add ~0.8 to satisfaction ratings is a claim about the world that the student must justify from course readings (e.g., "Emmons & McCullough, 2003, found a medium effect"). Deciding that collectivist cultural background moderates that effect is a theoretical commitment. The LLM translates these specifications into `compute_base_rating()`. The architecture around it (YAML loading, noise model, CSV output) is boilerplate the LLM handles. The student should review the generated code to confirm it implements what they specified.

**Reproducibility:** Running the script with the same random seed must produce identical output. Record the seed, the LLM and version used to write or adapt the code, and any prompts given.

### Step 5: Analyse the output

The simulation produces a CSV file. Specify what you want to know; the LLM produces the analysis. This course uses **Bayesian statistics**, which answer questions in the form students naturally think in: "How probable is it that this effect is real, and how big is it likely to be?"

#### Why Bayesian

Frequentist statistics answer a question nobody asked ("If there were no effect, how often would we see data this extreme?"). Bayesian statistics answer the actual question ("Given the data, how probable is it that gratitude practice increases satisfaction, and by how much?"). For a methods exercise where students are learning to reason about evidence, Bayesian posterior probabilities are both more honest and more intuitive.

#### What to specify

The student makes three kinds of decisions. The LLM implements all of them.

**Priors — what you expect before seeing the data:**
- For each effect in your model, specify a prior belief about its direction and size. This is a design decision that the student justifies from course readings.
- Example: "Based on Emmons & McCullough (2003), I expect gratitude practice to have a positive effect on satisfaction of roughly 0.5–1.0 points on a 7-point scale. I'll use a normal prior centred on 0.7 with SD 0.3."
- Example: "I'm genuinely uncertain whether cultural background moderates the gratitude effect. I'll use a prior centred on 0 with SD 0.5."
- A prior that says "I don't know" (wide, centred on zero) is a legitimate and honest choice. A prior that says "I'm fairly sure" (narrow, centred away from zero) is also legitimate if justified. The student must explain which and why.

**Model — what comparisons to make:**
- What is the outcome variable? (e.g., mean satisfaction rating)
- What are the predictors? (e.g., gratitude practice, cultural background, their interaction)
- Ask the LLM to fit a Bayesian regression using the simulation output. The LLM chooses the implementation (PyMC, Stan, or a simpler conjugate approach for straightforward designs). The student does not need to understand the sampling algorithm.

**Posterior summaries — what to report:**
- Ask the LLM for posterior distributions of each effect, credible intervals (e.g., 89% CI), and the probability that each effect is in the expected direction.
- Ask for visualisations: posterior density plots for key effects, and a plot showing the predicted group means with uncertainty.

#### Interpreting the output

Bayesian results produce statements like:

- "There is a 94% probability that gratitude practice increases satisfaction ratings (median effect: 0.72 points, 89% CI: [0.38, 1.09])."
- "The probability that cultural background moderates the gratitude effect is 68%, with the moderation estimate centred near −0.25 (89% CI: [−0.61, 0.14])."

**The student's job is interpreting what these statements mean for their research question.** The first statement suggests a fairly confident positive effect. The second suggests genuine uncertainty about the moderation — the credible interval includes zero, so the data are compatible with no moderation at all. What would it take to resolve that uncertainty? A larger sample? A different operationalisation of "cultural background"? That reasoning is the student's, not the LLM's.

**Sanity checks.** Do the reverse-scored items behave as expected? Are the posterior effect sizes close to what you specified in the simulation? They should be, since you built the effects in. If the posteriors recover your assumed effects, the model is working. If they don't, something is wrong in the code or the model specification.

**Sensitivity analysis.** The most interesting analytical move is changing a prior or an effect assumption and rerunning. What if you used a sceptical prior (centred on zero) for the main effect? Does the posterior still show a positive effect, or does it collapse? What if the cultural moderation were twice as large in the simulation? Specify what to vary and why; the LLM reruns and produces comparison output. Interpreting why the posteriors did or did not change is where the learning happens.

### Step 6: Report

The report has sections that are primarily descriptive and sections that require judgment. The division of labour follows the same principle as every other step.

**LLM drafts, student evaluates and revises:**
1. **Research question** (1–2 sentences) — The student formulated this in Step 1. The LLM can polish the wording; the student confirms accuracy.
2. **Method** — This describes decisions already made in Steps 2–4 (participant design, instrument, effect model, procedure). The LLM can draft this section directly from the design specifications and code. The student checks that the description is accurate and complete. Specify the LLM used, the random seed, and the number of participants.
3. **Results** — The LLM produced the posterior summaries, credible intervals, and visualisations in Step 5. The student organises them and describes the patterns. A description of what a posterior density plot shows is straightforward; the LLM can draft it, and the student checks it against the actual output.

**Student writes, LLM assists:**
4. **Discussion** — What do the patterns suggest? What assumptions drive the result? What would you change if designing a study with real participants? This is interpretive work. The LLM can help with language, but the reasoning is the student's.
5. **Limitations** — This section is not optional and is where the deepest thinking lives. At minimum, address:
   - The data reflects the effect model you built, not human psychology. Different assumptions produce different patterns.
   - The priors you chose influence the posteriors. If you used informative priors, the results partly reflect your prior beliefs, not just the data. If you used vague priors, the results are more data-driven but may be imprecise.
   - If you used an LLM to help set effect sizes or priors, those reflect the LLM's training data, which may encode stereotypes or inaccuracies.
   - The simulation cannot surprise you the way real data can. It confirms or disconfirms the internal logic of your model, not a hypothesis about the world.

## Connection to course learning outcomes

| CLO | How the simulation addresses it |
|---|---|
| 1 (Theoretical frameworks) | Students operationalise a framework (PERMA, SDT, broaden-and-build, etc.) by specifying what to measure, what effects to model, and justifying effect sizes from the literature. |
| 3 (Academic texts) | The report requires citing course readings to justify the research question, the effect model, and the interpretation. |
| 4 (Disciplinary terminology) | Design specifications, evaluation of generated items, effect-model justifications, and the report all require accurate use of terms (well-being, hedonic adaptation, self-efficacy, etc.). |
| 5 (Academic discussion) | The 5-minute presentation requires supporting claims with evidence from the simulated data. |
| 6 (Design and conduct inquiry) | The entire workflow. |
| 7 (Well-being practices) | Students who study a well-being practice (gratitude, mindfulness, etc.) must understand it well enough to specify its expected effects and evaluate whether the simulation output is plausible. |

## Provenance

This simulation method is adapted from an agent-based participant simulation workflow used in experimental linguistics (Reynolds, 2025, unpublished), where synthetic participant profiles with demographic characteristics generate judgment data for experimental design checking. The original uses Python and YAML profiles to produce 3,672 observations from 102 participants in a Latin-square design.

The methodological principle is the same: participant characteristics are defined explicitly and separately from the effect model, making assumptions visible and the simulation reproducible. The key difference is epistemological: in the original, simulated data debugs experimental designs before collecting human data; here, it teaches the research workflow itself.
