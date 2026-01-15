#  <img src="./logo.png" align="left" height="150" /></a>

<strong>SR2P</strong> is a stacking based framework for predicting spatial protein expression from spatial transcriptomics RNA profiles in spatial multi omics data.


<br> 

## 🌟 Features

 **Stacking based protein prediction:** Integrates multiple base learners and a meta learner for robust inference.

 **Spatial feature augmentation:** Enables spatial neighborhood enhanced prediction for non GNN models.

 **Flexible model benchmarking:** Supports both classical machine learning models and graph neural networks.

 **Easy to install:** Available via pip.

 **Ready for RNA only data:** Can infer protein abundance for spatial transcriptomics datasets without protein measurements.


## ⏬ Installation

We recommend using a separate Conda environment. Information about Conda and how to install it can be found in the [anaconda webpage](https://www.anaconda.com/docs/getting-started/miniconda/main).

- Create a conda environment and install the SR2P package

```bash
   conda create -n sr2p_env python=3.9
   conda activate sr2p_env

   pip install sr2p
```

The SR2P package has been installed successfully on Operating systems:

- macOS Sequoia 15.3.2
- Ubuntu 22.04
- SUSE Linux Enterprise Server 15 SP5 (Dardel HPC system)

## 📊 Data Input

SR2P uses `.h5ad` files, which are [AnnData](https://anndata.readthedocs.io/en/latest/) objects commonly used for spatial transcriptomics and spatial multi omics analysis.

#### **spatial_genomics.h5ad** (Spatial multi-omics data: RNA + protein)
- `.X`: Feature matrix (spots × features), including RNA expression and protein abundance
- `.obs`: Spot metadata
- Spatial coordinates: stored in `.obs` or `.obsm["spatial"]`

#### **st_adata.h5ad** (Spatial transcriptomics data: RNA only)
- `.X`: Gene expression matrix (spots × genes)
- `.obs`: Spot metadata
- Spatial coordinates: stored in `.obs` or `.obsm["spatial"]`

## 🔗 Example Data Download  

- Download the [Spatial Multi-Omics Data Example](https://drive.google.com/uc?export=download&id=1u166TTkRFKlr2rYbbvo9M0t4WwUayGd4). 

Example datasets used in the tutorial can be organized under:

```bash
sr2p_data/
├── human_breast_cancer_rna_protein.h5ad
├── human_tonsil_rna_protein_1.h5ad
├── human_tonsil_rna_protein_2.h5ad
└── human_glioblastoma_rna_protein.h5ad
```

## ⚙️ Usage


A complete guide is provided in this <a href="./tutorial.ipynb" target="_blank">tutorial</a>.

## 🧬 SR2P workflow

A typical SR2P workflow includes:

1. Load spatial multi omics data

2. RNA and protein preprocessing

3. Train and test matrix construction

4. Spatial neighborhood feature construction (optional)

5. Single Model training and prediction (optional)

6. Stacking based integration for final predictions

## 📌 Supported models

SR2P supports the following model families:

| Model type | Methods |
|-----------|---------|
| Linear model | PLS |
| Gradient boosting | XGBoost, LightGBM, CatBoost |
| Graph neural networks | GAT, GraphSAGE, DGAT |
| Meta learner | ExtraTrees |

## 📁 Output

SR2P returns predicted protein abundance as a `pandas.DataFrame`:

- **Rows:** spatial spots  
- **Columns:** proteins  
- **Values:** predicted protein abundance  

Predictions can be exported to CSV for downstream analysis.

## License  

GNU General Public License v3.0