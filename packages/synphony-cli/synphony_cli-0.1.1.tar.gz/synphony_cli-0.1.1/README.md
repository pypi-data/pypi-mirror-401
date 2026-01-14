# Synphony CLI

Command line interface for the Synphony robotics data platform.

## Installation

```bash
pip install synphony-cli
```

Or with pipx (recommended):

```bash
pipx install synphony-cli
```

## Quick Start

1. Get your API token from [synphony.co/settings](https://synphony.co/settings)

2. Authenticate:
```bash
synphony auth <your-token>
```

3. Initialize a project:
```bash
# Link to existing dataset
synphony init "My Dataset"

# Or create a new dataset
synphony init --new
synphony init --new "My New Dataset"
```

4. Process videos (uploads and generates augmented data):
```bash
synphony multiply *.mp4 -p "change lighting" -p "add motion blur"
```

5. Check status:
```bash
synphony status
```

6. Download results:
```bash
synphony pull
```

## Commands

| Command | Description |
|---------|-------------|
| `synphony auth <token>` | Authenticate with your API token |
| `synphony login` | Login via browser (alternative to auth) |
| `synphony whoami` | Show current authentication status |
| `synphony init <name>` | Link to existing dataset |
| `synphony init --new [name]` | Create a new dataset |
| `synphony list` | List all your datasets |
| `synphony multiply` | Upload videos and generate AI-augmented data |
| `synphony augment` | Apply traditional CV augmentations (fast) |
| `synphony status` | Check processing status |
| `synphony pull` | Download generated files |
| `synphony --version` | Show CLI version |

## Augmentations

Apply traditional computer vision augmentations (faster than AI generation):

```bash
# Simple - use default parameters
synphony augment *.mp4 --flip --rotation --jitter

# With custom parameters
synphony augment *.mp4 --rotation degrees=30,p=0.8 --jitter brightness=1.5

# Apply all augmentations
synphony augment *.mp4 --all

# Use a config file for full control
synphony augment *.mp4 --config augs.json
```

Available augmentations:
- `--flip` - Horizontal flip
- `--rotation` - Random rotation (degrees, p, resample)
- `--affine` - Affine transformation (degrees, p)
- `--perspective` - Perspective warp (distortion_scale, p)
- `--crop` - Random resized crop (size, p)
- `--noise` - Gaussian noise (mean, std, p)
- `--jitter` - Color jitter (brightness, contrast, p)
- `--erasing` - Random erasing/occlusion (p)

Example `augs.json`:
```json
[
  {"name": "RandomRotation", "params": {"degrees": 30, "p": 0.8}},
  {"name": "ColorJitter", "params": {"brightness": 1.5, "contrast": 1.2}}
]
```

## Links

- [Website](https://synphony.co)
- [Documentation](https://docs.synphony.co)
