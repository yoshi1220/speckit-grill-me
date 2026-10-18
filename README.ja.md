# SpecKit Grill Me

SpecKit Grill Me は、実装計画へ進む前に機能仕様の曖昧さと未決定事項を徹底的に解消する requirements elicitation skill です。設計上は `specify` と `plan` の間に置く specification convergence gate として機能します。

## 由来と帰属

このプロジェクトは、次の 2 つの MIT ライセンスプロジェクトを基にした独立プロジェクトです。

- [GitHub Spec Kit](https://github.com/github/spec-kit) の `speckit.clarify` を、成果物・副作用の互換対象とし、macOS / Linux + Bash 環境向けの代替として作成しています。
- [Matt Pocock の skills](https://github.com/mattpocock/skills) に含まれる [`grill-me`](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me) の、徹底的に質問して設計を研ぎ澄ます発想にインスパイアされています。

このプロジェクトは GitHub および Matt Pocock による公式プロジェクトではなく、両者からの承認・提携を示すものではありません。

## バリエーション

| 言語 | 調査・知識バックエンド | Skill | 用途 |
| --- | --- | --- | --- |
| 英語 | 通常ファイル | [`english/base/speckit-grill-me`](english/base/speckit-grill-me/) | 機能仕様の明確化 |
| 英語 | 通常ファイル | [`english/base/speckit-grill-with-docs`](english/base/speckit-grill-with-docs/) | 明確化と、既定では `docs/domain_knowledge/` への横断知識の保存 |
| 英語 | Serena | [`english/with_serena/speckit-grill-me`](english/with_serena/speckit-grill-me/) | Serena のメモリ・シンボル調査を使った明確化 |
| 英語 | Serena | [`english/with_serena/speckit-grill-with-docs`](english/with_serena/speckit-grill-with-docs/) | 明確化と Serena メモリへの確定知識の保存 |
| 日本語 | 通常ファイル | [`japanese/base/speckit-grill-me`](japanese/base/speckit-grill-me/) | 日本語での機能仕様の明確化 |
| 日本語 | 通常ファイル | [`japanese/base/speckit-grill-with-docs`](japanese/base/speckit-grill-with-docs/) | 明確化と通常の Markdown への横断知識の保存 |
| 日本語 | Serena | [`japanese/with_serena/speckit-grill-me`](japanese/with_serena/speckit-grill-me/) | Serena を使った日本語での明確化 |
| 日本語 | Serena | [`japanese/with_serena/speckit-grill-with-docs`](japanese/with_serena/speckit-grill-with-docs/) | 明確化と Serena メモリへの確定知識の保存 |

すべての版が macOS / Linux + Bash を対象とし、`.specify/` を含む Spec Kit プロジェクト構成を必要とします。`speckit-grill-with-docs` は同じ親ディレクトリにある `speckit-grill-me` も必要です。`with_serena` 版は Serena も必要です。

言語とバックエンドが異なる版でも同じ 2 つの Skill 名を使います。同じ Skill 探索ルートには、各 Skill 名につき 1 つの版だけをインストールしてください。各版は併用するものではなく、用途に応じて置き換える選択肢です。

## Community Extension

[`spec-kit-extension`](spec-kit-extension/) は、英語・Serena 非依存版を Spec Kit Community Extension `grill` として配布します。リリース 1.0.2 では次の 2 コマンドを提供します。

- `speckit.grill.me` — 仕様の徹底的な明確化
- `speckit.grill.with-docs` — 明確化と正準 Markdown 知識の同期

エージェントごとの呼び出し形式、専用リリース ZIP からのインストール、リリース情報は [Extension README](spec-kit-extension/README.md) を参照してください。

## `speckit.clarify` との違い

|                | `speckit.clarify`  | `speckit-grill-me`                                                                                                                                                                                                                                             |
| -------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 質問数         | 最大 5 問          | 上限なし                                                                                                                                                                                                                                                        |
| 進行単位       | 1 問ずつ順次       | フロンティア（いま聞ける質問の集合）単位のラウンド。ラウンド内も 1 問ずつ順に提示                                                                                                                                                                               |
| 回答形式       | 選択肢 or 5 語以内 | ラベル付き選択肢（A/B/C）＋無制限の自由記述。選択後も納得まで掘り下げ可                                                                                                                                                                                         |
| ラウンドの反復 | 1 回のスキャンのみ | 最初のスキャン（Step 1）で質問候補一覧を作り、ラウンドごとにその中からいま聞ける質問（フロンティア）を取り出して質問する。一覧に聞ける質問が残らなくなったら spec.md を読み直して曖昧さを再スキャン（Step 5）。フロンティアに新しい質問が出なくなるまで繰り返す |
| 終了条件       | 5 問 or 曖昧さ解消 | 全論点が Clear / Resolved / Outstanding / Deferred に確定 **かつ** ユーザーの納得の明示                                                                                                                                                                         |

## ライセンス

このプロジェクトは [MIT License](LICENSE) で提供します。

参照元のライセンスも確認済みです。

- GitHub Spec Kit — [MIT License](https://github.com/github/spec-kit/blob/main/LICENSE)、`Copyright GitHub, Inc.`
- mattpocock/skills — [MIT License](https://github.com/mattpocock/skills/blob/main/LICENSE)、`Copyright (c) 2026 Matt Pocock`

上記の帰属表示と、このリポジトリに含まれるMITライセンス本文を維持してください。
