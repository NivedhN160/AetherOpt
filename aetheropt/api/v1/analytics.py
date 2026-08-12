from fastapi import APIRouter
from aetheropt.datascience.analysis.result_analyzer import ResultAnalyzer

router = APIRouter()

@router.get("/")
def get_analytics_summary():
    """Returns basic aggregate statistics across all past experiments."""
    analyzer = ResultAnalyzer(log_dir="experiments/runs")
    summary = analyzer.generate_summary()
    return summary
