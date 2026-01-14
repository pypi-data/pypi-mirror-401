import wandb
import pandas as pd


def load_runs(
    entity: str,
    project: str,
    tags: list = None,
    exclude_tags: list = None,
    filters: dict = None,
    state: str = "finished",
    timeout: int = 5000,
) -> pd.DataFrame:
    """
    Loads runs from a W&B project with flexible filtering options.

    Args:
        entity: W&B entity (username or team name)
        project: W&B project name
        tags: Optional list of tags to filter runs (runs must have at least one of these tags)
        exclude_tags: Optional list of tags to exclude runs
        filters: Optional raw W&B filters dict for advanced queries
        state: Run state to filter on ("finished", "running", "crashed", etc.)
               Use "all" to include all states. Default: "finished"
        timeout: Timeout for the W&B API in seconds. Default: 5000

    Returns:
        pandas.DataFrame with run information including name, id, state, timestamps,
        tags, sweep_id, config values, and summary metrics.

    Examples:
        # Tag-based filtering (simple)
        df = load_runs("entity", "project", tags=["exp-v1"])

        # Raw filters (flexible)
        df = load_runs("entity", "project", filters={"config.lr": 0.001})

        # Combined filters
        df = load_runs("entity", "project", tags=["exp-v1"], filters={"config.lr": 0.001})

        # All states
        df = load_runs("entity", "project", tags=["exp-v1"], state="all")
    """
    # Build filters
    filter_conditions = []

    # Add tag filters if provided
    if tags is not None:
        filter_conditions.append({"tags": {"$in": tags}})
    if exclude_tags is not None:
        filter_conditions.append({"tags": {"$nin": exclude_tags}})

    # Add raw filters if provided
    if filters is not None:
        filter_conditions.append(filters)

    # Combine all filter conditions
    if len(filter_conditions) == 0:
        combined_filters = None
    elif len(filter_conditions) == 1:
        combined_filters = filter_conditions[0]
    else:
        combined_filters = {"$and": filter_conditions}

    api = wandb.Api(timeout=timeout)
    runs = api.runs(f"{entity}/{project}", filters=combined_filters)

    runs_list = []
    for run in runs:
        try:
            if state == "all" or run.state == state:
                run_info = {
                    "name": run.name,
                    "id": run.id,
                    "state": run.state,
                    "created_at": run.created_at,
                    "heartbeat_at": run.heartbeat_at,
                    "tags": run.tags,
                    "sweep_id": run.sweep.id if run.sweep else None,
                    **run.config,
                    **run.summary,
                }
                runs_list.append(run_info)
        except Exception as e:
            print(f"Error processing run {run.name} with ID {run.id}: {str(e)}")
            raise e

    runs_df = pd.DataFrame(runs_list)
    return runs_df
