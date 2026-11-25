# Match decision points across categories

Give each coverage entry a stable session ID. For each scan or batch of new findings, supply a short description per point naming the decision target and its applicable scope. Use the spec's terminology and include material distinctions such as actor, operation, lifecycle state, and exception. Leave out category names and statuses so a tentative classification cannot bias retrieval.

When there are points to compare, run `python3 "$skill_dir/scripts/decision_neighbors.py"` with JSON on standard input. Set `skill_dir` to the directory containing SKILL.md. Use the current descriptions of all recorded points as `known` (empty on the first scan). Give each `incoming` finding a unique temporary ID across both lists. The helper compares it with every known point and earlier findings in that batch.

```json
{
  "known": [{"id": "P1", "text": "Who can approve a refund before payment settles?"}],
  "incoming": [
    {"id": "N1", "text": "Which roles may authorize reimbursement before settlement?"},
    {"id": "N2", "text": "Who can approve a refund after payment settles?"}
  ]
}
```

Read `neighbors[incoming_id]` for up to three positively scoring IDs. Identical descriptions come first, followed by other candidates in descending cosine similarity for this batch. Check the source passages even for identical descriptions. In this example N1 can reuse P1 if “reimbursement” refers to the same operation and “settlement” to the same payment event. N2 needs its own ID if the rule can differ after settlement, even if the same role currently approves both.

- For a confirmed match, reuse the retained ID and add the supported category, goal, and facet links. Compare each finding with the retained point even when an earlier finding already points to that ID. Keep independently answerable decisions separate.
- Classify a new point from its combined evidence. If the passages disagree, assign Partial and send one candidate through the Step 2 fact gate. For a recorded point, preserve its status and dependencies while its resolution or hold rationale still applies. A contradiction with a recorded resolution reopens that ID for confirmation.
- A shortlist can miss a paraphrase. Check plausible matches from the coverage or request map even when their score is low or absent. If Python or the helper is unavailable, or the helper fails, continue with the same target-and-scope check directly.

The helper keeps vectors in memory. By default it computes TF-IDF over words, character trigrams, and comparison operators using Python's standard library. This mode ranks shared wording. When the project defines two terms as synonyms, use its canonical term in both descriptions and check the original wording when reviewing the match.

To retrieve paraphrases with learned embeddings, use a Python environment with `model2vec` installed and set `GRILL_ME_VECTOR_MODEL` to a local Model2Vec model directory suited to the spec's language. For English, one option is [potion-base-2M](https://huggingface.co/minishlab/potion-base-2M). The helper loads the configured model offline. If loading or encoding fails, or any vector is zero or non-finite, it scores the whole batch with TF-IDF so every pair uses the same scale. The output identifies the backend used.
