# Match decision points across categories

Use the same `helper` and `session` as in [Using the decision graph](decision-graph.md). Send one batch of findings on standard input. Give each finding a temporary ID such as `N1` and describe its decision target and scope in the spec's language. Include relevant actors, operations, conditions and exceptions.

```bash
python3 -B "$helper" match "$session" <<'JSON'
[
  {"id":"N1","text":"Which roles may authorize reimbursement before payment settles?"},
  {"id":"N2","text":"Who can approve a refund after payment settles?"}
]
JSON
```

The helper reads every stored node’s target and scope from the current GraphML revision. It compares each finding with those nodes and with earlier findings in the batch, including on the first scan of an empty graph. The output contains the revision, the vector backend and up to three positively scoring IDs per finding, ranked by cosine similarity. Matching leaves the graph intact.

Review the original passages for the shortlisted and other plausible matches. For example, if `D001` covers refund approval before settlement, `N1` can reuse it if the spec uses “reimbursement” for that operation. Keep `N2` separate if its rule can differ after settlement.

- For a confirmed match, reuse the stable graph ID and retain all applicable reporting categories and request-map links. Keep the recorded status and dependencies while the evidence still supports them. Resolve a reference to an earlier incoming finding to its retained graph ID. Allocate a new decision ID only for an independent decision.
- Apply the reconciled changes with the revision returned by `match`. A batch that only confirms existing entries needs no write. If the revision is stale, rerun the match and reconcile with the latest graph. Route conflicting evidence about an existing decision through conflict confirmation on its original ID. Only confirmed decision relationships belong in the dependency graph.

The helper keeps vectors in memory. By default it uses word and character TF-IDF vectors with Python's standard library. This mode ranks shared wording. When the project defines two terms as synonyms, use its canonical term in both descriptions and check the original wording when reviewing the match.

To retrieve paraphrases with learned embeddings, use a Python environment with `model2vec` installed and set `GRILL_ME_VECTOR_MODEL` to a local Model2Vec model directory suited to the spec's language. For English, one option is [potion-base-2M](https://huggingface.co/minishlab/potion-base-2M). The helper loads the configured model offline. Its output identifies the backend used, including a fallback to TF-IDF if the model cannot load.
