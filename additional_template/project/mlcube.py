"""MLCube handler file"""

import typer
from main import run_inference

app = typer.Typer()


@app.command("infer")
def infer(
    data_path: str = typer.Option(..., "--data_path"),
    # parameters_file: str = typer.Option(..., "--parameters_file"),
    output_path: str = typer.Option(..., "--output_path"),
    # Provide additional parameters as described in the mlcube.yaml file
    # e.g. model weights:
    model_path: str = typer.Option(..., "--model_path"),
):
    # Modify the infer command as needed
    run_inference(data_path, model_path, output_path)


@app.command("hotfix")
def hotfix():
    # NOOP command for typer to behave correctly. DO NOT REMOVE OR MODIFY
    pass


if __name__ == "__main__":
    app()