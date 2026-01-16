from pedal.questions.graders import FunctionGrader
from pedal.questions.questions import Question

def grade_function_question(function_name, signature, tests, instructions=None, config=None,
                            max_points=None, definition_points=None, components_points=None,
                            max_components_points=None, unit_test_type_points=None,
                            unit_test_value_points=None, unit_test_total_points=None,
                            unit_test_type_ratio=None, unit_test_completion_points=None
                            ):
    """

    Args:
        function_name:
        signature:
        tests:
        config:

    Returns:

    """
    grader = FunctionGrader(function_name, signature, tests, config,
                            max_points, definition_points, components_points,
                            max_components_points, unit_test_type_points,
                            unit_test_value_points, unit_test_total_points,
                            unit_test_type_ratio, unit_test_completion_points)
    question = Question(function_name, instructions, grader)
    return grader._test(question)