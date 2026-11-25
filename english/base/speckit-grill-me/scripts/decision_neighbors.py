"""Find decision points to review for possible duplication. Read one JSON batch on stdin."""

import json
import math
import os
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path


# Question scaffolding is frequent in decision descriptions but says little about scope.
QUESTION_WORDS = frozenset("a an the is are do does should can may what when where which who how".split())


def read_batch(payload):
    if not isinstance(payload, dict):
        raise ValueError("expected an object with known and incoming lists")
    ids = []
    texts = []
    seen = set()
    for group in ("known", "incoming"):
        rows = payload.get(group)
        if not isinstance(rows, list):
            raise ValueError(f"{group} must be a list")
        for row in rows:
            if not isinstance(row, dict):
                raise ValueError(f"expected a point in {group}")
            point_id, text = row.get("id"), row.get("text")
            if not isinstance(point_id, str) or not point_id.strip() or point_id in seen:
                raise ValueError("each point needs a unique nonempty id")
            if not isinstance(text, str) or not text.strip():
                raise ValueError(f"missing decision text for {point_id}")
            ids.append(point_id)
            texts.append(text)
            seen.add(point_id)
    return ids, texts, len(payload["known"])


def lexical_scores(texts):
    """Build unit TF-IDF vectors over words and within-word character trigrams."""
    counts = []
    frequency = Counter()
    for text in texts:
        terms = Counter()
        for word in re.findall(r"[^\W_]+", unicodedata.normalize("NFKC", text).casefold()):
            if word in QUESTION_WORDS:
                continue
            terms[("word", word)] += 1
            for start in range(len(word) - 2):
                terms[("gram", word[start:start + 3])] += 1
        counts.append(terms)
        frequency.update(terms.keys())

    vectors = []
    for terms in counts:
        weights = {
            term: (1 + math.log(tf)) * (1 + math.log((1 + len(texts)) / (1 + frequency[term])))
            for term, tf in terms.items()
        }
        norm = math.sqrt(sum(w * w for w in weights.values()))
        vectors.append({term: w / norm for term, w in weights.items()})

    def score_previous(i):
        query = vectors[i]
        return [sum(w * query.get(term, 0.0) for term, w in v.items()) for v in vectors[:i]]

    return score_previous


def scorer(texts):
    model_dir = os.environ.get("GRILL_ME_VECTOR_MODEL")
    if model_dir and texts:
        try:
            path = Path(model_dir).expanduser().resolve(strict=True)
            if not path.is_dir():
                raise ValueError("expected a local model directory")
            os.environ["HF_HUB_OFFLINE"] = "1"
            from model2vec import StaticModel

            model = StaticModel.from_pretrained(path, normalize=True)
            vectors = model.encode(texts)
            return "model2vec", lambda i: vectors[:i] @ vectors[i]
        except Exception as error:
            print(f"Local embeddings unavailable ({error}). Using TF-IDF.", file=sys.stderr)
    return "tf-idf", lexical_scores(texts)


def neighbors(payload):
    ids, texts, first_incoming = read_batch(payload)
    backend, score_previous = scorer(texts)
    results = {}
    for i in range(first_incoming, len(ids)):
        scores = score_previous(i)
        matches = sorted(range(i), key=lambda j: -scores[j])
        results[ids[i]] = [
            {"id": ids[j], "cosine": round(float(scores[j]), 5)}
            for j in matches[:3] if scores[j] > 0
        ]
    return {"backend": backend, "neighbors": results}


if __name__ == "__main__":
    try:
        print(json.dumps(neighbors(json.load(sys.stdin)), ensure_ascii=False))
    except ValueError as error:
        sys.exit(f"Invalid decision batch: {error}")
