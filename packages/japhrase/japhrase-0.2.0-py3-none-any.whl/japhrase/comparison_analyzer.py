"""
プロンプト最適化用の差分分析モジュール

Good と Bad のプロンプトを比較して：
- Winning Templates (成功テンプレート：Good に多くあり、Bad にない)
- Failure Patterns (失敗パターン：Bad に多くあり、Good にない)
- Common Baseline (共通ベース：両方にある)
を N-gram エンジンで抽出
"""

from typing import Dict, Set, List, Tuple
from pathlib import Path
import json
import logging

from japhrase import PhraseExtracter


logger = logging.getLogger(__name__)


class ComparisonAnalyzer:
    """
    Good/Bad プロンプトの比較分析を行うクラス
    
    PhraseExtracter の N-gram エンジンを使い、
    長いテンプレート・パターンを抽出する
    """
    
    def __init__(
        self,
        min_count: int = 2,
        min_length: int = 10,
        max_length: int = 100,
        use_pmi: bool = True
    ):
        """
        Args:
            min_count: フレーズの最小出現数
            min_length: フレーズの最小文字数（短いゴミを除外）
            max_length: フレーズの最大文字数（長いテンプレートを許容）
            use_pmi: PMI を使用するか（テンプレート抽出には True 推奨）
        """
        self.extractor = PhraseExtracter(
            min_count=min_count,
            min_length=min_length,
            max_length=max_length,
            use_pmi=use_pmi
        )
        self.min_count = min_count
        self.min_length = min_length
        self.max_length = max_length
        self.use_pmi = use_pmi
        
        logger.info(f"ComparisonAnalyzer initialized:")
        logger.info(f"  min_count={min_count}, min_length={min_length}, max_length={max_length}, use_pmi={use_pmi}")
    
    def compare_corpora(
        self,
        good_texts: List[str],
        bad_texts: List[str]
    ) -> Dict:
        """
        Good と Bad のテキストを比較して差分を抽出
        
        Good コーパスと Bad コーパスから、それぞれフレーズを抽出して
        スコアを比較し、勝利テンプレートと失敗パターンを特定する
        
        生のテキストのまま（カンマで分割しない）N-gram エンジンに食わせることで、
        長い「呪文の塊」（テンプレート）を抽出できる
        
        Args:
            good_texts: Good プロンプト（リスト）
            bad_texts: Bad プロンプト（リスト）
        
        Returns:
            {
                "winning_templates": [...],  # Good で高スコア
                "failure_patterns": [...],   # Bad で高スコア
                "common_baseline": [...],    # 両方で出現
                "analysis": {...}
            }
        """
        logger.info(f"Extracting phrases from {len(good_texts)} Good and {len(bad_texts)} Bad prompts...")
        
        # 各コーパスからフレーズを抽出
        # ここで split(',') は行わない。生のテキストのまま食わせる
        # そうすることで、PMI/エントロピーが「並び順」を見て、長い塊を認識する
        good_df = self.extractor.extract(good_texts)
        bad_df = self.extractor.extract(bad_texts)
        
        logger.info(f"Extracted {len(good_df)} phrases from Good corpus")
        logger.info(f"Extracted {len(bad_df)} phrases from Bad corpus")
        
        # フレーズセットを作成
        good_phrases = set(good_df['phrase'].values) if len(good_df) > 0 else set()
        bad_phrases = set(bad_df['phrase'].values) if len(bad_df) > 0 else set()
        
        # スコア辞書を作成（フレーズ -> スコア）
        good_scores = dict(zip(good_df['phrase'].values, good_df['score'].values)) if len(good_df) > 0 else {}
        bad_scores = dict(zip(bad_df['phrase'].values, bad_df['score'].values)) if len(bad_df) > 0 else {}
        
        # 集合演算
        only_in_good = good_phrases - bad_phrases  # Good だけ
        only_in_bad = bad_phrases - good_phrases   # Bad だけ
        in_both = good_phrases & bad_phrases       # 両方
        
        logger.info(f"Only in Good: {len(only_in_good)}")
        logger.info(f"Only in Bad: {len(only_in_bad)}")
        logger.info(f"In both: {len(in_both)}")
        
        # 勝利テンプレートを抽出（Good で出現し、Bad にはない）
        winning_templates = [
            (phrase, good_scores[phrase])
            for phrase in only_in_good
            if phrase in good_scores
        ]
        winning_templates.sort(key=lambda x: x[1], reverse=True)
        
        # 失敗パターンを抽出（Bad で出現し、Good にはない）
        failure_patterns = [
            (phrase, bad_scores[phrase])
            for phrase in only_in_bad
            if phrase in bad_scores
        ]
        failure_patterns.sort(key=lambda x: x[1], reverse=True)
        
        # 共通ベースラインを抽出
        common_baseline = [
            (phrase, good_scores.get(phrase, bad_scores.get(phrase, 0)))
            for phrase in in_both
        ]
        common_baseline.sort(key=lambda x: x[1], reverse=True)
        
        result = {
            "winning_templates": winning_templates,  # [(phrase, score), ...]
            "failure_patterns": failure_patterns,    # [(phrase, score), ...]
            "common_baseline": common_baseline,      # [(phrase, score), ...]
            "analysis": {
                "good_count": len(good_texts),
                "bad_count": len(bad_texts),
                "good_phrases": len(good_phrases),
                "bad_phrases": len(bad_phrases),
                "only_in_good": len(only_in_good),
                "only_in_bad": len(only_in_bad),
                "common_phrases": len(in_both),
                "min_count": self.min_count,
                "min_length": self.min_length,
                "max_length": self.max_length,
                "use_pmi": self.use_pmi
            }
        }
        
        return result
    
    def compare_from_files(
        self,
        good_file: Path,
        bad_file: Path
    ) -> Dict:
        """
        ファイルから Good/Bad テキストを読み込んで比較
        
        ファイル形式：1行 = 1つのプロンプト
        
        Args:
            good_file: Good プロンプトファイルパス
            bad_file: Bad プロンプトファイルパス
        
        Returns:
            比較結果
        """
        logger.info(f"Loading from files: {good_file}, {bad_file}")
        
        with open(good_file, "r", encoding="utf-8") as f:
            good_texts = [line.strip() for line in f if line.strip()]
        
        with open(bad_file, "r", encoding="utf-8") as f:
            bad_texts = [line.strip() for line in f if line.strip()]
        
        logger.info(f"Loaded {len(good_texts)} Good and {len(bad_texts)} Bad prompts")
        
        return self.compare_corpora(good_texts, bad_texts)
    
    def generate_report(self, comparison_result: Dict) -> str:
        """
        比較結果からレポートを生成
        
        Args:
            comparison_result: compare_corpora() の戻り値
        
        Returns:
            レポートテキスト
        """
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append("プロンプト最適化分析レポート")
        report_lines.append("=" * 70)
        report_lines.append("")
        
        # 分析サマリー
        analysis = comparison_result["analysis"]
        report_lines.append("📊 分析サマリー")
        report_lines.append("-" * 70)
        report_lines.append(f"Good プロンプト数: {analysis['good_count']}")
        report_lines.append(f"Bad プロンプト数: {analysis['bad_count']}")
        report_lines.append(f"Good フレーズ数: {analysis['good_phrases']}")
        report_lines.append(f"Bad フレーズ数: {analysis['bad_phrases']}")
        report_lines.append(f"Good だけに出現: {analysis['only_in_good']}")
        report_lines.append(f"Bad だけに出現: {analysis['only_in_bad']}")
        report_lines.append(f"両方に出現: {analysis['common_phrases']}")
        report_lines.append("")
        
        # 分析設定
        report_lines.append("⚙️  分析設定")
        report_lines.append("-" * 70)
        report_lines.append(f"最小出現数: {analysis['min_count']}")
        report_lines.append(f"最小文字数: {analysis['min_length']}")
        report_lines.append(f"最大文字数: {analysis['max_length']}")
        report_lines.append(f"PMI スコアリング: {'Yes' if analysis['use_pmi'] else 'No'}")
        report_lines.append("")
        
        # 勝利テンプレート
        report_lines.append("🏆 勝利テンプレート (Good に含まれる長い塊)")
        report_lines.append("-" * 70)
        
        winning = comparison_result.get("winning_templates", [])
        if winning:
            for i, (phrase, score) in enumerate(winning[:15], 1):
                report_lines.append(f"  {i:2d}. [{score:6.2f}] {phrase}")
            if len(winning) > 15:
                report_lines.append(f"  ... and {len(winning) - 15} more templates")
        else:
            report_lines.append("  (該当なし)")
        report_lines.append("")
        
        # 失敗パターン
        report_lines.append("💀 失敗パターン (Bad に含まれる長い塊)")
        report_lines.append("-" * 70)
        
        failures = comparison_result.get("failure_patterns", [])
        if failures:
            for i, (phrase, score) in enumerate(failures[:15], 1):
                report_lines.append(f"  {i:2d}. [{score:6.2f}] {phrase}")
            if len(failures) > 15:
                report_lines.append(f"  ... and {len(failures) - 15} more patterns")
        else:
            report_lines.append("  (該当なし)")
        report_lines.append("")
        
        # 共通ベースライン
        report_lines.append("🔗 共通ベースライン (Good と Bad の両方に出現)")
        report_lines.append("-" * 70)
        
        common = comparison_result.get("common_baseline", [])
        if common:
            for i, (phrase, score) in enumerate(common[:10], 1):
                report_lines.append(f"  {i:2d}. [{score:6.2f}] {phrase}")
            if len(common) > 10:
                report_lines.append(f"  ... and {len(common) - 10} more items")
        else:
            report_lines.append("  (該当なし)")
        report_lines.append("")
        
        # 推奨事項
        report_lines.append("💡 推奨事項")
        report_lines.append("-" * 70)
        
        if winning:
            top_winning = winning[0][0]
            report_lines.append(f"✅ この組み合わせを使用してください:")
            report_lines.append(f"   '{top_winning}'")
        
        if failures:
            top_failure = failures[0][0]
            report_lines.append(f"❌ この組み合わせを避けてください:")
            report_lines.append(f"   '{top_failure}'")
        
        report_lines.append("")
        report_lines.append("=" * 70)
        
        return "\n".join(report_lines)
    
    def save_results(
        self,
        comparison_result: Dict,
        output_file: Path,
        include_report: bool = True
    ):
        """
        結果をJSONファイルに保存
        
        Args:
            comparison_result: 比較結果
            output_file: 出力ファイルパス
            include_report: レポート生成も行うか
        """
        # JSON 保存
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(comparison_result, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Results saved to {output_file}")
        
        # レポート生成
        if include_report:
            report_file = output_file.with_stem(output_file.stem + "_report").with_suffix(".txt")
            report = self.generate_report(comparison_result)
            
            with open(report_file, "w", encoding="utf-8") as f:
                f.write(report)
            
            logger.info(f"Report saved to {report_file}")
            
            return output_file, report_file
        
        return output_file, None


if __name__ == "__main__":
    import sys
    
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s"
    )
    
    # Windows のエンコーディング対応
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    
    # テスト用コード
    # max_length を 100 に設定して、長いテンプレートを抽出
    analyzer = ComparisonAnalyzer(
        min_count=2,
        min_length=10,
        max_length=100,
        use_pmi=True
    )
    
    # データセットディレクトリ
    dataset_dir = Path(__file__).parent.parent / "data" / "toy_dataset"
    
    if dataset_dir.exists():
        good_file = dataset_dir / "good_positive.txt"
        bad_file = dataset_dir / "bad_positive.txt"
        
        if good_file.exists() and bad_file.exists():
            print("🔍 Comparing Good vs Bad prompts...\n")
            result = analyzer.compare_from_files(good_file, bad_file)
            
            print(analyzer.generate_report(result))
            
            # 結果保存
            output_file = dataset_dir / "comparison_results.json"
            json_file, report_file = analyzer.save_results(result, output_file)
            print(f"\n✅ Results saved to {json_file}")
            if report_file:
                print(f"✅ Report saved to {report_file}")
        else:
            print("⚠️  Dataset files not found. Run generate_comfy_toy_dataset.py first.")
    else:
        print("⚠️  Dataset directory not found. Run generate_comfy_toy_dataset.py first.")
