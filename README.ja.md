# SpecKit Grill Me

SpecKit Grill Me は、実装計画へ進む前に機能仕様の曖昧さと未決定事項を徹底的に解消する requirements elicitation skill です。設計上は `specify`と`plan` の間に置く specification convergence gate として機能します。

## 由来と帰属

このプロジェクトは、次の2つのMITライセンスプロジェクトを基にした独立プロジェクトです。

- [GitHub Spec Kit](https://github.com/github/spec-kit) の `/speckit-clarify` を、成果物・副作用の互換対象とし、macOS / Linux + Bash環境向けの代替として作成しています。
- [Matt Pocockのskills](https://github.com/mattpocock/skills) に含まれる [`grill-me`](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me) の、徹底的に質問して設計を研ぎ澄ます発想にインスパイアされています。

このプロジェクトはGitHubおよびMatt Pocockによる公式プロジェクトではなく、両者からの承認・提携を示すものではありません。

## バリエーション

- `japanese/base/speckit-grill-me` — 通常のファイル・コード・文書調査を使う、Serena非依存版
- `japanese/with_serena/speckit-grill-me` — Serenaのメモリ・シンボル調査を前提とする版

両版ともmacOS / Linux + Bashを対象とし、`.specify/`を含むSpec Kitプロジェクト構成を必要とします。

## `/speckit-clarify`との違い

|                | `/speckit-clarify` | `/speckit-grill-me`                                                                                                                                                                                                                                             |
| -------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 質問数         | 最大 5 問          | 上限なし                                                                                                                                                                                                                                                        |
| 進行単位       | 1 問ずつ順次       | フロンティア（いま聞ける質問の集合）単位のラウンド。ラウンド内も 1 問ずつ順に提示                                                                                                                                                                               |
| 回答形式       | 選択肢 or 5 語以内 | ラベル付き選択肢（A/B/C）＋無制限の自由記述。選択後も納得まで掘り下げ可                                                                                                                                                                                         |
| ラウンドの反復 | 1 回のスキャンのみ | 最初のスキャン（Step 1）で質問候補一覧を作り、ラウンドごとにその中からいま聞ける質問（フロンティア）を取り出して質問する。一覧に聞ける質問が残らなくなったら spec.md を読み直して曖昧さを再スキャン（Step 5）。フロンティアに新しい質問が出なくなるまで繰り返す |
| 終了条件       | 5 問 or 曖昧さ解消 | 全論点が Clear / Resolved / Outstanding / Deferred に確定 **かつ** ユーザーの納得の明示                                                                                                                                                                         |

## ライセンス

このプロジェクトは[MIT License](LICENSE)で提供します。

参照元のライセンスも確認済みです。

- GitHub Spec Kit — [MIT License](https://github.com/github/spec-kit/blob/main/LICENSE)、`Copyright GitHub, Inc.`
- mattpocock/skills — [MIT License](https://github.com/mattpocock/skills/blob/main/LICENSE)、`Copyright (c) 2026 Matt Pocock`

上記の帰属表示と、このリポジトリに含まれるMITライセンス本文を維持してください。
