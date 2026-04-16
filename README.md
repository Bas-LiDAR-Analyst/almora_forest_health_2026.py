
# Almora Automated Forest Health Analysis (2020-2026) 🌲🛰️

This project automates the detection of forest cover loss and vegetation health decline in the Almora region using Google Earth Engine (GEE) Python API.

## 📊 Key Findings
- **Total Forest Loss**: Automated spatial analysis detected a loss of **319.11 Hectares** in the study area between 2020 and 2026.
- **Vegetation Health Decline**: The Mean NDVI (Normalized Difference Vegetation Index) dropped from **0.36 to 0.28**, indicating significant ecological stress.

## 🛠️ Technology Stack
- **Language**: Python (Google Colab / GitHub Codespaces)
- **APIs**: Google Earth Engine (ee) Python API
- **Libraries**: `geemap` for visualization, `matplotlib` for automated charting.

## 🚀 How it Works
The script automatically fetches Sentinel-2 multi-spectral imagery, cloud-masks the data, calculates NDVI time-series, and performs zonal statistics to compute the exact area of forest loss.
