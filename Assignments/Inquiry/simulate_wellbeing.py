#!/usr/bin/env python3
"""
Reference simulation for GPSE 100 Mini Inquiry Project.

Generates synthetic survey responses from participant profiles.
Students adapt the effect model (compute_base_rating) to match
their research question, or have an LLM rewrite it.

Adapted from Reynolds (2025), agent-based participant simulation
for experimental linguistics.

Usage:
    python3 simulate_wellbeing.py --seed 42 --output results.csv
"""

import csv
import yaml
import numpy as np
from pathlib import Path
import argparse


def load_participants(participants_dir="participants"):
    """Load participant profiles from YAML files."""
    participants = []
    for yaml_file in sorted(Path(participants_dir).glob("*.yaml")):
        with open(yaml_file) as f:
            participants.append(yaml.safe_load(f))
    return participants


def load_items(items_file="items/survey_items.csv"):
    """Load survey items from CSV."""
    items = []
    with open(items_file) as f:
        for row in csv.DictReader(f):
            items.append(row)
    return items


# ── Effect model ─────────────────────────────────────────────
#
# THIS IS THE SECTION TO ADAPT. Each function below encodes an
# assumption about how participant characteristics influence
# survey responses. Change these to match your research question.
#
# The reference version models a gratitude-practice inquiry:
# participants who practise daily gratitude journaling rate
# well-being items higher, but this effect is moderated by
# cultural background.

def compute_base_rating(item, participant):
    """
    Compute base rating for one participant on one item.

    Returns a continuous value on the 1-7 scale before noise.
    Students: this function IS your effect model. Every number
    here is an assumption you must justify in your report.
    """
    # Grand mean: moderate well-being
    base = 4.2

    # ── Construct effect ─────────────────────────────────────
    # Gratitude items get a boost from gratitude practice
    practice = participant.get("gratitude_practice", "none")
    construct = item.get("construct", "")

    if practice == "daily_journaling" and construct == "gratitude":
        base += 0.8  # Main effect of gratitude practice
    elif practice == "daily_journaling" and construct == "satisfaction":
        base += 0.4  # Smaller spillover to life satisfaction

    # ── Cultural-background moderation ───────────────────────
    # Collectivist cultural backgrounds: smaller individual-
    # practice effect (assumption — justify from readings)
    background = participant.get("cultural_background", "")
    collectivist_markers = ["Korean", "Japanese", "Chinese", "Vietnamese"]

    if any(m in background for m in collectivist_markers):
        if practice == "daily_journaling":
            base -= 0.3  # Moderating effect

    # ── Age effect ───────────────────────────────────────────
    age = participant.get("age", 30)
    base += (age - 30) * -0.005  # Slight negative age trend

    # ── Wellbeing baseline ───────────────────────────────────
    baseline_map = {"low": -0.6, "moderate": 0.0, "high": 0.5}
    baseline = participant.get("wellbeing_baseline", "moderate")
    base += baseline_map.get(baseline, 0.0)

    # ── Reverse scoring ──────────────────────────────────────
    if item.get("reverse_scored", "").lower() in ("true", "yes", "1"):
        base = 8 - base  # Flip on the 1-7 scale

    return base


# ── Simulation engine (usually no need to change below) ──────

def generate_rating(item, participant, rng):
    """Generate one rating with participant and residual noise."""
    base = compute_base_rating(item, participant)

    # Participant-level effect: consistent across items
    p_rng = np.random.default_rng(participant.get("random_seed", 42))
    participant_effect = p_rng.normal(0, 0.7)

    # Residual noise: varies per trial
    residual = rng.normal(0, 0.6)

    rating = int(np.clip(np.round(base + participant_effect + residual), 1, 7))
    return rating


def run_simulation(participants, items, seed=42):
    """Run all participants through all items."""
    rng = np.random.default_rng(seed)
    observations = []

    for participant in participants:
        for item in items:
            rating = generate_rating(item, participant, rng)
            obs = {
                "participant_id": participant["participant_id"],
                "item_id": item["item_id"],
                "item_text": item.get("item_text", ""),
                "construct": item.get("construct", ""),
                "reverse_scored": item.get("reverse_scored", "false"),
                "rating": rating,
            }
            # Copy all participant characteristics into the row
            for key in participant:
                if key not in ("random_seed",):
                    obs.setdefault(key, participant[key])
            observations.append(obs)

    return observations


def save_results(observations, output_file):
    """Write observations to CSV."""
    if not observations:
        print("No observations to save.")
        return
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=observations[0].keys())
        writer.writeheader()
        writer.writerows(observations)
    print(f"Saved {len(observations)} observations to {output_file}")


def print_summary(observations):
    """Print basic summary statistics."""
    from collections import defaultdict

    by_construct = defaultdict(list)
    by_practice = defaultdict(list)

    for obs in observations:
        by_construct[obs["construct"]].append(obs["rating"])
        key = f"{obs.get('gratitude_practice', 'unknown')}_{obs['construct']}"
        by_practice[key].append(obs["rating"])

    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)

    print(f"\nTotal observations: {len(observations)}")

    print("\nMean rating by construct:")
    for construct in sorted(by_construct):
        ratings = by_construct[construct]
        print(f"  {construct:20s}  M = {np.mean(ratings):.2f}  SD = {np.std(ratings):.2f}  N = {len(ratings)}")

    print("\nMean rating by practice × construct:")
    for key in sorted(by_practice):
        ratings = by_practice[key]
        print(f"  {key:40s}  M = {np.mean(ratings):.2f}  N = {len(ratings)}")

    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="Simulate well-being survey responses"
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="results.csv")
    parser.add_argument("--participants-dir", default="participants")
    parser.add_argument("--items-file", default="items/survey_items.csv")
    args = parser.parse_args()

    participants = load_participants(args.participants_dir)
    print(f"Loaded {len(participants)} participants")

    items = load_items(args.items_file)
    print(f"Loaded {len(items)} survey items")

    observations = run_simulation(participants, items, seed=args.seed)
    print_summary(observations)
    save_results(observations, args.output)


if __name__ == "__main__":
    main()
