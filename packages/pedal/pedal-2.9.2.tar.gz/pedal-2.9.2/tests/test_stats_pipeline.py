
from pedal.command_line import run_job
from pedal.command_line.modes import StatsPipeline, MODES
from pedal.core.config_job import JobConfig


def test_stats_pipeline():
    """
    Test the StatsPipeline class to ensure it initializes correctly and can run.
    """
    pipeline = StatsPipeline(JobConfig(
        mode=MODES.STATS,
        submissions = "def main():\n    return 'Hello, World!'",
        instructor = "from pedal import *\nensure_function('main', score='+60%')",
        instructor_direct = True,
        submission_direct = True,
        points= ".5",
        output=None
    ))
    assert pipeline is not None, "StatsPipeline should be initialized"

    # Run the pipeline and check if it completes without errors
    try:
        result = pipeline.execute()
    except Exception as e:
        assert False, f"StatsPipeline run failed with exception: {e}"

    # Check if the report is generated
    assert pipeline.submissions[0].result.resolution.score == .5, "Expected score to be 1.5"

    print(pipeline.result)


def test_run_job():
    """
    Test the run_job function with StatsPipeline mode.
    """
    submissions = run_job(
        submissions = "def main():\n    return 'Hello, World!'",
        instructor = "from pedal import *\nensure_function('main', score='+60%')\n#### pool_1 ####\nensure_ast('For')\n#### pool_2 ####\nensure_ast('If')\n#### Footer ####\n",
        instructor_direct = True,
        submission_direct = True,
        points= ".5",
        pool = "submission_id",
        execution = {"submission_id": 0},
    )

    assert submissions is not None, "run_job should return a result"
    assert submissions[0].result.error is None
    assert submissions[0].result.resolution.score == .5, "Expected score to be 1.5"
    assert submissions[0].result.resolution.label == 'unused_variable'
    assert submissions[0].result.resolution.category == 'algorithmic'
    if not "MAIN_REPORT" in submissions[0].result.data:
        raise submissions[0].result.error
    main_report = submissions[0].result.data['MAIN_REPORT']
    print(main_report.feedback)
