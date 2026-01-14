import pytest
from cwl_utils.parser.cwl_v1_2 import (
    CommandLineTool,
    CommandInputParameter,
    CommandOutputParameter,
    CommandInputArraySchema,
    CommandOutputArraySchema,
    File,
    InputArraySchema,
    OutputArraySchema,
    Workflow,
    WorkflowStep,
)
from cwl_utils.parser import save

from CTADIRAC.Interfaces.Utilities.CWLUtilities import (
    format_input_by_type,
    format_output_by_type,
    get_current_step_obj,
    get_step_input_type,
    get_step_output_type,
    set_basename_value,
    set_input_file_basename,
    verify_cwl_output_type,
    fill_defaults,
)

ARRAY_FILE_OUTPUT = CommandOutputArraySchema(items="test.txt", type_="File")
ARRAY_ARRAY_OUTPUT = CommandOutputArraySchema(
    items=["test.txt", "test2.txt"], type_="array"
)


@pytest.mark.parametrize(
    ("output_type", "expected_result"),
    [
        ("File", True),
        (ARRAY_FILE_OUTPUT, True),
        (ARRAY_ARRAY_OUTPUT, True),
        (["File"], True),
        (["null", "File"], True),
        (["null", ARRAY_FILE_OUTPUT], True),
        (["null", ARRAY_ARRAY_OUTPUT], True),
        ("string", False),
        (["null", "string"], False),
    ],
)
def test_verify_cwl_output_type(output_type, expected_result):
    result = verify_cwl_output_type(output_type)
    assert result is expected_result


@pytest.mark.parametrize(
    ("cwl", "inputs", "expected_inputs"),
    [
        (
            CommandLineTool(
                inputs=[
                    CommandInputParameter(
                        id="/some/path#step_1",
                        type_="string",
                    )
                ],
                outputs={},
            ),
            {"input1": "input1", "input2": "input2"},
            {"input1": "input1", "input2": "input2"},
        ),
        (
            Workflow(
                steps=[
                    WorkflowStep(
                        id="/some/path#step_1",
                        in_=[],
                        out=[],
                        run=CommandLineTool(
                            inputs=[
                                CommandInputParameter(
                                    id="/some/path#step_1",
                                    type_="string",
                                    default="defaultInputStep1",
                                )
                            ],
                            outputs=[],
                            baseCommand="echo CLT1",
                        ),
                    ),
                    WorkflowStep(
                        id="/some/path#step_2",
                        in_=[],
                        out=[],
                        run=CommandLineTool(
                            inputs=[
                                CommandInputParameter(
                                    id="/some/path#step_2",
                                    type_="string",
                                    default="defaultInputStep2",
                                )
                            ],
                            outputs=[],
                            baseCommand="echo CLT2",
                        ),
                    ),
                ],
                inputs={},
                outputs={},
            ),
            {"input1": "input1", "input2": "input2"},
            {
                "input1": "input1",
                "input2": "input2",
                "step_1": "defaultInputStep1",
                "step_2": "defaultInputStep2",
            },
        ),
    ],
)
def test_fill_defaults(cwl, inputs, expected_inputs):
    result = fill_defaults(cwl, inputs)
    assert result == expected_inputs


@pytest.mark.parametrize(
    ("input_file", "expected_basename"),
    [
        (save({"input1": File(path="test_lfn_file.txt")}), "test_lfn_file.txt"),
        ({"input1": File(path="test_lfn_file.txt")}, "test_lfn_file.txt"),
        (
            save({"input1": File(path="test_local_file.txt", basename="local_file")}),
            "local_file",
        ),
        (
            {"input1": File(path="test_local_file.txt", basename="local_file")},
            "local_file",
        ),
        ({"input1": {"class": "File", "path": "/some/path/to/file.txt"}}, "file.txt"),
    ],
)
def test_set_input_file_basename(input_file, expected_basename):
    set_input_file_basename(input_file)
    for inp in input_file.values():
        if isinstance(inp, File):
            assert inp.basename == expected_basename
        else:
            assert inp.get("basename") == expected_basename


