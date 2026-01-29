"""Command-line interface for Monte Carlo SWE Probability."""

import sys
from datetime import date, datetime
from pathlib import Path

import click

from . import __version__
from .config import Config, DEFAULT_CONFIG_PATH, get_default_config_template, load_config
from .data_loader import DataLoadError, load_csv, validate_csv
from .metrics import calculate_throughput
from .output import (
    format_config_text,
    format_date_forecast_json,
    format_date_forecast_text,
    format_scope_forecast_json,
    format_scope_forecast_text,
    format_validation_json,
    format_validation_text,
)
from .simulation import DateForecastResult, SimulationConfig, forecast_date, forecast_scope


class DateParamType(click.ParamType):
    """Click parameter type for dates."""

    name = "date"

    def convert(self, value, param, ctx):
        if isinstance(value, date):
            return value

        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            self.fail(f"'{value}' is not a valid date. Use YYYY-MM-DD format.", param, ctx)


DATE = DateParamType()


def parse_confidence_levels(ctx, param, value: str | None) -> tuple[int, ...] | None:
    """Parse comma-separated confidence levels."""
    if value is None:
        return None

    try:
        levels = tuple(int(x.strip()) for x in value.split(","))
        for level in levels:
            if not 1 <= level <= 99:
                raise click.BadParameter(
                    f"Confidence level {level} must be between 1 and 99"
                )
        return levels
    except ValueError:
        raise click.BadParameter(
            f"Invalid confidence levels: '{value}'. Use comma-separated integers (e.g., 50,85,95)"
        )


