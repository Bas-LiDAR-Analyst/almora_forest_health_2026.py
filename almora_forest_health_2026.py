import ee
# ఎర్త్ ఇంజిన్ అథెంటికేషన్ మరియు ఇనిషియలైజేషన్
ee.Authenticate()
ee.Initialize(project='my-first-ndvi-project') # మీ ప్రాజెక్ట్ ఐడి ఇవ్వండి
# అల్మోరా లొకేషన్ సెట్ చేయడం
almora_roi = ee.Geometry.Point([79.67, 29.63]).buffer(5000)

# 2020 మరియు 2026 డేటాను ఆటోమేటిక్‌గా ఫిల్టర్ చేయడం
def get_ndvi(year_range):
    return ee.ImageCollection('COPERNICUS/S2_SR') \
        .filterBounds(almora_roi) \
        .filterDate(year_range[0], year_range[1]) \
        .sort('CLOUDY_PIXEL_PERCENTAGE') \
        .first() \
        .normalizedDifference(['B8', 'B4'])

ndvi_2020 = get_ndvi(['2020-01-01', '2020-12-31'])
ndvi_2026 = get_ndvi(['2026-01-01', '2026-04-15'])

# Forest Loss (NDVI తగ్గుదల) గుర్తించడం
forest_loss = ndvi_2020.subtract(ndvi_2026).gt(0.2)
import geemap

# మ్యాప్ క్రియేట్ చేయడం
Map = geemap.Map()
Map.centerObject(almora_roi, 13)

# శాటిలైట్ లేయర్లు యాడ్ చేయడం
Map.addLayer(ndvi_2020, {'min': 0, 'max': 1, 'palette': ['white', 'green']}, 'Forest 2020')
Map.addLayer(ndvi_2026, {'min': 0, 'max': 1, 'palette': ['white', 'green']}, 'Forest 2026')

# Forest Loss ని ఎరుపు రంగులో చూపించడం
Map.addLayer(forest_loss.selfMask(), {'palette': 'red'}, 'Automated Forest Loss')

Map
# Forest loss area లెక్కించడం (Square Meters లో)
area_image = forest_loss.multiply(ee.Image.pixelArea())
stats = area_image.reduceRegion(
    reducer=ee.Reducer.sum(),
    geometry=almora_roi,
    scale=10,
    maxPixels=1e9
)

# హెక్టార్లలోకి మార్చడం (1 హెక్టారు = 10,000 చ.మీ)
loss_sqm = stats.get('nd').getInfo()
loss_hectares = loss_sqm / 10000

print(f"Total Forest Loss in Almora Region (2020-2026): {loss_hectares:.2f} Hectares")
import matplotlib.pyplot as plt

labels = ['Forest Cover 2020', 'Forest Cover 2026']
# ఉదాహరణకు NDVI సగటు విలువలు అనుకుందాం
values = [ndvi_2020.reduceRegion(ee.Reducer.mean(), almora_roi, 10).get('nd').getInfo(),
          ndvi_2026.reduceRegion(ee.Reducer.mean(), almora_roi, 10).get('nd').getInfo()]

plt.bar(labels, values, color=['green', 'orange'])
plt.ylabel('Mean NDVI Value')
plt.title('Vegetation Health Decline in Almora')
plt.show()
import matplotlib.pyplot as plt

# మీ ఏరియా సగటు NDVI విలువలను తీసుకుందాం (Mean NDVI)
forest_2020 = ndvi_2020.reduceRegion(ee.Reducer.mean(), almora_roi, 10).get('nd').getInfo()
forest_2026 = ndvi_2026.reduceRegion(ee.Reducer.mean(), almora_roi, 10).get('nd').getInfo()

labels = ['Forest Health 2020', 'Forest Health 2026']
values = [forest_2020, forest_2026]

plt.figure(figsize=(8, 5))
plt.bar(labels, values, color=['#2ecc71', '#e67e22']) # Green vs Orange
plt.ylabel('Mean NDVI (Vegetation Index)')
plt.title('Automated Forest Health Decline Analysis: Almora (2020-2026)')
plt.ylim(0, 1) # NDVI scale 0 to 1

# వాల్యూస్ ని బార్స్ పైన చూపించడం
for i, v in enumerate(values):
    plt.text(i, v + 0.02, f"{v:.3f}", ha='center', fontWeight='bold')

plt.show()
