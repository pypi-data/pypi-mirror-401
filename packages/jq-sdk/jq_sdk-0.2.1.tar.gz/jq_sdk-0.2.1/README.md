# JQ-SDK

A comprehensive Python package for sensor data acquisition and visualization.

## Features

### Static Visualization
- Convert 1D arrays (1024 elements) into 32x32 heatmap visualizations
- Interactive Plotly-based heatmaps
- 10 beautiful pre-configured color schemes
- Simple and intuitive API

### Realtime Serial Acquisition (New in v0.2.0)
- Realtime data acquisition from 32x32 sensor arrays via serial port
- Multi-process architecture for high performance
- Data processing pipeline: wire order adjustment + interpolation
- Real-time heatmap rendering with matplotlib
- FPS monitoring and statistics display

## Installation

### Basic Installation (Static visualization only)

```bash
pip install jq-sdk
```

### Full Installation (Including serial acquisition)

```bash
pip install jq-sdk[serial]
```

Or install all features:

```bash
pip install jq-sdk[all]
```

### Install from source

```bash
git clone https://github.com/yourusername/JQ-SDK.git
cd JQ-SDK
pip install -e ".[serial]"
```

## Quick Start

### Static Heatmap Visualization

```python
import jq_sdk

# Create sample data (1024 elements)
data = list(range(1, 1025))

# Plot with default color scheme (viridis)
fig = jq_sdk.plot_heatmap(data)
fig.show()

# Use a different color scheme
fig = jq_sdk.plot_heatmap(data, colorscheme='plasma')
fig.show()

# Customize the plot
fig = jq_sdk.plot_heatmap(
    data,
    colorscheme='hot',
    title='My Custom Heatmap',
    width=1000,
    height=1000
)
fig.show()
```

### Realtime Serial Acquisition (New!)

```python
import jq_sdk
import multiprocessing as mp

if __name__ == "__main__":
    # Windows platform required
    mp.set_start_method('spawn', force=True)

    # One-line start (interactive port selection)
    jq_sdk.start_realtime_acquisition()

    # Or specify port and configuration
    jq_sdk.start_realtime_acquisition(
        port='COM3',
        colormap='hot',
        figsize=(10, 10)
    )
```

**Note**: Serial acquisition requires installation with `pip install jq-sdk[serial]`

## Available Color Schemes

JQ-SDK provides 10 beautiful color schemes:

- `viridis` (default) - Purple to yellow gradient
- `plasma` - Dark purple to yellow gradient
- `hot` - Black to red to yellow
- `blues` - White to dark blue
- `reds` - White to dark red
- `greens` - White to dark green
- `rainbow` - Full spectrum rainbow
- `inferno` - Black to purple to yellow
- `magma` - Black to purple to white
- `cividis` - Colorblind-friendly blue to yellow

You can get the list programmatically:

```python
import jq_sdk

schemes = jq_sdk.get_available_colorschemes()
print(schemes)
```

## API Reference

### `plot_heatmap(data, colorscheme='viridis', title='Heatmap Visualization', show_colorbar=True, width=800, height=800)`

Plot a 1x1024 matrix as a 32x32 heatmap.

**Parameters:**

- `data` (list or numpy.ndarray): Input data with exactly 1024 elements
- `colorscheme` (str, optional): Color scheme name. Default is 'viridis'
- `title` (str, optional): Title of the heatmap. Default is 'Heatmap Visualization'
- `show_colorbar` (bool, optional): Whether to show the colorbar. Default is True
- `width` (int, optional): Width of the figure in pixels. Default is 800
- `height` (int, optional): Height of the figure in pixels. Default is 800

**Returns:**

- `plotly.graph_objects.Figure`: Plotly figure object. Call `.show()` to display.

**Raises:**

- `ValueError`: If input data does not contain exactly 1024 elements
- `KeyError`: If an invalid colorscheme is specified

### `get_available_colorschemes()`

Get a list of available color schemes.

**Returns:**

- `list`: List of available colorscheme names

## Examples

### Basic Usage

```python
import jq_sdk
import numpy as np

# Using a list
data = list(range(1024))
fig = jq_sdk.plot_heatmap(data)
fig.show()

# Using numpy array
data = np.random.rand(1024)
fig = jq_sdk.plot_heatmap(data, colorscheme='plasma')
fig.show()
```

### Comparing Different Color Schemes

```python
import jq_sdk
import numpy as np

# Generate sample data
data = np.sin(np.linspace(0, 4*np.pi, 1024))

# Try different color schemes
for scheme in ['viridis', 'plasma', 'hot', 'rainbow']:
    fig = jq_sdk.plot_heatmap(
        data,
        colorscheme=scheme,
        title=f'Heatmap with {scheme} colorscheme'
    )
    fig.show()
```

### Saving to File

```python
import jq_sdk

data = list(range(1, 1025))
fig = jq_sdk.plot_heatmap(data, colorscheme='viridis')

# Save as HTML
fig.write_html('heatmap.html')

# Save as PNG (requires kaleido)
# pip install kaleido
fig.write_image('heatmap.png')
```

## Requirements

### Basic Installation
- Python >= 3.7
- numpy >= 1.19.0
- plotly >= 5.0.0

### Serial Acquisition (Optional)
- pyserial >= 3.5
- matplotlib >= 3.3.0
- scipy >= 1.5.0

## Serial Acquisition Examples

### Basic Usage

See [examples/basic_serial_acquisition.py](examples/basic_serial_acquisition.py):

```python
import jq_sdk
import multiprocessing as mp

if __name__ == "__main__":
    mp.set_start_method('spawn', force=True)
    jq_sdk.start_realtime_acquisition()
```

### Custom Configuration

See [examples/custom_configuration.py](examples/custom_configuration.py):

```python
jq_sdk.start_realtime_acquisition(
    port='COM3',
    baudrate=1000000,
    colormap='plasma',
    figsize=(10, 10)
)
```

### Low-Level API

See [examples/low_level_api.py](examples/low_level_api.py) for advanced usage with manual control of each processing step.

## Data Processing Pipeline

For 32x32 sensor arrays, the data processing pipeline is:

1. **Serial Reception**: Read 1024 bytes from serial port
2. **Frame Sync**: Find frame tail markers (0xAA 0x55 0x03 0x99)
3. **Reshape**: Convert to 32x32 matrix
4. **Wire Order Adjustment**: Apply row/column mapping to get 16x16 physical layout
5. **Interpolation**: Bilinear interpolation to upsample back to 32x32
6. **Statistics**: Calculate median, mean, max, min, valid points count
7. **Visualization**: Real-time matplotlib rendering with blitting

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please file an issue on the [GitHub issue tracker](https://github.com/yourusername/JQ-SDK/issues).

## Changelog

### 0.2.0 (Current)

- **New Feature**: Realtime serial data acquisition and visualization
  - Multi-process architecture for high performance
  - Data processing pipeline with wire order adjustment and interpolation
  - Real-time matplotlib heatmap rendering
  - FPS monitoring and statistics display
- Modular architecture: separate modules for serial, processing, visualization, and pipeline
- Optional dependencies: serial features can be installed separately
- New examples and documentation for serial acquisition
- Version upgrade to 0.2.0

### 0.1.0 (Initial Release)

- Initial release with basic heatmap visualization
- Support for 10 color schemes
- Interactive Plotly-based visualizations
- Python 3.7+ support
