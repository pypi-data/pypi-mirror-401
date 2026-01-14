# Model Training Guide

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Configure AWS and Bitbucket: `cpv aws-config && cpv bitbucket-config`

## Training
1. Prepare training data in `data/` directory
2. Update metrics logging in `train.py`
3. Run: `python train.py`

## Versioning
1. Upload checkpoint: `cpv model upload --message "Training v1"`
2. List checkpoints: `cpv model list-tags`
3. Revert to version: `cpv model revert --tag v1.0`

## Metrics
- Training metrics logged in `metrics.log`
- Model weights stored in `model.bin`
