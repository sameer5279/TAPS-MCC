# TAPS-MCC: Trust-Aware, Privacy-Preserving Secure Architecture for Mobile Cloud Computing

Code and data accompanying the manuscript:

> S. Awasthi, S. W. A. Rizvi, R. S. K. Boddu, A. K. Tiwari, "TAPS-MCC: A Trust-Aware, Privacy-Preserving Secure Architecture for Mobile Cloud Computing", submitted to *Cluster Computing* (Springer), 2026.

## Repository contents

| Folder | Contents | Paper section |
|---|---|---|
| `proverif/` | ProVerif 2.x model of the authentication and key-agreement protocol | Sec. 5.1, Table 6 |
| `benchmark/` | Cryptographic primitive benchmark and measured results on the mobile device and edge server | Sec. 6.2–6.3, Tables 8–9 |
| `ids/` | Google Colab notebook for the intrusion detection experiment on Edge-IIoTset, with results and figures | Sec. 6.4, Table 10, Fig. 4 |
| `simulation/` | Google Colab notebook for the trust-aware offloading simulation, with raw and summary results | Sec. 6.5, Tables 11–12, Figs. 5–7 |

## Reproducing the results

**1. Formal verification**

```
proverif proverif/taps_mcc.pv
```

All seven queries should report `true`.

**2. Cryptographic benchmark** (run on each device)

```
pip install cryptography phe
python benchmark/taps_mcc_benchmark.py
```

Measured results are in `benchmark/results/`: `mobile_motorola_edge60pro.txt` (Motorola Edge 60 Pro, MediaTek Dimensity 8350 Extreme, 12 GB RAM, Python 3.14.8) and `edge_server_ryzen5_5600h.txt` (AMD Ryzen 5 5600H, 16 GB RAM, Python 3.13.2).

**3. Intrusion detection**: open `ids/TAPS_MCC_IDS_Edge-IIoTset_v2.ipynb` in Google Colab and select *Runtime > Run all*. The notebook downloads Edge-IIoTset from Kaggle, removes the "0"/"0.0" label-leakage artefact, trains Random Forest, XGBoost, LightGBM and a 1D-CNN, and writes the results to `results/`.

**4. Offloading simulation**: open `simulation/TAPS_MCC_Offloading_Simulation.ipynb` in Google Colab and select *Runtime > Run all* (about 5 minutes). Each configuration is repeated 10 times and reported with 95% confidence intervals.

## Dataset

Edge-IIoTset: M. A. Ferrag et al., *IEEE Access* 10 (2022) 40281–40306, https://doi.org/10.1109/ACCESS.2022.3165809 (publicly available on Kaggle).

## License

MIT; see `LICENSE`.

## Contact

Corresponding author: Sameer Awasthi (sameer.awasthi@s.amity.edu)
