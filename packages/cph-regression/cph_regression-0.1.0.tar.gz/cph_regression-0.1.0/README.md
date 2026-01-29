# CPH Regression

A generic, config-driven regression training package using PyTorch Lightning. Train regression models on any tabular dataset by simply providing a YAML configuration file.

## Features

- **Fully Config-Driven**: All settings (features, hyperparameters, paths) controlled via YAML files
- **Generic & Reusable**: Use the same codebase for any regression task (gemstone prices, house prices, etc.)
- **Auto-Dimension Detection**: Automatically calculates input dimensions from feature lists
- **Production-Ready**: Exports models to ONNX format with preprocessors for easy deployment
- **PyTorch Lightning**: Built on PyTorch Lightning for scalable, professional ML training

## Installation

```bash
pip install cph-regression
```

## Quick Start

### 1. Create a Configuration File

Create a `config.yaml` file:

```yaml
# Your Project Configuration
seed_everything: true

trainer:
  callbacks:
    - class_path: lightning.pytorch.callbacks.ModelCheckpoint
      init_args:
        filename: "{epoch}-{val_loss:.2f}.best"
        monitor: "val_loss"
        mode: "min"
        save_top_k: 1
    - class_path: cph_regression.regression.callbacks.ONNXExportCallback
      init_args:
        output_dir: "models"
        model_name: "my_model"
        input_dim: null  # Auto-detected

  logger:
    class_path: lightning.pytorch.loggers.TensorBoardLogger
    init_args:
      save_dir: "lightning_logs"
      name: "MyProjectTraining"

  max_epochs: 50
  accelerator: auto
  devices: auto
  precision: 16-mixed

model:
  class_path: cph_regression.regression.modelmodule.ModelModuleRGS
  init_args:
    lr: 0.0001
    model:
      class_path: cph_regression.regression.modelfactory.RegressionModel
      init_args:
        input_dim: 0  # Auto-set from datamodule
        hidden_layers: [128, 64, 32]
        dropout_rates: [0.15, 0.1, 0.05]
        activation: "relu"

optimizer: 
  class_path: torch.optim.Adam
  init_args:
    lr: 0.001

data:
  class_path: cph_regression.regression.datamodule.DataModuleRGS
  init_args:
    csv_path: "data/your_data.csv"
    batch_size: 256
    val_split: 0.2
    categorical_cols:
      - column1
      - column2
    numeric_cols:
      - column3
      - column4
    target_col: "target"
    save_preprocessor: true
    preprocessor_path: "models/preprocessor.joblib"

fit:
  ckpt_path: null

test:
  ckpt_path: best
```

### 2. Run Training

```bash
cph-regression --config config.yaml
```

This will:
- Train the model
- Run validation
- Export the model to ONNX format
- Save the preprocessor

### 3. Alternative Commands

**Training only:**
```bash
cph-regression fit --config config.yaml
```

**Testing only:**
```bash
cph-regression test --config config.yaml
```

## Configuration Guide

### Data Configuration

- `csv_path`: Path to your CSV file
- `batch_size`: Batch size for training (default: 256)
- `val_split`: Validation split ratio (0.0 to 1.0, default: 0.2)
- `categorical_cols`: List of categorical feature column names
- `numeric_cols`: List of numeric feature column names
- `target_col`: Name of the target column to predict
- `preprocessor_path`: Where to save/load the preprocessor

### Model Configuration

- `hidden_layers`: List of hidden layer sizes, e.g., `[128, 64, 32]`
- `dropout_rates`: List of dropout rates matching hidden layers, e.g., `[0.15, 0.1, 0.05]`
- `activation`: Activation function (`"relu"`, `"tanh"`, `"gelu"`, `"sigmoid"`, `"leaky_relu"`, `"elu"`)
- `input_dim`: Automatically set from datamodule (set to `0` in config)

### Trainer Configuration

- `max_epochs`: Number of training epochs
- `precision`: Training precision (`"16-mixed"`, `"32"`, `"bf16-mixed"`)
- `accelerator`: Hardware accelerator (`"auto"`, `"gpu"`, `"cpu"`)
- `devices`: Number of devices (`"auto"`, `1`, `[0, 1]`)

## Output Files

After training, you'll find:

1. **Models Directory** (`models/`):
   - `your_model_name.onnx`: ONNX model for inference
   - `preprocessor.joblib`: Fitted preprocessor for data transformation

2. **Checkpoints** (`lightning_logs/YourProjectTraining/version_X/checkpoints/`):
   - `epoch-X-val_loss=Y.best.ckpt`: Best model checkpoint
   - `epoch-X.last.ckpt`: Last epoch checkpoint

3. **Training Logs** (`lightning_logs/`):
   - TensorBoard logs for visualization

## Model Inference

After training, use the exported ONNX model and preprocessor:

```python
import joblib
import onnxruntime as ort
import numpy as np
import pandas as pd

# Load preprocessor
preprocessor = joblib.load("models/preprocessor.joblib")

# Load ONNX model
session = ort.InferenceSession("models/your_model_name.onnx")

# Prepare input data
input_data = pd.DataFrame({
    'categorical_col': ['value1'],
    'numeric_col': [123.45],
    # ... other features
})

# Transform data
feature_cols = ['categorical_col', 'numeric_col']  # Your feature columns
transformed = preprocessor.transform(input_data[feature_cols])

# Predict
input_name = session.get_inputs()[0].name
output = session.run(None, {input_name: transformed.astype(np.float32)})
prediction = output[0][0][0]

print(f"Prediction: {prediction}")
```

## Viewing Training Progress

### TensorBoard

```bash
tensorboard --logdir lightning_logs
```

Then open `http://localhost:6006` in your browser.

## Example Projects

### Gemstone Price Prediction

See the [GemstonePricePrediction](https://github.com/imchandra11/cph-regression/tree/main/GemstonePricePrediction) directory for a complete example.

## Requirements

- Python >= 3.8
- PyTorch >= 2.0.0
- PyTorch Lightning >= 2.1.0

See `requirements.txt` for the complete list of dependencies.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Repository

- **GitHub**: https://github.com/imchandra11/cph-regression
- **Author**: chandra

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions:
1. Check the configuration file syntax
2. Verify CSV file format and column names
3. Check TensorBoard logs for training insights
4. Open an issue on [GitHub](https://github.com/imchandra11/cph-regression/issues)
