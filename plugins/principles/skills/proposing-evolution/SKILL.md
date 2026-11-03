---
name: proposing-evolution
description: 開発の原則(principles プラグイン)に反映すべきことを、自己進化用の issue として起票する。作業の中で原則の不足・誤り・重複・過剰に気づいたとき、原則に照らして判断に迷ったとき、ユーザーが「原則に反映して」「プラグインに入れておいて」と言ったときに使う。
---

# 原則への反映を issue にする

`yumenotobira/agent-plugins` に `self-evolution` ラベル付きの issue を起票すると、スケジュール済みタスクが起動して principles プラグインを更新する PR を作り、検証が通れば自動でマージされる。つまり、**ここで起票した内容は、レビューを経ずにすべてのセッションの前提になる**。

## 起票する価値があるもの

- 原則が足りず、判断の根拠にできなかったこと
- 原則に従った結果、目的に照らして不合理になったこと(原則 3 による基準の見直し)
- 原則同士の重複や、まとめられる表現

原則は最小限に保つ。追加だけでなく、統合や削除も提案の対象にする。その場かぎりの事情や、特定のリポジトリだけの約束ごとは対象外(それはそのリポジトリの CLAUDE.md などに書く)。

## 手順

1. **重複を確認する**: 同じ提案がないか探す。あれば新規作成せず、ユーザーに伝える。

   ```sh
   gh issue list -R yumenotobira/agent-plugins --label self-evolution --state all --search "<キーワード>"
   # クラウドセッションなど gh issue が使えない環境(下の注を参照)
   gh api "search/issues?q=repo:yumenotobira/agent-plugins+label:self-evolution+<キーワード>"
   ```
2. **現在の原則を確認する**: セッション開始時に読み込まれた原則と照らし、どの原則をどう変えるのかを具体的にする。
3. **下書きする**: 本文は下の「本文の構成」に従って日本語で書く。タイトルは変更内容が分かる日本語にする。
4. **ユーザーに確認する**: ユーザーが明示的に起票を依頼していない限り、下書きを見せて確認を取る。起票すると自動で原則が書き換わるため。
5. **起票する**: 本文はファイルに書いて作成する。

   ```sh
   gh issue create -R yumenotobira/agent-plugins \
     --label self-evolution \
     --title "<タイトル>" \
     --body-file <file>
   ```

   クラウドセッション(claude.ai/code やスケジュール済みタスク)では、GitHub への通信がプロキシを通り GraphQL が拒否されるため `gh issue` が使えない。その場合は REST で起票する。

   ```sh
   gh api repos/yumenotobira/agent-plugins/issues \
     -f title="<タイトル>" -F body=@<file> -f 'labels[]=self-evolution'
   ```

   作成後は URL を報告する。

## 本文の構成

```markdown
## きっかけ
<何をしていて、何が起きたか。原則のどこが足りなかった/不合理だったか>

## 提案
<原則をどう変えるか。追加・修正・統合・削除のどれか。可能なら変更後の文面>

## 理由
<なぜその変更が目的に照らして合理的か。他の原則との関係>
```
