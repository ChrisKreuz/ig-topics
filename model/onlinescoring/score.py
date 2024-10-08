import os
import logging
import json
import numpy as np


class DummyModel:
    def __init__(self, classes):
        self.classes = classes

    def predict(self, input_str):
        input_hash = hash(input_str)

        np.random.seed(input_hash % 200000)

        num_topics = np.random.randint(2, 6)

        sampled_classes = np.random.choice(self.classes, size=num_topics)

        probs = np.random.dirichlet(alpha=[0.5] * len(sampled_classes))

        return {
            cls: probs[cls_idx] for cls_idx, cls in enumerate(sampled_classes)
        }


def init():
    global model

    classes_path = os.path.join(
        os.getenv("AZUREML_MODEL_DIR"), "model/topics.json"
    )

    with open(classes_path) as f:
        classes = json.load(f)

    model = DummyModel(classes=classes)

    logging.info("Init complete")


def run(raw_data):
    logging.info("Request received")

    data_json = json.loads(raw_data)

    result_dict = {}

    if "data" in data_json.keys():
        input_str = data_json["data"]
        model_output = model.predict(input_str)
        result_dict["document_topics"] = model_output

    if "return_topics" in data_json and data_json["return_topics"]:
        result_dict["all_topics"] = model.classes

    logging.info("Request processed")

    return result_dict
