## Research Timeline

| Phase | Date | Event | Metrics | Evidence |
|-------|------|-------|---------|----------|
| T0 | 2026-06-06 | First AI interaction: setup, theory, protocol design |  |  |
| T1 | 2026-07-31 | First commit: 14 QPU experiments, weighted combined Z > 50 s | z_score_combined=50.0, experiments=14, backend=ibm_marrakesh | git c3ddc4a jobs: marrakesh-pasm-1  |
| T2 | 2026-08-04 | Replica 10x: Z = 39.6 sigma, shared MI 0.063 +/- 0.005 | z_score_combined=39.6, mi_shared=0.063, mi_shared_error=0.005 | jobs: marrakesh-replica-10x  |
| pivot | 2026-08-04 | Switch to phi-decoupling scan: MI modulated by phi, peak at  | mi_peak=0.047, mi_peak_error=0.004 |  |
| control | 2026-08-05 | Witness control: MI = 0.00013 (zero), cross-check with DISCO | mi_witness=0.00013, mi_qst_discord=0.728 | jobs: kingston-witness-1, marrakesh-witness-2  |
| milestone | 2026-08-06 | Scaling study: MI peaks at 3 qubits (0.159) and remains dist | mi_3q=0.159, z_distance=34.0 | git pasm-exp  |
| submission | 2026-08-07 | Submitted to JOSS (paper.md + this timeline as research prov |  |  |