@click.group()
@click.version_option(version=__version__, prog_name="mcswe")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--debug", is_flag=True, help="Enable debug output")
@click.pass_context
def main(ctx, verbose: bool, debug: bool):
    """Monte Carlo simulation tool for software engineering forecasting.

    Use historical throughput data to forecast delivery dates or scope.
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["debug"] = debug


@main.group()
def forecast():
    """Run forecasting simulations."""
    pass


@forecast.command("date")
@click.option(
    "--items", "-i", required=True, type=int, help="Number of items to complete"
)
@click.option(
    "--data", "-d", required=True, type=click.Path(exists=True), help="Path to CSV data file"
)
@click.option(
    "--start-date",
    type=DATE,
    default=None,
    help="Forecast start date (default: today)",
)
@click.option(
    "--simulations",
    "-n",
    type=int,
    default=None,
    help="Number of simulations (default: 10000)",
)
@click.option(
    "--confidence",
    "-c",
    callback=parse_confidence_levels,
    help="Confidence levels, comma-separated (default: 50,85,95)",
)
@click.option(
    "--exclude-weekends/--include-weekends",
    default=None,
    help="Exclude weekends from calculations (default: exclude)",
)
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.option("--no-histogram", is_flag=True, help="Hide histogram in text output")
@click.pass_context
def forecast_date_cmd(
    ctx,
    items: int,
    data: str,
    start_date: date | None,
    simulations: int | None,
    confidence: tuple[int, ...] | None,
    exclude_weekends: bool | None,
    output_json: bool,
    no_histogram: bool,
):
    """Forecast when items will be completed.

    Given a number of remaining items, predict completion dates at various
    confidence levels using Monte Carlo simulation.

    Example:

        mcswe forecast date --items 20 --data history.csv
    """
    try:
        # Load config and merge with CLI options
        config = load_config()

        sim_config = SimulationConfig(
            num_simulations=simulations or config.num_simulations,
            confidence_levels=confidence or tuple(config.confidence_levels),
            exclude_weekends=(
                exclude_weekends if exclude_weekends is not None else config.exclude_weekends
            ),
        )

        # Parse date filters from config
        date_from = None
        date_to = None
        if config.date_from:
            date_from = datetime.strptime(config.date_from, "%Y-%m-%d").date()
        if config.date_to:
            date_to = datetime.strptime(config.date_to, "%Y-%m-%d").date()

        # Load and process data
        work_items = load_csv(data, date_from=date_from, date_to=date_to)

        # Apply sample size limit
        if config.sample_size_limit and len(work_items) > config.sample_size_limit:
            work_items = work_items[-config.sample_size_limit :]

        if ctx.obj.get("verbose"):
            click.echo(f"Loaded {len(work_items)} work items from {data}")

        # Calculate throughput
        throughput = calculate_throughput(
            work_items, exclude_weekends=sim_config.exclude_weekends
        )

        # Run simulation
        result = forecast_date(
            throughput=throughput,
            items_remaining=items,
            start_date=start_date,
            config=sim_config,
        )

        # Format output
        historical_count = len(work_items)
        historical_range = throughput.date_range

        if output_json:
            output = format_date_forecast_json(result, historical_count, historical_range)
        else:
            output = format_date_forecast_text(
                result,
                historical_count,
                historical_range,
                show_histogram=not no_histogram and config.show_histogram,
                histogram_buckets=config.histogram_buckets,
            )

        click.echo(output)

    except DataLoadError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@forecast.command("scope")
@click.option(
    "--target-date",
    "-t",
    required=True,
    type=DATE,
    help="Target completion date (YYYY-MM-DD)",
)
@click.option(
    "--data", "-d", required=True, type=click.Path(exists=True), help="Path to CSV data file"
)
@click.option(
    "--start-date",
    type=DATE,
    default=None,
    help="Forecast start date (default: today)",
)
@click.option(
    "--simulations",
    "-n",
    type=int,
    default=None,
    help="Number of simulations (default: 10000)",
)
@click.option(
    "--confidence",
    "-c",
    callback=parse_confidence_levels,
    help="Confidence levels, comma-separated (default: 50,85,95)",
)
@click.option(
    "--exclude-weekends/--include-weekends",
    default=None,
    help="Exclude weekends from calculations (default: exclude)",
)
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.option("--no-histogram", is_flag=True, help="Hide histogram in text output")
@click.pass_context
def forecast_scope_cmd(
    ctx,
    target_date: date,
    data: str,
    start_date: date | None,
    simulations: int | None,
    confidence: tuple[int, ...] | None,
    exclude_weekends: bool | None,
    output_json: bool,
    no_histogram: bool,
):
    """Forecast how many items can be completed by a date.

    Given a target date, predict how many items can be completed at various
    confidence levels using Monte Carlo simulation.

    Example:

        mcswe forecast scope --target-date 2025-03-01 --data history.csv
    """
    try:
        # Load config and merge with CLI options
        config = load_config()

        sim_config = SimulationConfig(
            num_simulations=simulations or config.num_simulations,
            confidence_levels=confidence or tuple(config.confidence_levels),
            exclude_weekends=(
                exclude_weekends if exclude_weekends is not None else config.exclude_weekends
            ),
        )

        # Parse date filters from config
        date_from = None
        date_to = None
        if config.date_from:
            date_from = datetime.strptime(config.date_from, "%Y-%m-%d").date()
        if config.date_to:
            date_to = datetime.strptime(config.date_to, "%Y-%m-%d").date()

        # Load and process data
        work_items = load_csv(data, date_from=date_from, date_to=date_to)

        # Apply sample size limit
        if config.sample_size_limit and len(work_items) > config.sample_size_limit:
            work_items = work_items[-config.sample_size_limit :]

        if ctx.obj.get("verbose"):
            click.echo(f"Loaded {len(work_items)} work items from {data}")

        # Calculate throughput
        throughput = calculate_throughput(
            work_items, exclude_weekends=sim_config.exclude_weekends
        )

        # Run simulation
        result = forecast_scope(
            throughput=throughput,
            target_date=target_date,
            start_date=start_date,
            config=sim_config,
        )

        # Format output
        historical_count = len(work_items)
        historical_range = throughput.date_range

        if output_json:
            output = format_scope_forecast_json(result, historical_count, historical_range)
        else:
            output = format_scope_forecast_text(
                result,
                historical_count,
                historical_range,
                show_histogram=not no_histogram and config.show_histogram,
                histogram_buckets=config.histogram_buckets,
            )

        click.echo(output)

    except DataLoadError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def validate(file: str, output_json: bool):
    """Validate a CSV data file.

    Checks that the file has the required columns and valid data.

    Example:

        mcswe validate history.csv
    """
    result = validate_csv(file)

    if output_json:
        output = format_validation_json(result)
    else:
        output = format_validation_text(result)

    click.echo(output)

    if not result["valid"]:
        sys.exit(1)


@main.group()
def config():
    """Manage configuration."""
    pass


@config.command("show")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def config_show(output_json: bool):
    """Show current configuration.

    Displays the active configuration from the config file,
    or defaults if no config file exists.
    """
    import json as json_module

    try:
        cfg = load_config()
        config_path = DEFAULT_CONFIG_PATH if DEFAULT_CONFIG_PATH.exists() else None

        if output_json:
            data = cfg.to_dict()
            data["_config_file"] = str(config_path) if config_path else None
            click.echo(json_module.dumps(data, indent=2))
        else:
            click.echo(format_config_text(cfg.to_dict(), str(config_path) if config_path else None))

    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@config.command("init")
@click.option("--force", "-f", is_flag=True, help="Overwrite existing config file")
def config_init(force: bool):
    """Create a default configuration file.

    Creates a config file at ~/.config/montecarlo-swe/config.toml
    with default settings and documentation.
    """
    config_path = DEFAULT_CONFIG_PATH

    if config_path.exists() and not force:
        click.echo(f"Config file already exists at {config_path}")
        click.echo("Use --force to overwrite")
        sys.exit(1)

    # Create directory if needed
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Write template
    config_path.write_text(get_default_config_template())

    click.echo(f"Created config file at {config_path}")


if __name__ == "__main__":
    main()
