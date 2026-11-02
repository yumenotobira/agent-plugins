# agent-plugins

自分用の Claude Code プラグインを管理する marketplace リポジトリ。

## 使い方

```
/plugin marketplace add yumenotobira/agent-plugins
/plugin install <plugin-name>@agent-plugins
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
