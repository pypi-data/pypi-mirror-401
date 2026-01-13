"""
fastaiv2 - custom deep learning framework based on fastai

Built-in features:
- Data interception: TabularDataLoaders.from_df stores the input data
- Prediction control: Learner.get_preds supports custom prediction logic
"""

__version__ = "1.0.0"

# Import and apply patches
from .patches import (
    apply_patches,
    get_stored_data,
    get_data_store,
    set_custom_preds_func,
    data_store,
)

apply_patches()
