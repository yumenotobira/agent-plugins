# agent-plugins

自分用の Claude Code プラグインを管理する marketplace リポジトリ。

## 使い方

```
/plugin marketplace add yumenotobira/agent-plugins
/plugin install <plugin-name>@agent-plugins
```

## プラグイン一覧

| 名前 | 内容 |
|---|---|
| [git](plugins/git) | Git / GitHub を使った開発フローのスキル集（issue・PR の書き方など） |
| [principles](plugins/principles) | 開発の原則をセッションに読み込み、作業から得た気づきで原則を自己進化させる |

```
/plugin install git --marketplace yumenotobira/agent-plugins
```

## 構成

```
.claude-plugin/marketplace.json   # marketplace 定義（plugins 配列に登録）
plugins/<plugin-name>/
  .claude-plugin/plugin.json      # プラグインのメタデータ
  skills/ commands/ agents/ hooks/  # 必要なものだけ
```

## プラグインの追加

1. `plugins/<plugin-name>/` を作成
2. `.claude-plugin/marketplace.json` の `plugins` に追記:

   ```json
   { "name": "<plugin-name>", "source": "./plugins/<plugin-name>", "description": "..." }
   ```
3. `claude plugin validate .` で検証

## バージョン管理

`plugins/` 配下を変更した PR が main にマージされると、GitHub Actions（`.github/workflows/bump-versions.yml`）が変更のあったプラグインの `plugin.json` の `version` を上げて main に push する。

- デフォルトは patch。PR に `release:minor` / `release:major` ラベルを付けるとそのレベルで上げる
- `version` 未設定のプラグインは `0.1.0` が設定される
- `self-evolution` ラベルの PR は対象外（PR の中で自分で version を上げる。下記参照）

手元で実行する場合:

```sh
scripts/bump_versions.py --dry-run                 # origin/main...HEAD の変更を確認
scripts/bump_versions.py --level minor             # 変更のあったプラグインを minor bump
scripts/bump_versions.py --plugin foo --level major  # 指定プラグインを bump
```

## principles の自己進化

`principles` プラグインは、使いながら原則を更新していく。

1. 作業中に原則へ反映すべきことに気づいたら、`principles:proposing-evolution` スキルが `self-evolution` ラベル付きの issue を起票する（`.github/ISSUE_TEMPLATE/self-evolution.yml` から手で起票してもよい）
2. issue へのラベル付け（`issues.labeled`）を GitHub トリガーにしたスケジュール済みタスク（claude.ai/code/routines）が起動し、`.claude/skills/evolving/SKILL.md` の手順で原則を更新して version を上げ、`claude/` ブランチから PR を作る
3. `.github/workflows/self-evolution.yml` が検証し、次の条件をすべて満たせば squash マージする
   - 作成者が `yumenotobira`、head ブランチが `claude/`、`self-evolution` ラベル付き
   - 変更が `plugins/principles/**` と `.claude/skills/evolving/**` の中だけ
   - `plugins/principles/` を変えた場合は version が上がっている
4. marketplace の自動更新を ON にしている環境で、プラグインが更新される

条件を満たさない PR は自動マージされず、人のレビュー待ちとして残る。
