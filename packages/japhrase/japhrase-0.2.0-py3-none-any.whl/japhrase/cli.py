"""
japhrase コマンドラインインターフェース

CLIから各種分析機能を実行するメインエントリーポイント
"""

import click
import sys
from pathlib import Path
from typing import Optional, List
import logging
import pandas as pd

from .extracter import PhraseExtracter, PRESETS
from .writing_assistant import (
    KWICAnalyzer,
    AbstractBodyChecker,
    HabitDetector,
    RevisionHeatmap,
    RankingTrajectory
)
from .writing_tools import EditorConfigGenerator, SelfRecommender
from .workflow import WorkflowDefinition, WorkflowEngine
from .use_cases import WritingWorkflow
from .config import JaphraseConfig
from .checker import QualityChecker
from .utils import read_file, export_to_csv, export_to_json

logger = logging.getLogger(__name__)


# ルートグループ
@click.group(invoke_without_command=True)
@click.version_option()
@click.pass_context
def cli(ctx):
    """
    japhrase - 日本語フレーズ抽出・分析プラットフォーム

    文章品質と執筆効率を向上させるための高度なNLP分析ツールです。

    【コア機能】
      - フレーズ自動抽出 - PMI/エントロピー基盤の統計分析
      - 表記ゆれ検出 - 表現の重複と多様性の分析
      - 執筆習癖検出 - パーソナルスタイルの可視化
      - あらすじ乖離度 - 本文との整合性チェック
      - セルフリコメンデーション - 過去原稿との関連性発見

    【使用シーン】
      学位論文・学術論文、小説推敲、ブログ最適化、SNS投稿統一、
      編集者向けチェック、執筆ワークフロー自動化

    【開始方法】
      japhrase COMMAND [OPTIONS] [ARGS]
      japhrase --help (詳細なヘルプを表示)

    【主要コマンド】
      extract       テキストから自動的にフレーズを抽出
      stats         フレーズ統計を計算（JSON/CSV出力対応）
      analyze       統合分析レポートを生成
      use-case      ユースケース別ワークフロー実行
      workflow      YAMLワークフロー定義を実行

    詳細は各コマンドの --help を参照してください。
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


# ===== コマンド: extract =====
@cli.command()
@click.argument('input_file', type=click.Path(exists=True), metavar='INPUT_FILE')
@click.option('-o', '--output', type=click.Path(), help='出力ファイルパス (CSV/JSON形式で保存)')
@click.option('--config', type=click.Path(exists=True), help='設定ファイル (.japhrase.toml / .japhrase.yml)')
@click.option('--preset', type=click.Choice(list(PRESETS.keys())),
              help=f'パラメータプリセット ({", ".join(PRESETS.keys())} から選択)')
@click.option('--min-count', type=int, help='最小出現回数フィルタ (デフォルト: 6)')
@click.option('--max-length', type=int, help='最大フレーズ長フィルタ (デフォルト: 16)')
@click.option('--format', type=click.Choice(['csv', 'json', 'table']), default='table',
              help='出力形式: table=コンソール表示, csv/json=ファイル保存用')
@click.option('-v', '--verbose', is_flag=True, help='詳細なログを表示')
def extract(input_file, output, config, preset, min_count, max_length, format, verbose):
    """
    テキストからフレーズを自動抽出（PMI/エントロピー分析）

    入力テキストを自動的に解析し、統計的に意味のあるフレーズを抽出します。
    設定ファイルの自動検出に対応しています（.japhrase.toml/.yml）。

    CLIオプションは設定ファイルの値を上書きします（優先度: CLI > 設定ファイル > デフォルト）。

    出力フィールド:
      seqchar      - 抽出フレーズ
      freq         - 出現回数
      length       - 文字数
      originality  - オリジナリティ係数 (0.0-1.0)
      periodic     - 周期性指標

    使用例:
    \b
      # SNS投稿向けプリセットで抽出
      japhrase extract tweets.txt --preset sns -o result.csv --format csv

      # カスタムパラメータで抽出
      japhrase extract paper.txt --min-count 10 --max-length 20 --format json -o output.json

      # 設定ファイルを使用（CLIオプションで上書き）
      japhrase extract draft.txt --config .japhrase.toml --preset novel -v
    """
    try:
        # 設定ファイルを読み込む
        cfg = JaphraseConfig(config)
        config_params = cfg.get_extractor_params()

        # ファイル読込
        texts = read_file(input_file, encoding='auto')
        click.echo(f"📖 {len(texts)}行を読み込みました", err=True)

        # パラメータをマージ（CLIオプション > 設定ファイル）
        final_params = config_params.copy()

        if preset is not None:
            final_params['preset'] = preset
        if min_count is not None:
            final_params['min_count'] = min_count
        if max_length is not None:
            final_params['max_length'] = max_length

        # PhraseExtracter 初期化
        if 'preset' in final_params and not min_count and not max_length:
            extractor = PhraseExtracter.preset(final_params['preset'], verbose=1 if verbose else 0)
        else:
            # デフォルト値を設定
            if 'min_count' not in final_params:
                final_params['min_count'] = 6
            if 'max_length' not in final_params:
                final_params['max_length'] = 16

            extractor = PhraseExtracter(
                verbose=1 if verbose else 0,
                **{k: v for k, v in final_params.items() if k in [
                    'min_count', 'max_length', 'min_length', 'threshold_originality',
                    'weight_freq', 'weight_len', 'removes', 'knowns', 'unnecesary'
                ]}
            )

        # 抽出実行
        click.echo("🔍 フレーズを抽出中...", err=True)
        phrases_df = extractor.get_dfphrase(texts)

        if len(phrases_df) == 0:
            click.echo("❌ フレーズが見つかりませんでした", err=True)
            sys.exit(1)

        click.echo(f"✅ {len(phrases_df)}個のフレーズを検出しました", err=True)

        # 出力
        if format == 'table':
            click.echo(phrases_df[['seqchar', 'freq', 'length']].head(20).to_string(index=False))
        elif format == 'csv' and output:
            export_to_csv(phrases_df, output)
            click.echo(f"💾 {output} に保存しました", err=True)
        elif format == 'json' and output:
            export_to_json(phrases_df, output)
            click.echo(f"💾 {output} に保存しました", err=True)
        else:
            click.echo(phrases_df[['seqchar', 'freq', 'length']].to_string(index=False))

    except Exception as e:
        click.echo(f"❌ エラー: {e}", err=True)
        sys.exit(1)


# ===== コマンド: stats =====
@cli.command()
@click.argument('input_file', type=click.Path(exists=True), metavar='INPUT_FILE')
@click.option('-o', '--output', type=click.Path(), help='統計結果出力先 (JSON/CSV形式)')
@click.option('--config', type=click.Path(exists=True), help='設定ファイル (.japhrase.toml / .japhrase.yml)')
@click.option('--preset', type=click.Choice(list(PRESETS.keys())),
              help=f'パラメータプリセット ({", ".join(PRESETS.keys())} から選択)')
@click.option('--min-count', type=int, help='最小出現回数フィルタ (デフォルト: 6)')
@click.option('--max-length', type=int, help='最大フレーズ長フィルタ (デフォルト: 16)')
@click.option('--format', type=click.Choice(['csv', 'json', 'table']), default='json',
              help='出力形式 (デフォルト: json - NRE v7対応)')
@click.option('--top-n', type=int, default=20, help='出力する上位フレーズ数 (デフォルト: 20)')
def stats(input_file, output, config, preset, min_count, max_length, format, top_n):
    """
    フレーズ統計を計算（JSON/CSV/テーブル形式対応）

    入力テキストを解析し、フレーズの統計情報を計算します。
    JSON形式での出力は NRE v7 の audit コマンドとシームレスに統合できます。

    計算される統計値:
      集計情報:
        - total_phrases        フレーズ総数
        - unique_phrases       ユニークフレーズ数
        - text_lines           テキスト行数

      頻度分析:
        - freq_mean            出現回数の平均
        - freq_median          出現回数の中央値
        - freq_std_dev         出現回数の標準偏差
        - freq_min/max         出現回数の最小/最大値

      長さ分析:
        - length_mean          フレーズ長の平均
        - length_median        フレーズ長の中央値
        - length_std_dev       フレーズ長の標準偏差

      多様性指標:
        - diversity_score      表現の多様性スコア
        - entropy              シャノンエントロピー

      上位フレーズ:
        - top_phrases          出現頻度上位のフレーズと統計

    JSON形式出力:
      NRE v7 の audit コマンドで自動的に YAML に変換可能です。
      API形式: { "status": "success", "data": {...}, "timestamp": "..." }

    使用例:
    \b
      # JSONで統計を出力（NRE v7連携用）
      japhrase stats manuscript.txt -o stats.json --format json

      # 上位100フレーズの統計をCSVで出力
      japhrase stats paper.txt --format csv -o phrase_stats.csv --top-n 100

      # コンソールに統計を表示
      japhrase stats text.txt --preset novel --format table

      # カスタムパラメータで統計計算
      japhrase stats corpus.txt --min-count 5 --max-length 20 -o output.json
    """
    try:
        # 設定ファイルを読み込む
        cfg = JaphraseConfig(config)
        config_params = cfg.get_extractor_params()

        # ファイル読込
        texts = read_file(input_file, encoding='auto')
        click.echo(f"📖 {len(texts)}行を読み込みました", err=True)

        # パラメータをマージ（CLIオプション > 設定ファイル）
        final_params = config_params.copy()
        if preset is not None:
            final_params['preset'] = preset
        if min_count is not None:
            final_params['min_count'] = min_count
        if max_length is not None:
            final_params['max_length'] = max_length

        # PhraseExtracter 初期化
        if 'preset' in final_params and not min_count and not max_length:
            extractor = PhraseExtracter.preset(final_params['preset'], verbose=0)
        else:
            if 'min_count' not in final_params:
                final_params['min_count'] = 6
            if 'max_length' not in final_params:
                final_params['max_length'] = 16

            extractor = PhraseExtracter(
                verbose=0,
                **{k: v for k, v in final_params.items() if k in [
                    'min_count', 'max_length', 'min_length', 'threshold_originality',
                    'weight_freq', 'weight_len', 'removes', 'knowns', 'unnecesary'
                ]}
            )

        # フレーズ抽出実行
        click.echo("🔍 フレーズを抽出中...", err=True)
        phrases_df = extractor.get_dfphrase(texts)

        if len(phrases_df) == 0:
            click.echo("❌ フレーズが見つかりませんでした", err=True)
            sys.exit(1)

        click.echo(f"✅ {len(phrases_df)}個のフレーズを検出しました", err=True)

        # 統計計算
        click.echo("📊 統計を計算中...", err=True)
        import numpy as np
        from datetime import datetime

        freq_col = phrases_df['freq'].values
        length_col = phrases_df['length'].values
        originality_col = phrases_df['originality'].values if 'originality' in phrases_df.columns else np.ones_like(freq_col)

        stats_data = {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'parameters': {
                'input_file': str(input_file),
                'min_count': final_params.get('min_count', 6),
                'max_length': final_params.get('max_length', 16),
                'preset': final_params.get('preset', 'custom')
            },
            'summary': {
                'total_phrases': int(len(phrases_df)),
                'unique_phrases': int(len(phrases_df)),
                'text_lines': int(len(texts)),
                'total_phrase_occurrences': int(freq_col.sum())
            },
            'frequency': {
                'mean': float(np.mean(freq_col)),
                'median': float(np.median(freq_col)),
                'std_dev': float(np.std(freq_col)),
                'min': int(np.min(freq_col)),
                'max': int(np.max(freq_col))
            },
            'length': {
                'mean': float(np.mean(length_col)),
                'median': float(np.median(length_col)),
                'std_dev': float(np.std(length_col)),
                'min': int(np.min(length_col)),
                'max': int(np.max(length_col))
            },
            'originality': {
                'mean': float(np.mean(originality_col)),
                'median': float(np.median(originality_col)),
                'std_dev': float(np.std(originality_col)),
                'min': float(np.min(originality_col)),
                'max': float(np.max(originality_col))
            },
            'diversity': {
                'entropy': float(-np.sum((freq_col / freq_col.sum()) * np.log2(freq_col / freq_col.sum() + 1e-10))),
                'gini_coefficient': float(2 * np.sum(np.arange(1, len(freq_col) + 1) * np.sort(freq_col)) / (len(freq_col) * np.sum(freq_col)) - (len(freq_col) + 1) / len(freq_col))
            },
            'top_phrases': []
        }

        # 上位フレーズを追加
        top_phrases_df = phrases_df.nlargest(min(top_n, len(phrases_df)), 'freq')
        for idx, row in top_phrases_df.iterrows():
            stats_data['top_phrases'].append({
                'phrase': str(row['seqchar']),
                'frequency': int(row['freq']),
                'length': int(row['length']),
                'originality': float(row['originality']) if 'originality' in row else 0.0
            })

        # 出力
        if format == 'json':
            if output:
                export_to_json(pd.DataFrame([stats_data]), output)
                click.echo(f"✅ JSON統計を出力しました: {output}", err=True)
            else:
                import json
                click.echo(json.dumps(stats_data, ensure_ascii=False, indent=2))
        elif format == 'csv':
            if output:
                # CSVには平坦化したデータを出力
                csv_data = []
                csv_data.append({
                    'metric': 'total_phrases',
                    'value': stats_data['summary']['total_phrases']
                })
                csv_data.append({
                    'metric': 'frequency_mean',
                    'value': stats_data['frequency']['mean']
                })
                csv_data.append({
                    'metric': 'frequency_median',
                    'value': stats_data['frequency']['median']
                })
                csv_data.append({
                    'metric': 'length_mean',
                    'value': stats_data['length']['mean']
                })
                csv_data.append({
                    'metric': 'entropy',
                    'value': stats_data['diversity']['entropy']
                })
                csv_df = pd.DataFrame(csv_data)
                export_to_csv(csv_df, output)
                click.echo(f"✅ CSV統計を出力しました: {output}", err=True)
            else:
                click.echo("❌ CSV形式では -o/--output オプションでファイル指定が必須です", err=True)
                sys.exit(1)
        else:  # table
            click.echo("\n" + "=" * 70)
            click.echo("フレーズ統計レポート")
            click.echo("=" * 70)
            click.echo(f"\n【基本情報】")
            click.echo(f"  フレーズ総数: {stats_data['summary']['total_phrases']}")
            click.echo(f"  テキスト行数: {stats_data['summary']['text_lines']}")
            click.echo(f"  総出現回数: {stats_data['summary']['total_phrase_occurrences']}")

            click.echo(f"\n【頻度統計】")
            click.echo(f"  平均: {stats_data['frequency']['mean']:.2f}")
            click.echo(f"  中央値: {stats_data['frequency']['median']:.2f}")
            click.echo(f"  標準偏差: {stats_data['frequency']['std_dev']:.2f}")
            click.echo(f"  範囲: {stats_data['frequency']['min']}-{stats_data['frequency']['max']}")

            click.echo(f"\n【長さ統計】")
            click.echo(f"  平均: {stats_data['length']['mean']:.2f} 文字")
            click.echo(f"  中央値: {stats_data['length']['median']:.2f} 文字")
            click.echo(f"  範囲: {stats_data['length']['min']}-{stats_data['length']['max']} 文字")

            click.echo(f"\n【多様性指標】")
            click.echo(f"  エントロピー: {stats_data['diversity']['entropy']:.3f}")
            click.echo(f"  ジニ係数: {stats_data['diversity']['gini_coefficient']:.3f}")

            click.echo(f"\n【出現頻度上位 {len(stats_data['top_phrases'])} フレーズ】")
            for i, phrase_info in enumerate(stats_data['top_phrases'], 1):
                click.echo(f"  {i:2d}. {phrase_info['phrase']:<20} (出現: {phrase_info['frequency']:3d}回, 長さ: {phrase_info['length']:2d})")
            click.echo("\n" + "=" * 70)

    except Exception as e:
        click.echo(f"❌ エラー: {e}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


# ===== コマンド: kwic =====
@cli.command()
@click.argument('input_file', type=click.Path(exists=True), metavar='INPUT_FILE')
@click.option('--phrase', required=True, help='検索対象フレーズ (必須)')
@click.option('-o', '--output', type=click.Path(), help='結果出力先ファイル')
@click.option('--context', type=int, default=1, help='前後の文脈行数 (デフォルト: 1)')
def kwic(input_file, phrase, output, context):
    """
    フレーズの出現箇所を文脈付きで検索 (KWIC: Keyword in Context)

    指定したフレーズがテキスト内のどこに出現するかを、前後の文脈と共に表示します。
    表記ゆれの確認や、フレーズの使用方法の検証に有用です。

    出力形式:
      出現番号    - 何番目の出現か（全体に対する位置）
      行番号      - テキスト内での行番号
      文字位置    - その行内での文字位置
      context     - 前後の文脈（フレーズは【】で囲まれる）

    使用例:
    \b
      # 「機械学習」の出現箇所を確認
      japhrase kwic paper.txt --phrase "機械学習" --context 2

      # 「表記ゆれ」の出現箇所を保存
      japhrase kwic manuscript.txt --phrase "表記ゆれ" -o kwic_results.txt
    """
    try:
        texts = read_file(input_file, encoding='auto')
        click.echo(f"📖 {len(texts)}行を読み込みました", err=True)

        kwic = KWICAnalyzer(texts, context_lines=context)
        results = kwic.find_phrase(phrase)

        if len(results) == 0:
            click.echo(f"❌ フレーズ「{phrase}」は見つかりませんでした", err=True)
            sys.exit(1)

        click.echo(f"✅ {len(results)}件検出しました\n", err=True)

        # 表示
        for idx, row in results.iterrows():
            click.echo(f"【出現 {row['occurrence_num']}/{row['total_occurrences']}】")
            click.echo(f"行番号: {row['line_num']}, 文字位置: {row['char_pos']}")
            click.echo(row['context'])
            click.echo("-" * 70)

        # ファイル出力
        if output:
            kwic.export_kwic_results(phrase, output)
            click.echo(f"💾 {output} に保存しました", err=True)

    except Exception as e:
        click.echo(f"❌ エラー: {e}", err=True)
        sys.exit(1)


# ===== コマンド: check-divergence =====
@cli.command()
@click.argument('abstract_file', type=click.Path(exists=True))
@click.argument('body_file', type=click.Path(exists=True))
@click.option('-o', '--output', type=click.Path(), help='レポート出力先')
def check_divergence(abstract_file, body_file, output):
    """
    あらすじと本文の乖離をチェック

    使用例:
    \b
        japhrase check-divergence abstract.txt body.txt
        japhrase check-divergence abstract.txt body.txt -o report.txt
    """
    try:
        abstract_text = '\n'.join(read_file(abstract_file, encoding='auto'))
        body_text = '\n'.join(read_file(body_file, encoding='auto'))

        click.echo("🔍 乖離分析を実行中...", err=True)
        checker = AbstractBodyChecker(abstract_text, body_text)

        report = checker.generate_report()
        click.echo(report)

        if output:
            checker.export_report(output)
            click.echo(f"\n💾 {output} に保存しました", err=True)

    except Exception as e:
        click.echo(f"❌ エラー: {e}", err=True)
        sys.exit(1)


# ===== コマンド: detect-habits =====
@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--reference-dir', type=click.Path(exists=True), help='参照コーパスディレクトリ')
@click.option('--top-n', type=int, default=10, help='表示上位件数')
@click.option('-o', '--output', type=click.Path(), help='出力先（CSV）')
def detect_habits(input_file, reference_dir, top_n, output):
    """
    個人の口癖・習癖を検出

    使用例:
    \b
        japhrase detect-habits text.txt
        japhrase detect-habits text.txt --reference-dir corpus/ -o habits.csv
    """
    try:
        texts = read_file(input_file, encoding='auto')
        click.echo(f"📖 {len(texts)}行を読み込みました", err=True)

        # 参照テキスト取得
        reference_texts = None
        if reference_dir:
            ref_files = list(Path(reference_dir).glob('*.txt'))
            reference_texts = []
            for f in ref_files:
                try:
                    reference_texts.extend(read_file(str(f), encoding='auto'))
                except:
                    pass

        click.echo("🔍 口癖を検出中...", err=True)
        detector = HabitDetector(texts, reference_texts=reference_texts)
        habits = detector.detect_habits(limit=top_n)

        if len(habits) == 0:
            click.echo("✅ 特別な口癖は見つかりませんでした", err=True)
        else:
            click.echo(f"✅ {len(habits)}個の習癖を検出しました\n", err=True)
            click.echo(habits.to_string(index=False))

            if output:
                habits.to_csv(output, index=False, encoding='utf-8-sig')
                click.echo(f"\n💾 {output} に保存しました", err=True)

    except Exception as e:
        click.echo(f"❌ エラー: {e}", err=True)
        sys.exit(1)


# ===== コマンド: analyze =====
@cli.command()
@click.argument('input_file', type=click.Path(exists=True), metavar='INPUT_FILE')
@click.option('--abstract', type=click.Path(exists=True),
              help='あらすじファイル (あらすじ vs 本文の乖離度を分析)')
@click.option('--corpus-dir', type=click.Path(exists=True),
              help='過去原稿ディレクトリ (セルフリコメンデーション用)')
@click.option('-o', '--output', type=click.Path(), help='分析レポート出力先')
@click.option('--preset', type=click.Choice(list(PRESETS.keys())), default='default',
              help=f'抽出パラメータプリセット (デフォルト: default)')
def analyze(input_file, abstract, corpus_dir, output, preset):
    """
    複数の分析機能を組み合わせた統合レポート生成

    1つのコマンドで以下の分析を順序実行します：
      [1] フレーズ自動抽出 (preset で指定)
      [2] あらすじ乖離度分析 (--abstract オプション指定時)
      [3] 個人の執筆習癖検出
      [4] セルフリコメンデーション (--corpus-dir 指定時)

    各セクションは統合レポートに含まれ、実行結果はコンソール表示と
    ファイル保存の両方に対応しています。

    レポート内容:
      📋 フレーズ抽出結果
      🔄 あらすじ乖離度（%）
      👤 検出された個人の習癖（上位5件）
      🔍 関連記事（過去原稿との類似度）

    使用例:
    \b
      # 基本的な使用 (フレーズ抽出のみ)
      japhrase analyze manuscript.txt -o report.txt

      # あらすじ乖離度も分析
      japhrase analyze manuscript.txt --abstract abstract.txt -o report.txt

      # 過去原稿との比較も含める
      japhrase analyze draft.txt --abstract abstract.txt \\
                 --corpus-dir past_articles/ -o full_report.txt

      # 特定プリセットを使用
      japhrase analyze novel.txt --preset novel --corpus-dir corpus/ -o analysis.txt
    """
    try:
        texts = read_file(input_file, encoding='auto')
        text = '\n'.join(texts)

        click.echo("📊 統合分析を開始します...\n", err=True)

        report = []
        report.append("=" * 70)
        report.append("japhrase 統合分析レポート")
        report.append("=" * 70)
        report.append("")

        # 1. フレーズ抽出
        click.echo("  [1/4] フレーズを抽出中...", err=True)
        extractor = PhraseExtracter.preset(preset, verbose=0)
        phrases_df = extractor.get_dfphrase(texts)
        report.append(f"\n📋 フレーズ抽出\n")
        report.append(f"検出フレーズ数: {len(phrases_df)}個")
        if len(phrases_df) > 0:
            report.append(f"上位フレーズ: {', '.join(phrases_df.head(5)['seqchar'].tolist())}")

        # 2. あらすじチェック
        if abstract:
            click.echo("  [2/4] あらすじをチェック中...", err=True)
            abstract_text = '\n'.join(read_file(abstract, encoding='auto'))
            checker = AbstractBodyChecker(abstract_text, text)
            divergence = checker.get_divergence_score()
            report.append(f"\n🔄 あらすじ vs 本文\n")
            report.append(f"乖離度: {divergence:.1%}")
        else:
            click.echo("  [2/4] スキップ (あらすじなし)", err=True)

        # 3. 口癖検出
        click.echo("  [3/4] 口癖を検出中...", err=True)
        detector = HabitDetector(texts)
        habits = detector.detect_habits(limit=5)
        report.append(f"\n👤 個人の習癖\n")
        if len(habits) > 0:
            report.append(f"検出数: {len(habits)}個")
        else:
            report.append("検出なし")

        # 4. セルフリコメンデーション
        if corpus_dir:
            click.echo("  [4/4] 関連記事を検索中...", err=True)
            recommender = SelfRecommender(corpus_dir, min_count=1)
            related = recommender.find_related_articles(text, top_n=3)
            report.append(f"\n🔍 関連記事\n")
            if len(related) > 0:
                report.append(f"見つかった記事: {len(related)}件")
            else:
                report.append("見つかりません")
        else:
            click.echo("  [4/4] スキップ (コーパスなし)", err=True)

        report.append("\n" + "=" * 70)
        report_text = "\n".join(report)

        click.echo(report_text)

        if output:
            with open(output, 'w', encoding='utf-8-sig') as f:
                f.write(report_text)
            click.echo(f"\n💾 {output} に保存しました", err=True)

    except Exception as e:
        click.echo(f"❌ エラー: {e}", err=True)
        sys.exit(1)


# ===== コマンド: workflow =====
@cli.command()
@click.argument('workflow_file', type=click.Path(exists=True))
@click.option('--parallel', is_flag=True, help='タスクを並列実行')
@click.option('--max-workers', type=int, default=4, help='並列実行時のワーカー数')
@click.option('-o', '--output', type=click.Path(), help='レポート出力先')
@click.option('-v', '--verbose', is_flag=True, help='詳細出力')
def workflow(workflow_file, parallel, max_workers, output, verbose):
    """
    YAMLで定義されたワークフローを実行

    ワークフロー定義ファイルに複数のタスクを記述し、
    依存関係を自動的に解決しながら順序実行または並列実行します。

    使用例:
    \b
        japhrase workflow manuscript.yaml
        japhrase workflow manuscript.yaml --parallel --max-workers 8
        japhrase workflow manuscript.yaml -o report.txt
    """
    try:
        click.echo(f"📋 ワークフローを読込中: {workflow_file}", err=True)

        # ワークフロー定義を読込
        wf = WorkflowDefinition.from_yaml(workflow_file)

        click.echo(f"✅ ワークフロー「{wf.name}」をロードしました", err=True)
        click.echo(f"   タスク数: {len(wf.tasks)}個", err=True)

        # ワークフロー検証
        valid, errors = wf.validate()
        if not valid:
            click.echo(f"❌ ワークフロー検証エラー:", err=True)
            for error in errors:
                click.echo(f"   - {error}", err=True)
            sys.exit(1)

        # 実行順序を表示
        execution_order = wf.get_execution_order()
        click.echo(f"📊 実行順序: {' → '.join(execution_order)}", err=True)

        # ワークフロー実行
        if parallel:
            click.echo(f"🚀 並列実行を開始します (ワーカー数: {max_workers})...", err=True)
        else:
            click.echo("🚀 順序実行を開始します...", err=True)

        engine = WorkflowEngine()
        results = engine.execute(wf, parallel=parallel, max_workers=max_workers)

        # レポート生成
        report = engine.get_report()
        click.echo(report)

        # ファイル出力
        if output:
            with open(output, 'w', encoding='utf-8-sig') as f:
                f.write(report)
            click.echo(f"\n💾 {output} に保存しました", err=True)

        # 完了状況をチェック
        completed = sum(1 for r in results.values() if r.status.value == 'completed')
        failed = sum(1 for r in results.values() if r.status.value == 'failed')

        if failed > 0:
            click.echo(f"\n⚠️ {completed}/{len(results)}個のタスクが完了しました", err=True)
            sys.exit(1)
        else:
            click.echo(f"\n✅ すべてのタスクが正常に完了しました", err=True)

    except FileNotFoundError as e:
        click.echo(f"❌ ファイルが見つかりません: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ エラー: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


# ===== ユーティリティコマンド =====
@cli.command()
def presets_list():
    """
    利用可能なプリセット一覧を表示
    """
    click.echo("利用可能なプリセット:")
    click.echo("=" * 70)
    for name, config in PRESETS.items():
        click.echo(f"\n[{name}]")
        click.echo(f"  {config['description']}")
        click.echo(f"  パラメータ: min_count={config['min_count']}, "
                   f"max_length={config['max_length']}")


@cli.command()
def version():
    """
    バージョン情報を表示
    """
    from . import __version__
    click.echo(f"japhrase version {__version__}")


# ===== コマンド: use-case =====
@cli.command(name='use-case')
@click.argument('use_case', type=click.Choice([
    'academic_writing', 'novel_revision', 'blog_writing', 'sns_content', 'editing'
]))
@click.option('--body', type=click.Path(exists=True), help='本文ファイル')
@click.option('--abstract', type=click.Path(exists=True), help='あらすじファイル')
@click.option('--v1', type=click.Path(exists=True), help='バージョン1（小説推敲用）')
@click.option('--v2', type=click.Path(exists=True), help='バージョン2（小説推敲用）')
@click.option('--v3', type=click.Path(exists=True), help='バージョン3（小説推敲用）')
@click.option('--corpus', type=click.Path(exists=True), help='過去原稿ディレクトリ')
@click.option('-o', '--output', type=click.Path(), help='レポート出力先')
def use_case(use_case, body, abstract, v1, v2, v3, corpus, output):
    """
    ユースケース別ワークフローを実行

    特定の執筆シナリオに最適化されたワークフローを実行します。

    利用可能なユースケース:
    \b
    - academic_writing: 学位論文・学術論文の品質チェック
    - novel_revision: 小説原稿の推敲
    - blog_writing: ブログ記事の最適化
    - sns_content: SNS投稿の表記統一
    - editing: 編集者向けチェック

    使用例:
    \b
        japhrase use-case academic_writing --body paper.txt --abstract abstract.txt
        japhrase use-case novel_revision --v1 draft1.txt --v2 draft2.txt
        japhrase use-case blog_writing --body article.txt --corpus past_articles/
        japhrase use-case sns_content --body tweet.txt -o report.txt
    """
    try:
        click.echo(f"📋 ユースケース: {use_case}", err=True)

        # ワークフローを生成
        workflow = WritingWorkflow.for_use_case(use_case)

        # ワークフローを実行
        report = workflow.run(
            body_file=body,
            abstract_file=abstract,
            v1=v1,
            v2=v2,
            v3=v3,
            past_corpus_dir=corpus,
            output_dir='results'
        )

        # レポートを表示
        click.echo(report)

        # ファイル出力
        if output:
            with open(output, 'w', encoding='utf-8-sig') as f:
                f.write(report)
            click.echo(f"\n💾 {output} に保存しました", err=True)

        click.echo("\n✅ 分析完了", err=True)

    except ValueError as e:
        click.echo(f"❌ エラー: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ エラー: {e}", err=True)
        sys.exit(1)


@cli.command(name='use-case-list')
def use_case_list():
    """
    利用可能なユースケース一覧を表示
    """
    click.echo("利用可能なユースケース:")
    click.echo("=" * 70)

    usecases = WritingWorkflow.list_usecases()
    for use_case_id, description in usecases.items():
        click.echo(f"\n[{use_case_id}]")
        click.echo(f"  {description}")


# ===== コマンド: config =====
@cli.command()
@click.option('--file', type=click.Path(exists=True), help='設定ファイルパス')
@click.option('--show-defaults', is_flag=True, help='デフォルト値も表示')
def config(file, show_defaults):
    """
    設定ファイルの内容を表示

    使用例:
    \b
        japhrase config
        japhrase config --file .japhrase.toml
        japhrase config --show-defaults
    """
    try:
        cfg = JaphraseConfig(file)

        if cfg.config:
            click.echo(cfg.display_config())
        else:
            click.echo("アクティブな設定ファイルが見つかりません", err=True)
            if show_defaults:
                click.echo("\n=== デフォルト設定 ===")
                click.echo("min_count: 6")
                click.echo("max_length: 16")
                click.echo("threshold_originality: 0.5")

    except Exception as e:
        click.echo(f"❌ エラー: {e}", err=True)
        sys.exit(1)


# ===== コマンド: check =====
@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--config', type=click.Path(exists=True), help='設定ファイルパス (.toml/.yml)')
@click.option('-o', '--output', type=click.Path(), help='レポート出力先')
def check(input_file, config, output):
    """
    文書品質チェック（Linter モード）

    設定ファイルのルールに基づいて文書品質をチェック。
    - 禁止ワード検出
    - 必須キーワード確認
    - 表記ゆれ検出
    - 文書長チェック
    - 段落構成チェック

    使用例:
    \b
        japhrase check document.txt --config .japhrase.toml
        japhrase check document.txt --config .japhrase.toml -o report.txt
    """
    try:
        # テキスト読み込み
        texts = read_file(input_file, encoding='auto')
        text = '\\n'.join(texts)
        click.echo(f"📖 {len(texts)}行を読み込みました", err=True)

        # 設定ファイル読み込み
        cfg = JaphraseConfig(config)
        if not cfg.config:
            click.echo("❌ 設定ファイルが見つかりません", err=True)
            sys.exit(1)

        # チェッカー実行
        click.echo("🔍 品質チェックを実行中...", err=True)
        checker = QualityChecker(text, cfg.config)
        success, errors, warnings = checker.run_all_checks()

        # レポート表示
        report = checker.get_report()
        click.echo(report)

        # ファイル出力
        if output:
            with open(output, 'w', encoding='utf-8-sig') as f:
                f.write(report)
            click.echo(f"💾 {output} に保存しました", err=True)

        # 結果に応じて終了コードを設定
        if not success:
            sys.exit(1)

        click.echo("✅ チェック完了", err=True)

    except Exception as e:
        click.echo(f"❌ エラー: {e}", err=True)
        sys.exit(1)


def main():
    """CLIのメインエントリーポイント"""
    cli()


if __name__ == '__main__':
    main()
