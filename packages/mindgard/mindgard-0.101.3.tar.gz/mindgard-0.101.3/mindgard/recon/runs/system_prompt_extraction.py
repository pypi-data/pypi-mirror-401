# Standard library imports
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import Any

# Third party imports
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Project imports
from mindgard.api.exceptions import ClientException
from mindgard.api.recon.system_prompt_extraction import ReconSystemPromptExtractionClient, SystemPromptExtractResult
from mindgard.auth import load_access_token
from mindgard.constants import API_BASE, DASHBOARD_URL
from mindgard.recon.subcommands.system_prompt_extraction import SystemPromptExtractionReconCommand
from mindgard.utils import CliResponse
from mindgard.wrappers.llm import LLMModelWrapper


def run_system_prompt_extraction(console: Console, model_wrapper: LLMModelWrapper, final_args: dict[str, Any]):
    access_token = load_access_token()
    recon_service = ReconSystemPromptExtractionClient(API_BASE, access_token, final_args["project_id"])
    recon_command = SystemPromptExtractionReconCommand(recon_service, model_wrapper)
    result: SystemPromptExtractResult = None

    def system_prompt_extraction() -> None:
        nonlocal result
        recon_id = recon_command.start_system_prompt_extraction(final_args["project_id"])
        recon_command.poll_system_prompt_extraction(recon_id)
        result = recon_command.fetch_recon_system_prompt_extraction_result(recon_id)

    def system_prompt_extraction_with_spinner() -> None:
        with Progress(
            SpinnerColumn(style="bold yellow"),
            TextColumn("[bold yellow]Probing for system prompt extractions…"),
            transient=True,
            console=console,
        ) as progress:
            task_id = progress.add_task("probing", total=None)

            with ThreadPoolExecutor(max_workers=1) as executor:
                input_encoding_future = executor.submit(system_prompt_extraction)

                while not input_encoding_future.done():
                    sleep(0.15)

                progress.update(task_id, completed=100)
                input_encoding_future.result()

    try:
        system_prompt_extraction_with_spinner()
    except ClientException as ex:
        raise ex

    if result is None:
        console.print("Failed to get result from system prompt extraction recon session")
        exit(CliResponse(1).code())

    console.print("\nProbing completed!", style="bold green")
    detected = result.result.total_detected > 0

    if not detected:
        console.print("\nNo clear signs of system prompt from target system.", style="bold red")
        console.print(
            f"\n[underline]Reasoning[/underline]: The target didn't produce outputs that point to a detected system prompt."
        )
        console.print(
            f"[underline]Recommendation[/underline]: Run the complete mindgard test suite for open-ended probing to uncover any additional risks. See [yellow]mindgard test --help[/yellow] to learn more.\n"
        )
        exit(CliResponse(0).code())

    console.print(
        f"\nFull results can be found here: {DASHBOARD_URL}/results/recon?project_id={result.project_id}&reconType=system_prompt_extraction\n"
    )
