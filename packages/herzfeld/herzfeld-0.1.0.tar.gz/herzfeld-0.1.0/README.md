# HERZFELD
**High-fidelity Epigraphic Rendering for Zonated Feature Extraction and Labelled Datasets**

HERZFELD is a specialised pipeline for generating synthetic datasets for Optical Character Recognition (OCR) of ancient inscriptions, specifically focusing on Middle Persian and Inscriptional Pahlavi.

## Why HERZFELD?
Traditional 2D synthetic data (like flat PNG/JPG images) fails to capture the complexity of epigraphy. HERZFELD leverages **Blender** and **Geometry Nodes** to produce physically accurate 3D renders of stone surfaces.

### Key Features:
* **OpenEXR Output:** Provides multi-channel "Ground Truth" data.
* **Depth Maps:** Allows AI models to distinguish between intentional carvings and natural stone erosion.
* **Surface Normals:** Facilitates training under variable raking-light conditions, mimicking field documentation.
* **Procedural Rock Generation:** Creates infinitely varied geological backgrounds for robust ML training.
