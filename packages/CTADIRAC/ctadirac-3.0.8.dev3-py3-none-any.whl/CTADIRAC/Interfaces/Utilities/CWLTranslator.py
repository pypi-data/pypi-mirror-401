from copy import deepcopy
from pathlib import Path
from typing import Any

from cwl_utils.pack import pack
from cwl_utils.parser import load_document, WorkflowStep, save, load_document_by_uri
from cwl_utils.parser import (
    CommandLineTool,
    CommandOutputParameter,
    ExpressionTool,
    File,
    Workflow,
    WorkflowStepInput,
)
from cwl_utils.parser.utils import load_inputfile
from cwl_utils.expression import do_eval

from CTADIRAC.Interfaces.Utilities.CWLUtilities import (
    fill_defaults,
    format_input_by_type,
    format_output_by_type,
    get_step_input_type,
    get_step_output_type,
    set_basename_value,
    verify_cwl_output_type,
    LFN_PREFIX,
    LOCAL_PREFIX,
    LFN_DIRAC_PREFIX,
    JS_REQ,
    set_input_file_basename,
)


class CWLTranslator:
    """Translator from CWL Workflow to DIRAC Job.
    Extract needed DIRAC job arguments from the CWL and inputs description.

    Parameters
    ----------
        cwl_workflow : str
            Path to the local CWL workflow file
        cwl_inputs : str
            Path to the local CWL inputs file
    """

    def __init__(
        self,
        cwl_workflow: str,
        cwl_inputs: str,
    ) -> None:
        self.cwl_workflow_path = Path(cwl_workflow)
        self.cwl_inputs_path = Path(cwl_inputs)

        self.original_cwl = load_document(pack(str(self.cwl_workflow_path)))
        self.unpacked_cwl = load_document_by_uri(self.cwl_workflow_path)
        self.original_inputs = load_inputfile(
            self.original_cwl.cwlVersion, self.cwl_inputs_path.read_text()
        )

        self.transformed_inputs = deepcopy(self.original_inputs)
        self.transformed_cwl = deepcopy(self.original_cwl)
        self.output_sandbox = []
        self.output_data = []
        self.input_sandbox = []
        self.input_data = []

        self.current_step_name = None

    def translate(self, cvmfs_base_path: Path, apptainer_options: list[Any]) -> None:
        """Translate the CWL workflow description into Dirac compliant execution.

        Parameters
        ----------
            cvmfs_base_path : Path
                The base path for CVMFS container repository.
            apptainer_options : list[Any]
                A list of options for Apptainer.
        """

        if isinstance(self.transformed_cwl, CommandLineTool):
            self._translate_clt(cvmfs_base_path, apptainer_options)

        if isinstance(self.transformed_cwl, Workflow):
            self._translate_workflow(cvmfs_base_path, apptainer_options)

    def _translate_clt(
        self, cvmfs_base_path: Path, apptainer_options: list[Any]
    ) -> None:
        """Translate the CWL CommandLineTool description into Dirac compliant execution.

        Parameters
        ----------
            cvmfs_base_path : Path
                The base path for CVMFS container repository.
            apptainer_options : list[Any]
                A list of options for Apptainer.
        """

        if self.transformed_cwl.hints:
            self.transformed_cwl = self._translate_docker_hints(
                self.transformed_cwl, cvmfs_base_path, apptainer_options
            )
        self._extract_and_translate_input_files()
        self._extract_output_files(self.transformed_cwl, self.original_inputs)

    def _translate_workflow(
        self, cvmfs_base_path: Path, apptainer_options: list[Any]
    ) -> None:
        """Translate the CWL Workflow description into Dirac compliant execution.

        Parameters
        ----------
        cvmfs_base_path : Path
            The base path for CVMFS container repository.
        apptainer_options : list[Any]
            A list of options for Apptainer.
        """
        # Need to set the file basename for JSReq:
        self.transformed_inputs = set_input_file_basename(self.transformed_inputs)
        self.transformed_inputs = fill_defaults(
            self.transformed_cwl, self.transformed_inputs
        )
        # Extract the DIRAC related
        self._extract_and_translate_input_files()

        self.evaluated_steps_outputs = {}
        steps_inputs = deepcopy(self.transformed_inputs)
        for n, wf_step in enumerate(self.transformed_cwl.steps):
            step_name = wf_step.id.rpartition("#")[2].split("/")[0]
            self.current_step_name = step_name
            self.evaluated_steps_outputs.setdefault(step_name, {})
            # replace docker hints
            if wf_step.run.hints:
                self.transformed_cwl.steps[n].run = self._translate_docker_hints(
                    wf_step.run, cvmfs_base_path, apptainer_options
                )
            # Update the input context for next steps
            steps_inputs = fill_defaults(wf_step.run, steps_inputs)
            steps_inputs = set_input_file_basename(steps_inputs)
            steps_inputs = self._evaluate_step_inputs(wf_step, steps_inputs)

            # Evaluate step outputs
            # specific evaluation if the step is an ExpressionTool
            if isinstance(wf_step.run, ExpressionTool):
                exptool_outputs = self._evaluate_expression_tool_outputs(
                    self.unpacked_cwl, wf_step, steps_inputs, step_name
                )
                self.evaluated_steps_outputs[step_name] = exptool_outputs
            else:
                self._evaluate_step_outputs(wf_step, steps_inputs)
        # Finally extract the DIRAC related outputs
        self._extract_workflow_outputs()

    @staticmethod
    def _translate_docker_hints(
        cwl_object: CommandLineTool, cvmfs_base_path: Path, apptainer_options: list[Any]
    ) -> CommandLineTool:
        """Translate CWL DockerRequirement into Dirac compliant execution.

        Parameters
        ----------
            cwl_object : CommandLineTool
                The CWL definition.
            cvmfs_base_path : Path
                The base path for CVMFS container repository.
            apptainer_options : list[Any]
                A list of options for Apptainer.

        Returns
        -------
            cwl_object :CommandLineTool
                The translated cwl object.
        """
        for index, hint in enumerate(cwl_object.hints):
            if hint.class_ == "DockerRequirement":
                image = hint.dockerPull
                image_path = str(cvmfs_base_path / f"{image}")

                cmd = [
                    "apptainer",
                    "run",
                    *apptainer_options,
                    image_path,
                ]

                if isinstance(cwl_object.baseCommand, str):
                    cmd.append(cwl_object.baseCommand)
                else:
                    cmd.extend(cwl_object.baseCommand)

                cwl_object.baseCommand = cmd
                del cwl_object.hints[index]
                break
        return cwl_object

    def _evaluate_step_inputs(
        self, step: WorkflowStep, inputs: dict[str, Any]
    ) -> dict[str, Any]:
        """Evaluate inputs in Workflow step.

        Parameters
        ----------
            step : WorkflowStep
                Current WorkflowStep
            inputs : dict[str, Any]
                Workflow inputs.

        Returns
        -------
            wf_inputs : dict[str, Any]
                Updated workflow inputs with evaluated step inputs.
        """

        def evaluate_input(
            inp: WorkflowStepInput, input_context: dict, scatter_inputs: dict
        ) -> list | dict[str, Any] | None:
            """Evaluate input value from JS expression or sources.

            Parameters
            ----------
            inp : WorkflowStepInput
                Input 'in_' object
            input_context : dict
                CWL input context
            scatter_inputs : dict
                Scattered inputs

            Returns
            -------
            list | dict[str, Any] | None
                Evaluated CWL File or list of CWL File
            """
            inp_id = inp.id.rpartition("#")[2].split("/")[-1]
            if inp.valueFrom:
                # evaluate if it is a JS exp
                if inp.valueFrom.startswith("$("):
                    # handle the case where the input is scattered
                    # First find if the expression contains the scattered input
                    scatter_match = [
                        scat_inp
                        for scat_inp in scatter_inputs.keys()
                        if scat_inp in inp.valueFrom
                    ]
                    if scatter_match:
                        eval_files = []
                        scatter_input_context = deepcopy(input_context)
                        for match in scatter_match:
                            for input in scatter_inputs[match]:
                                # Update context with only one item from the input
                                scatter_input_context[match] = input
                                eval_exp = do_eval(
                                    inp.valueFrom,
                                    scatter_input_context,
                                    outdir=None,
                                    requirements=[JS_REQ],
                                    tmpdir=None,
                                    resources={},
                                )
                                eval_files.append(
                                    format_input_by_type(
                                        eval_exp, get_step_input_type(step, inp_id)
                                    )
                                )
                        return eval_files
                    else:
                        eval_exp = do_eval(
                            inp.valueFrom,
                            input_context,
                            outdir=None,
                            requirements=[JS_REQ],
                            tmpdir=None,
                            resources={},
                        )
                        return format_input_by_type(
                            eval_exp, get_step_input_type(step, inp_id)
                        )
                else:
                    return format_input_by_type(
                        inp.valueFrom, get_step_input_type(step, inp_id)
                    )

            if inp.source:
                # if the input refers to a source from another step output
                # we need to map it using stored interpreted outputs from
                # previous steps
                sources = []
                if isinstance(inp.source, str):
                    sources = [inp.source]
                elif isinstance(inp.source, list):
                    sources = inp.source
                # TODO: do we need to handle the scatter case here?
                for src in sources:
                    inp_source = src.rpartition("#")[2].split("/")
                    if len(inp_source) > 1:
                        step_ref = inp_source[0]
                        source = inp_source[-1]
                        if (
                            source
                            in self.evaluated_steps_outputs.get(step_ref, {}).keys()
                        ):
                            # TODO: can that be a list?
                            return self.evaluated_steps_outputs[step_ref][source]
                    elif inp_source[0] in save(self.transformed_inputs):
                        return save(self.transformed_inputs)[inp_source[0]]
                    elif inp_source[0] in input_context:
                        return input_context[inp_source[0]]

        updated_inputs = save(deepcopy(inputs))
        scatter_inputs = self._get_scattered_inputs(step, updated_inputs)
        for inp in step.in_:
            inp_id = inp.id.rpartition("#")[2].split("/")[-1]
            eval_inp = evaluate_input(inp, updated_inputs, scatter_inputs)
            updated_inputs[inp_id] = set_basename_value(eval_inp)

        return updated_inputs

    def _get_scattered_inputs(self, step: WorkflowStep, inputs: dict) -> dict:
        """Retrieve the input names which are scattered.

        Parameters
        ----------
        step : WorkflowStep
            CWL Workflow step object
        inputs : dict
            CWL Input object

        Returns
        -------
        dict:
            scatter input : input value
        """
        scatter_inputs = {}
        if step.scatter:
            if isinstance(step.scatter, list):
                scattered_ids = [
                    scatter_input.rpartition("#")[2].split("/")[-1]
                    for scatter_input in step.scatter
                ]
            else:
                scattered_ids = [step.scatter.rpartition("#")[2].split("/")[-1]]

            for scat_id in scattered_ids:
                # match the scatter input with the inputs
                match = self._find_input_source(step, scat_id)
                scatter_inputs[scat_id] = inputs.get(match, None)
        return scatter_inputs

    def _find_input_source(self, step: WorkflowStep, input: str) -> str | None:
        """Find the source in the step for a given input.

        Parameters
        ----------
            step : WorkflowStep
                The step where inputs are defined.
            input :str
                The name of the input to match.

        Returns
        -------
            (str|None): The source of the input in the step, or None if not found.
        """
        for inp in step.in_:
            # Extract the input ID and check if it matches the scattered input
            inp_id = inp.id.rpartition("#")[2].split("/")[-1]
            if inp_id == input:
                return inp.source.rpartition("#")[2].split("/")[-1]
        return None

    def _evaluate_step_outputs(self, step: WorkflowStep, inputs: dict):
        """Evaluate Workflow Step outputs.

        Parameters
        ----------
            step : WorkflowStep
                WorkflowStep in which evaluate the outputs
            inputs : dict
                Updated inputs with evaluated input from previous steps
        """
        for output in step.run.outputs:
            output_name = output.id.rpartition("#")[2].split("/")[-1]
            glob = output.outputBinding.glob
            if glob:
                if isinstance(glob, str):
                    # the glob is an expression we evaluate it
                    glob_exp = glob if glob.startswith("$(") else None
                    if glob_exp:
                        eval_glob = do_eval(
                            glob,
                            inputs,
                            outdir=None,
                            requirements=[],
                            tmpdir=None,
                            resources={},
                        )
                        if step.scatter and isinstance(eval_glob, list):
                            for out in eval_glob:
                                self.evaluated_steps_outputs[
                                    self.current_step_name
                                ].setdefault(output_name, []).append(
                                    format_output_by_type(out, output.type_)
                                )
                        else:
                            self.evaluated_steps_outputs[self.current_step_name][
                                output_name
                            ] = format_output_by_type(eval_glob, output.type_)
                    else:
                        self.evaluated_steps_outputs[self.current_step_name][
                            output_name
                        ] = format_output_by_type(glob, output.type_)
                elif isinstance(glob, list):
                    self.evaluated_steps_outputs[self.current_step_name].setdefault(
                        output_name, []
                    )
                    for g in glob:
                        if isinstance(g, str):
                            self.evaluated_steps_outputs[self.current_step_name][
                                output_name
                            ].append(format_output_by_type(g, output.type_))

    def _evaluate_expression_tool_outputs(
        self,
        unpacked_cwl_obj: Workflow,
        wf_step: WorkflowStep,
        cwl_inputs: dict,
        step_name: str,
    ):
        """Evaluate the ExpressionTool outputs.

        Parameters
        ----------
            unpacked_cwl_obj : Workflow
                The unpacked CWL workflow.
            wf_step : WorkflowStep
                The Workflow step.
            cwl_inputs : dict
                The CWL inputs dict.
            step_name :str
                The current step name.

        Returns
        -------
            dict:
                A dictionary containing the evaluated ExpressionTool outputs.
        """
        for st in unpacked_cwl_obj.steps:
            if st.id.rpartition("#")[2].split("/")[0] == step_name:
                exp_tool_step = st

        expr_inputs = []
        if wf_step.scatter:
            # In the scattering case we need to verfify the input name
            expr_inputs = self._create_scatter_exptool_inputs(
                wf_step, cwl_inputs, exp_tool_step
            )
        else:
            # In the case where there is no scattering, we assume there is only one single input
            input_name = wf_step.run.inputs[0].id.rpartition("#")[2].split("/")[-1]
            source = exp_tool_step.in_[0].source.rpartition("#")[2].split("/")[-1]
            for inp, value in cwl_inputs.items():
                # Then we match the input name and the input value name
                if inp == source:
                    expr_inputs.append({input_name: value})

        # Finally we evaluate the JS expression
        exptool_outputs = {}
        for inp in expr_inputs:
            inp = fill_defaults(wf_step.run, inp)

            # Evaluate the JS expression
            eval_exp = do_eval(
                wf_step.run.expression,
                save(inp),
                outdir=None,
                requirements=[JS_REQ],
                tmpdir=None,
                resources={},
            )
            for key, val in eval_exp.items():
                output_type = get_step_output_type(wf_step, key)
                if wf_step.scatter:
                    exptool_outputs.setdefault(key, []).append(
                        format_output_by_type(val, output_type)
                    )
                else:
                    exptool_outputs[key] = format_output_by_type(val, output_type)
        return exptool_outputs

    @staticmethod
    def _create_scatter_exptool_inputs(
        wf_step: WorkflowStep, inputs: dict, exp_tool_step: WorkflowStep
    ) -> list[dict]:
        """Create a list of inputs by matching the scatter input names
        and the names in the cwl inputs.

        Parameters
        ----------
            wf_step : WorkflowStep
                The CWL Workflow step.
            inputs: dict
                The CWL inputs.
            exp_tool_step : WorkflowStep
                The Expression Tool step from the unpacked CWL.

        Returns
        -------
            list[dict]:
                Expression Tool inputs list.
        """

        def find_source_in_exp_tool_step(
            exp_tool_step: WorkflowStep, scattered_inp: str
        ) -> str | None:
            """Find the source in the ExpressionTool step for a given scattered input.

            Parameters
            ----------
                exp_tool_step : WorkflowStep
                    The ExpressionTool step where inputs are defined.
                scattered_inp : str
                    The name of the scattered input to match.

            Returns
            -------
                (str|None): The source of the input in the ExpressionTool step, or None if not found.
            """
            for inp in exp_tool_step.in_:
                # Extract the input ID and check if it matches the scattered input
                inp_id = inp.id.rpartition("#")[2].split("/")[-1]
                if inp_id == scattered_inp:
                    return inp.source.rpartition("#")[2].split("/")[-1]
            return None

        expr_inputs = []
        scattered_inp = wf_step.scatter.rpartition("#")[2].split("/")[-1]

        # Find the source corresponding to the scattered input
        source = find_source_in_exp_tool_step(exp_tool_step, scattered_inp)

        # Match the scatter input name with the input value name
        for inp, value in inputs.items():
            if inp == source:
                value = value if isinstance(value, list) else [value]
                expr_inputs.extend({scattered_inp: val} for val in value)

        return expr_inputs

    def _extract_and_translate_input_files(self) -> None:
        """Extract input files from CWL inputs and rewrite file paths.
        If the file is a Sandbox, ensure there is no absolute path, and store it in the input sandbox list.
        If the file is a LFN, remove the lfn prefix and store it in the lfns list.
        """

        def rewrite_file_path(file: File | str) -> str:
            """Rewrite file path.

            Parameters
            ----------
                file : File | str
                    File which path should be rewritten.

            Returns:
            -----
                str:
                    The new file path.
            """
            path, is_lfn = self._translate_sandboxes_and_lfns(file)
            (self.input_data if is_lfn else self.input_sandbox).append(path)
            return Path(path.removeprefix(LFN_DIRAC_PREFIX)).name

        for key, input_value in self.transformed_inputs.items():
            if isinstance(input_value, list):
                for file in input_value:
                    if isinstance(file, File):
                        file.path = rewrite_file_path(file)
            elif isinstance(input_value, File):
                input_value.path = rewrite_file_path(input_value)
            elif isinstance(input_value, str) and input_value.startswith(LFN_PREFIX):
                self.transformed_inputs[key] = Path(
                    input_value.removeprefix(LFN_PREFIX)
                ).name

    def _translate_sandboxes_and_lfns(self, file: File | str) -> tuple[str, bool]:
        """Extract local files as sandboxes and lfns as input data.

        Parameters
        ----------
            file : File | str
                Local file.

        Returns
        -------
            (str, bool):
                A tuple containing a filename and a boolean if it's a lfn (True) or not (False).
        """
        filename = file.path if isinstance(file, File) else file
        if not filename:
            raise KeyError("File path is not defined.")

        is_lfn = filename.startswith(LFN_PREFIX)
        if is_lfn:
            filename = filename.replace(LFN_PREFIX, LFN_DIRAC_PREFIX)
        filename = filename.removeprefix(LOCAL_PREFIX)
        return filename, is_lfn

    def _extract_workflow_outputs(self):
        """Extract the DIRAC outputs (output sandbox/data) from Workflow outputs."""
        for output in self.transformed_cwl.outputs:
            output_source_step = output.outputSource.rpartition("#")[2].split("/")[0]
            output_source_name = output.outputSource.rpartition("#")[2].split("/")[-1]
            output_value = self.evaluated_steps_outputs[output_source_step].get(
                output_source_name, None
            )

            if isinstance(output_value, list):
                for out in output_value:
                    self._fill_dirac_outputs(out)
            else:
                self._fill_dirac_outputs(output_value)

    def _fill_dirac_outputs(self, output_value: dict):
        """Fill DIRAC output sandbox and data lists.

        Parameters
        ----------
            output_value : dict
        """
        if output_value.get("class", None) == "File":
            if output_value.get("path", "").startswith(LFN_PREFIX):
                self.output_data.append(
                    output_value.get("path", "").replace(LFN_PREFIX, LFN_DIRAC_PREFIX)
                )
            else:
                self.output_sandbox.append(output_value.get("path", ""))

    def _extract_output_files(
        self,
        cwl_obj: CommandLineTool,
        cwl_inputs: dict,
        outputs_to_record: [list | None] = None,
        update_inputs: bool = False,
        always_resolve_output: bool = False,
    ) -> dict:
        """Translate output files into a DIRAC compliant usage.

        Extract local outputs and lfns.
        Remove outputs path prefix.

        Parameters
        ----------
            cwl_obj : CommandLineTool
                The CWL definition.
            cwl_inputs : dict
                CWL inputs.
            outputs_to_record : list|None
                A list of outputs to record.
            update_inputs : bool
                If True, update cwl inputs with output expression (Needed for interpreting JS requirements).
            always_resolve_output : bool
                If True, resolve output expression even if not in the outputs list (Needed for interpreting JS requirements).

        Returns
        -------
            dict:
                Inputs or updated inputs
        """
        inputs = fill_defaults(cwl_obj, cwl_inputs)

        for output in cwl_obj.outputs:
            if not verify_cwl_output_type(output.type_):
                continue

            output_id = (
                output.id.rpartition("#")[2].split("/")[-1] if output.id else None
            )
            if not output_id:
                continue

            glob_list = self._create_glob_list(output)
            for glob in glob_list:
                resolved_glob = self._process_glob(
                    inputs, glob, outputs_to_record, output_id, always_resolve_output
                )
                if update_inputs and output_id not in inputs:
                    inputs = self._update_input_with_output(
                        inputs, resolved_glob, output, output_id
                    )
        return inputs

    @staticmethod
    def _create_glob_list(output: CommandOutputParameter) -> list:
        """
        Create a list of glob expressions.

        Parameters
        ----------
            output : CommandOutputParameter
                The output to process.

        Returns
        -------
            list:
                A list of glob expressions.
        """
        if not output.outputBinding:
            return []
        glob_expr = output.outputBinding.glob
        return [glob_expr] if isinstance(glob_expr, str) else glob_expr or []

    def _process_glob(
        self,
        inputs: dict,
        glob: str,
        outputs_to_record: list | None,
        output_id: str,
        always_resolve_output: bool,
    ) -> str:
        """Evaluate a glob expression and record it if needed.

        Parameters
        ----------
            inputs : dict
                CWL inputs (with added defaults).
            glob : str
                The glob expression.
            outputs_to_record :list
                A list of outputs to record.
            output_id : str
                The current output id.
            always_resolve_output : bool
                If True, resolve output expression even if not in the outputs list (Needed for interpreting JS requirements).
        """
        should_record_output = (
            outputs_to_record is None or output_id in outputs_to_record
        )
        should_eval = (
            should_record_output or always_resolve_output
        ) and glob.startswith("$")
        if should_eval:
            glob = do_eval(
                glob,
                inputs,
                outdir=None,
                requirements=[],
                tmpdir=None,
                resources={},
            )
        if self.current_step_name:
            self.evaluated_steps_outputs[self.current_step_name][output_id] = glob
        if should_record_output:
            if glob.startswith(LFN_PREFIX):
                self.output_data.append(glob.replace(LFN_PREFIX, LFN_DIRAC_PREFIX))
            else:
                self.output_sandbox.append(glob)

        return glob

    @staticmethod
    def _update_input_with_output(
        inputs: dict, resolved_glob: str, output: CommandOutputParameter, output_id: str
    ) -> dict:
        """Inject resolved output value into inputs for JS/parameter expressions.

        Parameters
        ----------
            inputs : dict
                CWL inputs (with added defaults).
            resolved_glob: str
                The resolved glob expression.
            output : CommandOutputParameter
                The output to process.
            output_id : str
                The current output id.

        Returns
        -------
            dict:
                Updated inputs.
        """
        if output.type_ == "File":
            inputs[output_id] = {
                "class": "File",
                "path": resolved_glob,
                "basename": resolved_glob,
            }
        else:
            inputs[output_id] = resolved_glob
        return inputs
