# Match decision points across categories

Give each coverage entry a stable session ID. For each scan or batch of new findings, supply a short description per point naming the decision target and its applicable scope. Use the spec's terminology and include material distinctions such as actor, operation, lifecycle state, and exception. Leave out category names and statuses so a tentative classification cannot bias retrieval.

Run `python3 "$skill_dir/scripts/decision_neighbors.py"` with JSON on standard input, where `skill_dir` is the directory containing this SKILL.md. Use the current descriptions of all recorded points as `known` (empty on the first scan). Give each `incoming` finding a fresh ID for comparison. The helper compares it with every known point and earlier findings in that batch. For example:

```json
{
  "known": [{"id": "P1", "text": "Who can approve a refund before payment settles?"}],
  "incoming": [
    {"id": "N1", "text": "Which roles may authorize reimbursement before settlement?"},
    {"id": "N2", "text": "Who can approve a refund after payment settles?"}
  ]
}
```

For each incoming ID, review the returned IDs in descending cosine similarity (up to three). Compare the underlying spec passages. Would one answer settle both decisions for the same people under the same conditions? In this example N1 can reuse P1 if the spec uses “reimbursement” for the same operation. N2 still needs a separate decision if the rule can differ after settlement.

- For a confirmed match, reuse the original ID, category, status, dependencies, and goal links. Associate any additional goals or facets with that point. If another category covers it, refer to the same ID there and count the decision once. When a match is to an earlier incoming finding, follow it to the retained ID.
- Keep independently answerable decisions separate. Route conflicting evidence about the same decision through the existing conflict-confirmation flow. Similarity alone cannot settle a point, establish a dependency, or discard a question.
- A shortlist can miss a paraphrase. Check plausible matches from the coverage or request map even when their score is low or absent. If Python is unavailable, use the same target-and-scope check directly.

The helper keeps vectors in memory. By default it uses word and character TF-IDF vectors with Python's standard library. This mode ranks shared wording. When the project defines two terms as synonyms, use its canonical term in both descriptions and check the original wording when reviewing the match.

To retrieve paraphrases with learned embeddings, use a Python environment with `model2vec` installed and set `GRILL_ME_VECTOR_MODEL` to a local Model2Vec model directory suited to the spec's language. For English, one option is [potion-base-2M](https://huggingface.co/minishlab/potion-base-2M). The helper loads the configured model offline. Its output identifies the backend used, including a fallback to TF-IDF if the model cannot load.
