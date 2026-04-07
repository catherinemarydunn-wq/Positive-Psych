# LLM-Based Participant Simulation for the Mini Inquiry Project

## Purpose

This document proposes a methodology for the Mini Inquiry Project (course learning outcome [CLO] 6): LLM-based participant simulation. Students build a simulation that generates synthetic survey responses, analyse the output using Bayesian statistics, and report on the results. The method teaches the full research workflow (operationalisation, measurement, simulation, analysis, interpretation) without requiring ethics approval, participant recruitment, or data collection infrastructure.

The core principle throughout is that **students make design decisions and the large language model (LLM) handles execution**. At every step, the student specifies what and why; the LLM generates profiles, writes code, runs analyses, and drafts descriptive prose. The student evaluates LLM output and provides the interpretation.

A reference Python script (`simulate_wellbeing.py`) is included. If the LLM tool students use supports sub-agent orchestration (e.g., GitHub Copilot CLI's `/fleet` command), the entire workflow from profile generation through analysis can be dispatched as parallel subtasks from a single design specification.

## What this is (and what it is not)

**This is a methods exercise.** The simulated data reflects modelling assumptions that the student makes explicit, not the psychology of actual humans. Any "findings" are hypotheses worth testing with real participants, not conclusions about human well-being.

**This is not empirical research on human psychology.** The word "inquiry" is deliberate. Students are not conducting experiments, and the report should not claim to have discovered facts about people. The correct framing is: "Given these modelling assumptions, the simulation produced these patterns. Here is what that suggests we should investigate with real participants."

### Learning targets

- Translating a research question into measurable variables
- Specifying a participant population: what characteristics matter, what their distributions should look like, and why
- Specifying what constructs to measure and evaluating whether generated survey items actually measure them
- Specifying effect assumptions and justifying their direction and size from course readings
- Specifying prior beliefs about effects, justifying the choice of informative vs. vague priors, and evaluating prior predictive output for plausibility
- Deciding what analytical questions to ask and interpreting posterior probabilities and credible intervals
- Evaluating and revising LLM-generated output at every stage (profiles, items, code, analysis, prose)
- Articulating the limitations of a data source honestly

## The workflow

The workflow has six steps. In each, the left column is the student's intellectual contribution; the right column is what the LLM executes.

| Step | Student decides | LLM executes |
|------|----------------|--------------|
| 1. Research question | What to investigate and why | — |
| 2. Participant design | Characteristics, distributions, sample size, rationale | Generates YAML profiles |
| 3. Instrument design | Constructs, item count, scale, reverse scoring, rationale | Generates survey items as CSV |
| 4. Simulation | Effect directions, sizes, justifications from readings | Writes/adapts Python; runs simulation |
| 5. Analysis | Priors, prior predictive evaluation, comparisons, sensitivity | Fits Bayesian model; produces checks, posteriors, plots |
| 6. Report | Discussion reasoning, limitations | Drafts Method/Results from artifacts |

At every step, the student reviews and revises LLM output.

### Step 1: Research question

Students start with a question that connects a positive psychology concept from the course to a characteristic that varies across people.

**Examples:**
- Does the relationship between gratitude practice and reported well-being differ by cultural background?
- Do younger and older adults report different levels of flow in academic vs. leisure activities?
- Does growth mindset predict different responses to setback scenarios across education levels?

The question must be specific enough to operationalise. "Is happiness good?" is not a research question. "Do people who score higher on hedonic adaptation report lower satisfaction with repeated positive events?" is.

### Step 2: Participant design

Students specify the population; the LLM generates the profiles. Profiles are stored as individual YAML (Yet Another Markup Language) files, a human-readable data format.

**What students specify:**
- **Sample size.** There is no practical cost to generating hundreds of participants. Larger samples produce narrower credible intervals (more precise estimates). Students should ask the LLM what sample size gives useful precision for the effect size they expect.
- **Characteristics and distributions.** Which demographic and psychological variables matter for the research question? What should their distributions look like?
- **Independent variable.** How should participants be split across conditions?

**Example specification:**

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

**Where the learning happens:** Deciding that cultural background should be split into equal thirds (rather than proportional to the actual student body) is a design choice that needs justifying. Deciding that well-being baseline should be 20/60/20 is a modelling assumption. These are the decisions the student defends. Generating 300 YAML files from that specification is mechanical.

### Step 3: Instrument design

Students specify what to measure, how, and why. The LLM generates the items. The study design is a survey: participants respond to Likert-scale items measuring one or more psychological constructs.

**What students specify:**
- **Constructs.** Which psychological constructs does the research question require? (e.g., gratitude, life satisfaction, hedonic adaptation). Justified from course readings.
- **Scale.** What response format? (e.g., 1–7 Likert, where 1 = strongly disagree and 7 = strongly agree). Why that scale?
- **Item count.** How many items per construct? Students can ask the LLM what is standard for the constructs they are measuring.
- **Reverse-scored items.** At least some. These check that the model produces internally consistent responses.
- **Item quality constraints.** Each item should measure one thing. Items should be at a language level the simulated population would understand.

**Example specification:**

> Generate a survey instrument as a comma-separated values (CSV) file with columns for item_id, item_text, construct, and reverse_scored. I need items measuring two constructs: gratitude (8 items, including 2 reverse-scored) and life satisfaction (6 items, including 2 reverse-scored). Use a 1–7 Likert scale. Items should be written at a B2 English level. Base the items on established instruments (GQ-6 for gratitude, SWLS for satisfaction) but do not copy them verbatim.

**Where the learning happens:** Deciding to measure gratitude and satisfaction (rather than flow and meaning) follows from the research question. Deciding on 8 + 6 items with reverse scoring is a methodological choice. Writing 14 item stems is mechanical. Reviewing the generated items and revising any that are unclear, double-barrelled, or off-construct — that evaluation is the skill being practised.

### Step 4: Simulation

Students give the LLM their full design specification and have it handle profile generation, script writing, and execution. If the LLM tool supports sub-agents (e.g., Copilot CLI's `/fleet`), these can run as parallel subtasks.

**Two starting points:**

**Option A:** Adapt the reference script (`simulate_wellbeing.py`). The effect model section (`compute_base_rating`) is clearly marked as the part to modify.

**Option B:** Have the LLM write a script from scratch, using the reference script as an architectural example.

**Either way, the script should:**
1. Load participant profiles from YAML files
2. Load survey items from the CSV file
3. Compute a base rating for each participant–item pair using explicit effect assumptions
4. Add participant-level random effects and residual noise
5. Constrain ratings to the scale
6. Output a CSV file with one row per participant–item pair

**Where the learning happens:** Deciding that gratitude practice should add ~0.8 to satisfaction ratings is a claim about the world that the student justifies from course readings (e.g., "Emmons & McCullough, 2003, found a medium effect"). Deciding that collectivist cultural background moderates that effect is a theoretical commitment. The LLM translates these into code. The student reviews the generated code to confirm it implements what they specified.

**Reproducibility:** Same random seed must produce identical output. Students record the seed, the LLM and version used, and any prompts given.

### Step 5: Analysis

The simulation produces a CSV file. Students specify what they want to know; the LLM produces the analysis. The analysis follows a Bayesian workflow: specify priors, check that the priors are sensible, fit the model, check that the model's predictions match the data, then interpret and probe.

#### Why Bayesian

Frequentist statistics answer a question nobody is asking ("If there were no effect, how often would we see data this extreme?"). Bayesian statistics answer the actual question ("Given the data, how probable is it that gratitude practice increases satisfaction, and by how much?"). For a methods exercise where students are learning to reason about evidence, Bayesian posterior probabilities are more honest and more intuitive. The p-value framework actively misleads novices ("not significant" ≠ "no effect"), and introducing it without the context to use it properly would be irresponsible. Bayesian credible intervals say what students think confidence intervals say.

Bayesian analysis also fits the design/execute split cleanly. Prior specification is a design decision: the student decides what they expect and why. The mechanics (Markov chain Monte Carlo [MCMC] sampling, convergence checking) are the LLM's job. The student never needs to understand the sampling algorithm.

#### The Bayesian workflow

The analysis has five stages. The LLM executes all of them; the student specifies and evaluates.

**1. Specify priors — what they expect before seeing the data.**

For each effect in the model, students specify a prior belief about its direction and size, justified from course readings.

- Example: "Based on Emmons & McCullough (2003), I expect gratitude practice to have a positive effect on satisfaction of roughly 0.5–1.0 points on a 7-point scale. I'll use a normal prior centred on 0.7 with standard deviation (SD) 0.3."
- Example: "I'm genuinely uncertain whether cultural background moderates the gratitude effect. I'll use a prior centred on 0 with SD 0.5."
- A prior that says "I don't know" (wide, centred on zero) is legitimate. A prior that says "I'm fairly sure" (narrow, off zero) is also legitimate if justified. The student explains which and why.

Students also specify the model structure: outcome variable (e.g., satisfaction rating), predictors (e.g., gratitude practice, cultural background, their interaction). The LLM chooses the implementation (PyMC, Stan, or a simpler conjugate approach for straightforward designs).

**2. Prior predictive check — do the priors produce plausible predictions?**

Before fitting the model to any data, the LLM generates predictions from the priors alone and visualises them. The student evaluates whether these predictions are plausible.

If the prior predictive distribution shows satisfaction scores below 1 or above 7, or predicts that most participants would rate at ceiling, the priors need adjusting. This is a concrete, visual sanity check that forces the student to confront what their priors actually mean in terms of the outcome they are modelling.

**Where the learning happens:** This is model criticism *before* seeing results. The student is asking "Do my assumptions, taken together, produce a world that makes sense?" This directly serves CLO 2 (critically evaluate empirical research) — if a published study used unreasonable assumptions, this is how one would detect it.

**3. Fit the model.**

The LLM fits the Bayesian regression to the simulation output. The student does not need to understand MCMC internals. The LLM reports posterior distributions of each effect, credible intervals (e.g., 89% CI), and the probability that each effect is in the expected direction.

**4. Posterior predictive check — do the model's predictions match the data?**

After fitting, the LLM generates predictions from the posterior and overlays them on the actual simulation data. The student evaluates whether the model captures the patterns in the data.

Since the data is simulated with known effects, this is partly a code-verification step: if the posterior predictions don't match the simulation output, something is wrong in either the simulation code or the model specification. But the visual comparison also builds the habit of checking model fit rather than blindly trusting output.

**5. Interpret and probe.**

Bayesian results produce statements like:

- "There is a 94% probability that gratitude practice increases satisfaction ratings (median effect: 0.72 points, 89% CI [0.38, 1.09])."
- "The probability that cultural background moderates the gratitude effect is 68%, with the moderation estimate centred near −0.25 (89% CI [−0.61, 0.14])."

**Where the learning happens:** The first statement suggests a fairly confident positive effect. The second suggests genuine uncertainty — the credible interval includes zero, so the data are compatible with no moderation. What would it take to resolve that uncertainty? A larger sample? A different operationalisation of "cultural background"? That reasoning is the student's.

**Sanity checks.** Are the posterior effect sizes close to what the student specified in the simulation? They should be, since the effects were built in. If the posteriors recover the assumed effects, the model is working. If not, something is wrong in the code or model specification.

**Sensitivity analysis.** The most interesting analytical move is changing a prior or an effect assumption and rerunning. What if a sceptical prior (centred on zero) is used for the main effect? Does the posterior still show a positive effect, or does it collapse? What if the cultural moderation were twice as large? The student specifies what to vary and why; the LLM reruns and produces comparison output. Interpreting why the posteriors did or did not change is where the learning happens.

### Step 6: Report

The report has sections that are primarily descriptive and sections that require judgment.

**LLM drafts, student evaluates and revises:**
1. **Research question** (1–2 sentences) — formulated in Step 1; the LLM can polish wording.
2. **Method** — describes decisions already made in Steps 2–4. The LLM drafts directly from the design specifications and code. The student checks accuracy and completeness. Should specify the LLM used, the random seed, and the number of participants.
3. **Results** — the LLM produced the posterior summaries, credible intervals, predictive checks, and visualisations in Step 5. The student organises them and describes the patterns. The LLM can draft descriptions of what the plots show; the student checks against the actual output.

**Student writes, LLM assists with language:**
4. **Discussion** — What do the patterns suggest? What assumptions drive the result? What would change with real participants? This is interpretive work.
5. **Limitations** — not optional; this is where the deepest thinking lives. At minimum:
   - The data reflects the effect model the student built, not human psychology. Different assumptions produce different patterns.
   - The priors influence the posteriors. Informative priors mean the results partly reflect prior beliefs, not just data. Vague priors are more data-driven but may be imprecise.
   - If the LLM helped set effect sizes or priors, those reflect its training data, which may encode stereotypes or inaccuracies.
   - The simulation cannot surprise the way real data can. It confirms or disconfirms the internal logic of the model, not a hypothesis about the world.

## Connection to course learning outcomes

| CLO | How the simulation addresses it |
|---|---|
| 1 (Theoretical frameworks) | Students operationalise a framework (PERMA, SDT, broaden-and-build, etc.) by specifying what to measure, what effects to model, and justifying effect sizes from the literature. |
| 2 (Critical evaluation) | Prior predictive checks and posterior predictive checks teach model criticism: evaluating whether assumptions produce plausible predictions, and whether a fitted model captures the data. |
| 3 (Academic texts) | The report requires citing course readings to justify the research question, the effect model, the priors, and the interpretation. |
| 4 (Disciplinary terminology) | Design specifications, evaluation of generated items, effect-model justifications, and the report all require accurate use of terms (well-being, hedonic adaptation, self-efficacy, etc.). |
| 5 (Academic discussion) | The 5-minute presentation requires supporting claims with evidence from the simulated data. |
| 6 (Design and conduct inquiry) | The entire workflow. |
| 7 (Well-being practices) | Students who study a well-being practice (gratitude, mindfulness, etc.) must understand it well enough to specify its expected effects and evaluate whether the simulation output is plausible. |

## Provenance

This simulation method is adapted from an agent-based participant simulation workflow used in experimental linguistics (Reynolds, 2025, unpublished), where synthetic participant profiles with demographic characteristics generate judgment data for experimental design checking. The original uses Python and YAML profiles to produce 3,672 observations from 102 participants in a Latin-square design.

The methodological principle is the same: participant characteristics are defined explicitly and separately from the effect model, making assumptions visible and the simulation reproducible. The key difference is epistemological: in the original, simulated data debugs experimental designs before collecting human data; here, it teaches the research workflow itself.
