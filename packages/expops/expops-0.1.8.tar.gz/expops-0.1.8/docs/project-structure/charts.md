# Chart Generation

ExpOps supports both static and dynamic chart generation for visualizing experiment results.

## Static Charts

Static charts generate PNG image files that are saved to disk.

### Configuration

Static chart scripts are configured in `configs/project_config.yaml`:

```yaml
reporting:
  static_entrypoint: "projects/my-project/charts/plot_metrics.py"
  charts:
    - name: "my_chart"
      probe_paths:
        data_source: "process_name/step_name"
```

The `static_entrypoint` path is relative to the workspace root. You can place your chart scripts anywhere and configure the path accordingly.

### Chart Functions

Functions decorated with `@chart()` generate visualizations:

```python
from mlops.reporting.registry import chart
from mlops.reporting.context import ChartContext

@chart()
def plot_metrics(context: ChartContext):
    # Access metrics from previous steps
    metrics = context.get_metrics()
    
    # Generate matplotlib plot
    import matplotlib.pyplot as plt
    plt.figure()
    # ... plotting code ...
    plt.savefig("output.png")
```

**Note**: The function name should match the chart `name` defined in `project_config.yaml`, or be registered via the `@chart()` decorator.

### Metrics Access

Charts can read metrics from previous pipeline steps via `ChartContext`:
- Access logged metrics
- Read step outputs
- Combine data from multiple steps

### Output

Static charts produce image files (PNG) saved to:
```
artifacts/charts/<run-id>/
```

## Dynamic Charts

Dynamic charts provide real-time, interactive visualizations.

### Configuration

Dynamic chart scripts are configured in `configs/project_config.yaml`:

```yaml
reporting:
  dynamic_entrypoint: "projects/my-project/charts/plot_metrics.js"
  charts:
    - name: "my_dynamic_chart"
      type: dynamic
      probe_paths:
        data_source: "process_name/step_name"
```

The `dynamic_entrypoint` path is relative to the workspace root. If not specified, the system will attempt to derive it from `static_entrypoint` by changing the `.py` extension to `.js`.

### Features

- **Real-time updates**: Charts update as metrics are logged during execution
- **Chart.js integration**: Uses Chart.js library for interactive visualizations
- **Live metrics**: Subscribes to metric streams from multiple pipeline steps
- **Web UI integration**: Rendered in the web UI for interactive exploration

### Example

```javascript
// Subscribe to metrics
subscribeToMetrics((metrics) => {
    // Update Chart.js chart
    chart.data.datasets[0].data = metrics;
    chart.update();
});
```

## Chart Dependencies

Chart dependencies are configured separately from the main project dependencies to reduce training environment overhead.

### Configuration

Chart dependencies are specified in `project_config.yaml`:

```yaml
environment:
  venv:
    reporting:
      name: "my-project-env-reporting"
      requirements_file: "projects/my-project/charts/requirements.txt"
```

The `requirements_file` path is relative to the workspace root. This allows you to:
- Keep visualization libraries separate from training dependencies
- Use minimal dependencies for chart generation
- Include libraries like matplotlib, seaborn, plotly, etc.

## Viewing Charts

### Static Charts

Static charts are saved as PNG files and can be:
- Viewed in the file system
- Displayed in the web UI

### Dynamic Charts

Dynamic charts are available in the web UI:
- Real-time updates during execution
- Interactive exploration
- Multiple chart types