# **AuraData — Automated Data Quality Auditing Engine**
**Author:** Abdul Mofique Siddiqui  
**License:** MIT  

**Install via pip:**
```bash
pip install auradata
```

Import it in your Python code:
```python
from auradata import Dataset
```

---

## Overview
AuraData is a data-centric auditing and diagnostics engine for machine learning datasets.

It automatically inspects datasets to detect:
* Duplicate samples
* Noisy or anomalous records
* Potentially mislabeled samples
* Subgroup performance disparities (bias risks)

AuraData is designed to be **transparent, conservative, and human-in-the-loop** — it flags risks and provides diagnostics instead of blindly modifying data.

---

## Installation
Install the package via pip:
```bash
pip install auradata
```

---

## How It Works
* **Duplicate Detection** Identifies exact row duplicates.
* **Noise Detection** Uses Isolation Forest on numeric features to flag outliers.
* **Label Issue Detection** Flags samples where the model strongly disagrees with provided labels.
* **Bias Audit** Evaluates subgroup performance disparities across sensitive attributes.
* **State Tracking** Tracks cleaning and fixing actions safely and reversibly.
* **HTML Reporting** Produces structured, readable audit reports.

---

## Getting Started

### 1. Import the package
```python
from auradata import Dataset
```

### 2. Initialize the dataset
```python
ds = Dataset(X, y)
```

### 3. Run an initial audit
```python
ds.audit(check_labels=False, check_bias=False)
```

### 4. Clean obvious issues
```python
ds.clean(remove_duplicates=True, remove_noise=True)
```

### 5. Train your model
```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000)
model.fit(ds.X.select_dtypes(include=["number"]), ds.y)
```

### 6. Run a full audit
```python
ds.audit(model=model, sensitive_feature="gender", check_duplicates=False, check_noise=False)
```

### 7. Fix label issues (optional)
```python
ds.fix_labels(model)
```

### 8. Generate a report
```python
ds.report("auradata_report.html")
```

---

## API Reference

### Dataset(X, y=None, feature_names=None)
Initializes the dataset.

**Parameters:**
* `X`: Feature matrix (array-like or DataFrame)
* `y`: Labels (optional)
* `feature_names`: Optional column names

---

### `.audit(...)`
Audits the dataset for quality issues.

---

### `.clean(...)`
Removes duplicate and/or noisy samples.

---

### `.fix_labels(model)`
Replaces mislabeled values with model predictions.

---

### `.report(path)`
Generates an HTML report summarizing all detected issues.

---

### `.restore_original()`
Restores the dataset to its original unmodified state.

---

### `.summary()`
Prints a quick console summary of the dataset state.

---

## Example Usage

```python
import numpy as np
import pandas as pd
from auradata import Dataset
from sklearn.linear_model import LogisticRegression

# Create synthetic dataset with 200 samples
np.random.seed(42)
n = 200

X = pd.DataFrame({
    "age": np.random.randint(18, 70, n),
    "income": np.random.normal(50000, 15000, n),
    "score": np.random.normal(70, 10, n),
    "gender": np.random.choice(["M", "F"], n)
})

# Create binary labels where income > 50k and score > 70 determines the class
y = ((X["income"] > 50000) & (X["score"] > 70)).astype(int).values

# Inject a duplicate row at index 1
X.iloc[1] = X.iloc[0]
y[1] = y[0]

# Inject an extreme outlier at index 5
X.loc[5, ["age", "income", "score"]] = [150, 1_000_000, 300]

# Flip labels at specific indices to simulate labeling errors
y[10] = 1 - y[10]
y[20] = 1 - y[20]
y[30] = 1 - y[30]

print("Injected issues: 1 duplicate, 1 outlier, 3 flipped labels\n")

# Initialize the AuraData wrapper
ds = Dataset(X, y)

print("STEP 1: Initial audit (duplicates & noise)")
# Check for structural issues first
ds.audit(check_labels=False, check_bias=False)

print("\nSTEP 2: Cleaning dataset")
# Remove duplicates and noise identified in the audit
ds.clean(remove_duplicates=True, remove_noise=True)

print("\nSTEP 3: Training model")
# Train a simple model on numeric columns only
model = LogisticRegression(max_iter=1000)
model.fit(ds.X.select_dtypes(include=["number"]), ds.y)

print("\nSTEP 4: Full audit (labels & bias)")
# Run model-based checks
ds.audit(
    model=model,
    sensitive_feature="gender",
    check_duplicates=False,
    check_noise=False,
    label_threshold=0.7
)

print("\nSTEP 5: Fixing labels")
# Automatically correct labels where the model is confident
ds.fix_labels(model, retrain=True, threshold=0.7)

print("\nSTEP 6: Generating reports")

# --- REPORTING OPTIONS ---

# Option 1: Generate HTML report only (This is the DEFAULT)
# ds.report("auradata_report", report_format="html")

# Option 2: Generate PDF report only
# ds.report("auradata_report", report_format="pdf")

# Option 3: Generate BOTH HTML and PDF reports
ds.report("auradata_report", report_format="both")

# -------------------------

# Print final stats to console
ds.summary()

print("\nDone! Reports generated.")
```

---

## Internals
* Isolation Forest for outlier detection
* Confidence-based disagreement for label validation
* Group-wise evaluation for bias detection
* State-aware cleaning with reversible actions
* Transparent reporting for auditability

---

## Notes
* Works with numeric and mixed datasets
* Conservative by default (no blind destructive actions)
* Designed for ML practitioners and researchers
* Suitable for responsible and regulated workflows

---

## Author
Abdul Mofique Siddiqui

---

## License
This project is licensed under the MIT License.

