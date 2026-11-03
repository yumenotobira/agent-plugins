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
| [git](plugins/git) | Git / GitHub を使った開発フローのスキル集（issue の書き方など） |

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

手元で実行する場合:

```sh
scripts/bump_versions.py --dry-run                 # origin/main...HEAD の変更を確認
scripts/bump_versions.py --level minor             # 変更のあったプラグインを minor bump
scripts/bump_versions.py --plugin foo --level major  # 指定プラグインを bump
```
