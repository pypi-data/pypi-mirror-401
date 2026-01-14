from label_studio_sdk import LabelStudio
from label_studio_sdk.converter import Converter
from tqdm import tqdm
from PIL import Image
import requests
import time
import os
from label_studio_anoter.logger import logger


class LabelStudioAnoter:
    """
    A class to interact with Label Studio for creating projects, importing data,
    pre-annotating using YOLO models, and exporting annotations in YOLO format.
    """
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key
        self.client = LabelStudio(base_url=url, api_key=api_key)
        self.local_files_serving_enabled = "true"
        self.local_files_document_root = "/label-studio/files/images"
        self.logger = logger
        
    def load_model(self, model_name):
        from ultralytics import YOLO
        self.model_name = model_name
        self.model = YOLO(self.model_name)
        self.logger.info(f"Model {model_name} loaded successfully.")

    def label_studio_user(self):
        # A basic request to verify connection is working
        me = self.client.users.whoami()
        self.logger.info(f"Connected to Label Studio as user: {me.username}")
        self.logger.info(f"User email: {me.email}")
        return me
    
    def create_project(self, project_title, label_config):
        project = self.client.projects.create(
            title=project_title,
            label_config=label_config,
        )
        self.logger.info(f"Project '{project_title}' created with ID: {project.id}")
        return project
    
    def get_project(self, project_id):
        project = self.client.projects.get(project_id)
        self.logger.info(f"Retrieved project '{project.title}' with ID: {project.id}")
        return project

    def generate_label_config(self):
        yolo_labels = '\n'.join([f'<Label value="{label}"/>' for label in self.model.names.values()])
        label_config = f'''
        <View>
            <Image name="img" value="$image" zoom="true" width="100%" maxWidth="800" brightnessControl="true" contrastControl="true" gammaControl="true" />
            <RectangleLabels name="label" toName="img">
            {yolo_labels}
            </RectangleLabels>
        </View>'''
        self.logger.info("Generated label configuration from model classes.")
        return label_config

    def create_project_with_model(self, project_title):
        label_config = self.generate_label_config()
        project = self.create_project(project_title, label_config)
        self.logger.info(f"Project '{project_title}' created with model-based label config.")
        return project

    def import_data(self, project, path="/label-studio/files/images"):
        storage = self.client.import_storage.local.create(
            project=project.id,
            regex_filter='.*jpg',
            path=path,
            title="pre_anot_data",
            use_blob_urls=True,
            
        )
        self.client.import_storage.local.sync(id=storage.id)
        self.logger.info(f"Imported data to project ID {project.id} from local storage.")
        return storage

    def predict_yolo(self, images, conf):
        results = self.model(images, conf=conf)
        predictions = []
        for result in results:
            img_height, img_width = result.orig_shape
            boxes = result.boxes.cpu().numpy()
            prediction = {'result': [], 'score': 0.0, 'model_version': self.model_name}
            scores = []
            for box, class_id, score in zip(boxes.xywh, boxes.cls, boxes.conf):
                x, y, w, h = box
                prediction['result'].append({
                    'from_name': 'label',
                    'to_name': 'img',
                    'original_width': int(img_width),
                    'original_height': int(img_height),
                    'image_rotation': 0,
                    'value': {
                        'rotation': 0,
                        'rectanglelabels': [result.names[class_id]],
                        'width': float(w / img_width * 100),
                        'height': float(h / img_height * 100),
                        'x': float((x - 0.5 * w) / img_width * 100),
                        'y': float((y - 0.5 * h) / img_height * 100)
                    },
                    'score': float(score),
                    'type': 'rectanglelabels',
                })
                scores.append(float(score))
            prediction['score'] = min(scores) if scores else 0.0
            predictions.append(prediction)
        self.logger.info(f"Generated predictions for {len(images)} images.")
        return predictions

    def pre_annotate(self, project, conf=0.25):
        tasks = self.client.tasks.list(project=project.id)
        for i, task in enumerate(tqdm(tasks)):
            try:
                url = f"{self.url}{task.data['image']}"
                image = Image.open(requests.get(url, headers={'Authorization': f'Token {self.api_key}'}, stream=True).raw)
                predictions = self.predict_yolo([image], conf)[0]
                self.client.predictions.create(task=task.id, result=predictions['result'], score=predictions['score'], model_version=predictions['model_version'])
            except Exception as e:
                self.logger.error(f"Error processing task ID {task.id}: {e}")
        self.logger.info(f"Pre-annotated tasks in project ID {project.id}.")

    def export_yolo(self, project_id, output_root):
        os.environ["LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED"] = self.local_files_serving_enabled
        os.environ["LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT"] = self.local_files_document_root
        os.environ["LABEL_STUDIO_URL"] = self.url
        os.environ["LABEL_STUDIO_API_KEY"] = self.api_key

        project = self.get_project(project_id)
        self.logger.info(f"Exporting project: {project.title} (ID: {project.id})")
        export = self.client.projects.exports.create(project_id, title="YOLO Full Export")
        self.logger.info("Waiting for export to complete...")
        while getattr(export, "status", "") == "in_progress":
            time.sleep(3)
            export = self.client.projects.exports.get(id=project_id, export_pk=export.id)
        self.logger.info("Export completed. Downloading data...")
        data = self.client.projects.exports.download(id=project_id, export_pk=export.id, export_type="JSON")
        snapshot_path = os.path.join(output_root, f"project_{project_id}_snapshot.json")
        os.makedirs(output_root, exist_ok=True)
        self.logger.info(f"Saving snapshot to {snapshot_path}")
        with open(snapshot_path, "wb") as f:
            for chunk in data:
                f.write(chunk)
        self.logger.info("Converting to YOLO format...")
        converter = Converter(config=project.label_config, project_dir=output_root)
        converter.convert_to_yolo(snapshot_path, output_root, is_dir=False)
        self.logger.info("YOLO export completed.")


if __name__ == "__main__":
    LABEL_STUDIO_URL = 'http://192.168.0.47:8080'
    LABEL_STUDIO_API_KEY = 'f8c902ab62bc78bae61e832cb0f17ad0abdca4b2'
    label_studio_anoter = LabelStudioAnoter(LABEL_STUDIO_URL, LABEL_STUDIO_API_KEY)
    user = label_studio_anoter.label_studio_user()
    label_studio_anoter.load_model("yolo11m.pt")
    project = label_studio_anoter.create_project_with_model("YOLOv11 Pre-Annotated Project")
    storage = label_studio_anoter.import_data(project, path="/label-studio/files/images")
    project = label_studio_anoter.get_project(project.id)
    label_studio_anoter.pre_annotate(project, conf=0.25)
    label_studio_anoter.export_yolo(20, "Exported_YOLOv11_Project")