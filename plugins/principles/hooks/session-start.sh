#!/bin/sh
# SessionStart: 原則をセッションのコンテキストに読み込ませる。
cat "${CLAUDE_PLUGIN_ROOT}/PRINCIPLES.md"
cat <<'EOF'

以上は principles プラグインが読み込んでいる開発の原則である。
作業の中で、この原則に追加・修正・統合・削除すべきことに気づいたら、principles:proposing-evolution スキルで issue にする。
EOF
