#!/bin/sh
# SessionStart: task-principles スキルの本文（frontmatter を除く）をコンテキストに読み込ませる。
echo "以下は principles プラグインが読み込んでいる、タスク遂行の原則である。すべてのタスクでこの原則に従う。"
awk 'n >= 2 { print } /^---$/ && n < 2 { n++ }' "${CLAUDE_PLUGIN_ROOT}/skills/task-principles/SKILL.md"
