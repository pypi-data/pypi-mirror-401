# Label Studio Anoter
Label Studio SDK wapper for Create project, Load dataset, Pre-annotation with YOLO Models and Export annotated data

## Install
```bash
conda create -n label-studio-anoter python=3.10 -y
conda activate label-studio-anoter
```
```bash
pip install label-studio-anoter
```
## Start Label-Studio Docker
```bash
docker run -it --rm -p 192.168.3.27:8080:8080 \
       --user root -v $(pwd)/my-label-studio:/label-studio/data \
       --env LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true \
       --env LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/label-studio/files \
       -v $(pwd)/my-files:/label-studio/files \
       heartexlabs/label-studio:latest
```
## Quick Start

```python
from label_studio_anoter import LabelStudioAnoter

# Replace with your URL and API KEY
LABEL_STUDIO_URL = 'http://192.168.3.27:8080'
LABEL_STUDIO_API_KEY = 'f8c902ab62bc78bae6fkjfh89rqcb0erwtredca4b2'

label_studio_anoter = LabelStudioAnoter(LABEL_STUDIO_URL, LABEL_STUDIO_API_KEY)

# Check User Details
user = label_studio_anoter.label_studio_user()
```
```python
# Create project
project_title = "COCO Project"
label_config = """
<View>
    <Image name="img" value="$image" zoom="true" width="100%" maxWidth="800" brightnessControl="true" contrastControl="true" gammaControl="true" />
    <RectangleLabels name="label" toName="img">
        <Label value="person"/>
        <Label value="bottle"/>
        <Label value="spoon"/>
        <Label value="teddy bear"/>
        <Label value="hair drier"/>
        <Label value="toothbrush"/>
    </RectangleLabels>
</View>
"""
project = label_studio_anoter.create_project(project_title, label_config)
```
```python
# Load YOLO Model
label_studio_anoter.load_model("yolo11m.pt")

# Create project with YOLO Model
project = label_studio_anoter.create_project_with_model("YOLOv11 Pre-Annotated Project")

storage = label_studio_anoter.import_data(project, path="/label-studio/files/images")
```
```python
# Load project from project ID
PROJECT_ID = 20
project = label_studio_anoter.get_project(PROJECT_ID)
```
```python
# Load YOLO Model
label_studio_anoter.load_model("yolov8n.pt")

# Pre-annotate with YOLO Model
label_studio_anoter.pre_annotate(project, conf=0.25)
```
```python
# Export to YOLO Format
PROJECT_ID = 23
label_studio_anoter.export_yolo(PROJECT_ID, "Exported_YOLOv11_Project")
```