@pytest.mark.parametrize(
    ("cwl", "step_name", "expected_step_id"),
    [
        (
            Workflow(
                steps=[
                    WorkflowStep(
                        id="/some/path#step_1",
                        in_=[],
                        out=[],
                        run=CommandLineTool(
                            inputs=[
                                CommandInputParameter(
                                    id="/some/path#step_1",
                                    type_="string",
                                    default="defaultInputStep1",
                                )
                            ],
                            outputs=[],
                            baseCommand="echo CLT1",
                        ),
                    ),
                    WorkflowStep(
                        id="/some/path#step_2",
                        in_=[],
                        out=[],
                        run=CommandLineTool(
                            inputs=[
                                CommandInputParameter(
                                    id="/some/path#step_2",
                                    type_="string",
                                    default="defaultInputStep2",
                                )
                            ],
                            outputs=[],
                            baseCommand="echo CLT2",
                        ),
                    ),
                ],
                inputs={},
                outputs={},
            ),
            "step_2",
            "/some/path#step_2",
        ),
    ],
)
def test_get_current_step_obj(cwl, step_name, expected_step_id):
    step = get_current_step_obj(cwl, step_name)
    assert step.id == expected_step_id


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        (
            {"class": "File", "path": "/some/path/to/file.txt"},
            {"class": "File", "path": "/some/path/to/file.txt", "basename": "file.txt"},
        ),
    ],
)
def test_set_basename_value(input, expected):
    result = set_basename_value(input)
    assert result == expected


@pytest.mark.parametrize(
    ("step", "input_name", "expected"),
    [
        (
            WorkflowStep(
                id="/some/path#step_1",
                in_=[],
                out=[],
                run=CommandLineTool(
                    inputs=[
                        CommandInputParameter(
                            id="/some/path#step_1/input1",
                            type_="string",
                            default="defaultInputStep1",
                        ),
                        CommandInputParameter(
                            id="/some/path#step_1/input2",
                            type_="File",
                            default="defaultInputStep2",
                        ),
                    ],
                    outputs=[],
                    baseCommand="echo CLT1",
                ),
            ),
            "input2",
            "File",
        ),
    ],
)
def test_get_step_input_type(step, input_name, expected):
    result = get_step_input_type(step, input_name)
    assert result == expected


@pytest.mark.parametrize(
    ("step", "output_name", "expected"),
    [
        (
            WorkflowStep(
                id="/some/path#step_1",
                in_=[],
                out=[],
                run=CommandLineTool(
                    inputs=[],
                    outputs=[
                        CommandOutputParameter(
                            id="/some/path#step_1/output1",
                            type_="string",
                        ),
                        CommandOutputParameter(
                            id="/some/path#step_1/output2",
                            type_="File",
                        ),
                    ],
                    baseCommand="echo CLT1",
                ),
            ),
            "output2",
            "File",
        ),
    ],
)
def test_get_step_output_type(step, output_name, expected):
    result = get_step_output_type(step, output_name)
    assert result == expected


@pytest.mark.parametrize(
    ("input", "in_type", "expected"),
    [
        # Basic string types
        ("value", "string", "value"),
        ("true", "boolean", "true"),
        ("42", "int", "42"),
        # File type
        ("myfile.txt", "File", {"class": "File", "path": "myfile.txt"}),
        # List types
        ("myfile.txt", ["File", "string"], {"class": "File", "path": "myfile.txt"}),
        ("value", ["string", "null"], "value"),
        ("value", ["null", "string"], "value"),
        ("value", ["null"], "value"),
        # CommandInputArraySchema
        (
            "myfile.txt",
            CommandInputArraySchema(items="myfile.txt", type_="File"),
            {"class": "File", "path": "myfile.txt"},
        ),
        ("value", CommandInputArraySchema(items="value", type_="string"), "value"),
        # InputArraySchema
        (
            "myfile.txt",
            InputArraySchema(items="myfile.txt", type_="File"),
            {"class": "File", "path": "myfile.txt"},
        ),
        ("value", InputArraySchema(items="value", type_="string"), "value"),
        # Edge case: empty list
        ("value", [], "value"),
    ],
)
def test_format_input_by_type(input, in_type, expected):
    result = format_input_by_type(input, in_type)
    assert result == expected


@pytest.mark.parametrize(
    ("output", "out_type", "expected"),
    [
        # Basic string types
        ("value", "string", "value"),
        ("true", "boolean", "true"),
        ("42", "int", "42"),
        # File type
        ("myfile.txt", "File", {"class": "File", "path": "myfile.txt"}),
        # OutputArraySchema
        (
            "myfile.txt",
            OutputArraySchema(items="myfile.txt", type_="File"),
            {"class": "File", "path": "myfile.txt"},
        ),
        ("value", OutputArraySchema(items="value", type_="string"), "value"),
        # Edge case: non-string output
        (None, "File", None),
        # Edge case: empty string output
        ("", "string", ""),
    ],
)
def test_format_output_by_type(output, out_type, expected):
    result = format_output_by_type(output, out_type)
    assert result == expected
