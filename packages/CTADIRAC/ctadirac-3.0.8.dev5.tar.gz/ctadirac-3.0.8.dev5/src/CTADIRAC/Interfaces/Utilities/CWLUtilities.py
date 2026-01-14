from copy import deepcopy
from typing import Union
from pathlib import Path
from cwl_utils.parser import (
    File,
    InputArraySchema,
    OutputArraySchema,
    Workflow,
    WorkflowStep,
    CommandLineTool,
    ExpressionTool,
)
from cwl_utils.parser.cwl_v1_2 import CommandInputArraySchema

LFN_PREFIX = "lfn://"
LFN_DIRAC_PREFIX = "LFN:"
LOCAL_PREFIX = "file://"
JS_REQ = {"class": "InlineJavascriptRequirement"}


def verify_cwl_output_type(
    output_type: Union[str, OutputArraySchema, list[Union[str, OutputArraySchema]]]
) -> bool:
    """Check if output type is a "File" str or OutputArraySchema (or a list containing them).

    Parameters
    ----------
    output_type : Union[str, OutputArraySchema, List[Union[str, OutputArraySchema]]]
        The output type.
    """
    if isinstance(output_type, list):
        return any(t == "File" or isinstance(t, OutputArraySchema) for t in output_type)
    return output_type == "File" or isinstance(output_type, OutputArraySchema)


def get_current_step_obj(cwl_obj: Workflow, step_name: str):
    """Get the current step object by step name.

    Parameters
    ----------
    cwl_obj : Workflow
        The CWL workflow object containing steps.
    step_name : str
        The name of the step to retrieve.

    Returns
    -------
    step : WorkflowStep | None
        The matched step object, or None if not found.
    """
    for step in cwl_obj.steps:
        if step.id.rpartition("#")[2].split("/")[0] == step_name:
            return step
    return None


def fill_defaults(cwl: Union[Workflow, CommandLineTool, ExpressionTool], inputs: dict):
    """Fill defaults from CWL inputs into inputs dict.
    This is needed for evaluating expressions later on.

    Parameters
    ----------
    cwl : Union[Workflow, CommandLineTool, ExpressionTool]
        The CWL definition
    inputs : dict
        User provided inputs.

    Returns
    -------
    inputs : dict
        Inputs with additional values filled from CWL defaults
    """
    updated_inputs = deepcopy(inputs)

    def fill_input_inputs(step):
        for inp in step.inputs:
            key = inp.id.rpartition("#")[2].split("/")[-1]
            if inp.default is not None:  # and key not in updated_inputs
                updated_inputs[key] = inp.default

    if isinstance(cwl, Workflow):
        for step in cwl.steps:
            fill_input_inputs(step.run)
    elif isinstance(cwl, (CommandLineTool, ExpressionTool)):
        fill_input_inputs(cwl)

    return updated_inputs


def set_input_file_basename(inputs: dict) -> None:
    """Ensure input Files have basename set.

    Parameters
    ----------
    inputs : dict
        cwl inputs
    """
    for inp in inputs.values():
        inp = set_basename_value(inp)
    return inputs


def set_basename_value(input: dict):
    """Set basename field of a cwl File.

    Parameters
    ----------
    input : dict | File
        CWL input

    Returns
    -------
    dict | File
        CWL input
    """
    if isinstance(input, File) and not input.basename:
        input.basename = Path(input.path).name
    elif isinstance(input, list):
        for val in input:
            if isinstance(val, File) and not val.basename:
                val.basename = Path(val.path).name
    # ensure it works with dict inputs
    elif isinstance(input, dict):
        if input.get("class", None) == "File" and not input.get("basename", None):
            input["basename"] = Path(input.get("path", "")).name
        if input.get("class", None) == "List" and not input.get("basename", None):
            for val in input:
                if input.get("class", None) == "File" and not input.get(
                    "basename", None
                ):
                    input["basename"] = Path(input.get("path", "")).name
    return input


def get_step_input_type(step: WorkflowStep, input_name: str):
    """Retrieve the step input type.

    Parameters
    ----------
    step : WorkflowStep
    input_name : str

    Returns
    -------
    Any:
        input type
    """
    for input in step.run.inputs:
        if input.id.rpartition("#")[2].split("/")[-1] == input_name:
            return input.type_


def get_step_output_type(step: WorkflowStep, output_name: str):
    """Retrieve the step output type.

    Parameters
    ----------
    step : WorkflowStep
    output_name : str

    Returns
    -------
    Any:
        Output type
    """
    for output in step.run.outputs:
        if output.id.rpartition("#")[2].split("/")[-1] == output_name:
            return output.type_


def format_input_by_type(
    input: str, in_type: list | str
) -> str | dict[str, str] | list[dict[str, str]]:
    """Format the input value by type

    Parameters
    ----------
    input : str
        input name
    in_type : list | str
        _description_

    Returns
    -------
    str | dict[str, str] | list[dict[str, str]]
        formatted input
    """
    if isinstance(in_type, list):
        if "null" in in_type:
            in_type.remove("null")
        if len(in_type) == 1:
            in_type = in_type[0]
        elif "File" in in_type:
            in_type = "File"
            # Is there any other cases than [File, string]
    if isinstance(in_type, str):
        if in_type in ["boolean", "string", "int"]:
            return input
        elif in_type == "File":
            return {"class": "File", "path": input}
    elif isinstance(in_type, (CommandInputArraySchema, InputArraySchema)):
        if in_type.type_ == "File":
            return {"class": "File", "path": input}
        elif in_type.type_ == "string":
            return input
    else:
        return input


def format_output_by_type(
    output: str, out_type: list | str
) -> str | dict[str, str] | None:
    """Format output value by type

    Parameters
    ----------
    output : str
        Output name
    out_type : list | str
        Output type

    Returns
    -------
    str | dict[str, str] | None
        Formatted output
    """
    if isinstance(output, str):
        if isinstance(out_type, str):
            if out_type in ["boolean", "string", "int"]:
                return output
            elif out_type in ["File", "File[]"]:
                return {"class": "File", "path": output}
        elif isinstance(out_type, OutputArraySchema):
            if out_type.type_ == "File":
                return {"class": "File", "path": output}
            elif out_type.type_ == "string":
                return output
        else:
            return output
    else:
        return output
