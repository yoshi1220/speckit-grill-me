# SpecKit Grill With Docs（base）

Serena に依存せず、Spec Kit の機能仕様を徹底的に明確化しながら、確定したプロジェクト横断の用語・ドメイン知識・設計判断を通常の Markdown 文書へ同期する Skill です。

## 標準のドキュメント配置

利用先プロジェクトで別の正準保存先が明示されていない場合は、次の配置を使用します。

```text
docs/domain_knowledge/
├── CONTEXT.md
├── <kebab-case-domain-topic>.md
└── adr/
    └── 0001-<kebab-case-decision>.md
```

利用先プロジェクトが別の正準知識ルートを指定している場合は、その既存の入口ファイルと ADR 配置規約に従います。規約がなければ、入口を `<knowledge-root>/CONTEXT.md`、ADR を `<knowledge-root>/adr/` に配置します。

- `CONTEXT.md` は知識ベースの入口です。プロジェクト固有の正準用語、概念の境界、避ける同義語を簡潔に保持し、実装詳細や feature 仕様は混ぜません。見出しは利用先プロジェクトの文書言語と規約に合わせます。
- 個別の Markdown ファイルは、複数の境界、不変条件、業務ルールを 1〜2 文では正確に表せない場合だけ作成します。判断に迷う場合は `CONTEXT.md` に留めます。
- 個別文書を作成した場合は、`CONTEXT.md` から相対リンクします。
- 覆しにくく、文脈なしでは意外で、実在する代替案から選んだ決定だけを `adr/` へ記録します。
- feature 固有の要件は `spec.md`、feature を超えて通用する正準知識はこのディレクトリへ書き分けます。

この分離は Matt Pocock の [domain-modeling](https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling) が採用する「簡潔な用語集」と「必要なときだけ作る ADR」を参考にしつつ、保存先を `docs/domain_knowledge/` に統一したものです。

## 依存関係

- macOS または Linux
- Bash
- `.specify/` を含む Spec Kit プロジェクト
- 同じ親ディレクトリにある `speckit-grill-me` Skill

Serena、Serena MCP、`.serena/` は不要です。
