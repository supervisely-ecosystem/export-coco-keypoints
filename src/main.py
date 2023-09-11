import ast
import json
import os
from distutils.util import strtobool

import supervisely as sly
from dotenv import load_dotenv

import functions as f

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))


USER_NAME = "Supervisely User"
selected_output = os.environ["modal.state.selectedOutput"]
selected_filter = os.environ["modal.state.selectedFilter"]
all_datasets = bool(strtobool(os.getenv("modal.state.allDatasets")))
selected_datasets = ast.literal_eval(os.environ.get("modal.state.datasets", []))


class MyExport(sly.app.Export):
    def process(self, context: sly.app.Export.Context):
        api = sly.Api.from_env()

        project = api.project.get_info_by_id(id=context.project_id)
        if context.dataset_id is not None:
            datasets = [api.dataset.get_info_by_id(context.dataset_id)]
        elif len(selected_datasets) > 0 and not all_datasets:
            datasets = [
                api.dataset.get_info_by_id(dataset_id)
                for dataset_id in selected_datasets
            ]
        else:
            datasets = api.dataset.get_list(project.id)

        project_meta = sly.ProjectMeta.from_json(api.project.get_meta(project.id))
        categories_mapping = f.get_categories_map_from_meta(project_meta)

        result_dir = f.create_project_dir(project)

        label_id = 0
        for dataset in datasets:
            img_dir, ann_dir = f.create_coco_dataset(result_dir, dataset.name)

            images = api.image.get_list(dataset.id)

            if selected_filter == "annotated":
                images = [
                    image
                    for image in images
                    if image.labels_count > 0 or len(image.tags) > 0
                ]

            coco_ann = {}

            pbar = sly.Progress(f"Converting dataset: {dataset.name}", total_cnt=len(images))
            for batch in sly.batched(images):
                image_ids = [image.id for image in batch]
                ann_infos = api.annotation.download_batch(dataset.id, image_ids)
                img_paths = [os.path.join(img_dir, img_info.name) for img_info in batch]

                if selected_output == "images":
                    api.image.download_paths(dataset.id, image_ids, img_paths)

                anns = []
                for ann_info, img_info in zip(ann_infos, batch):
                    ann = f.check_sly_annotations(ann_info, img_info, project_meta)
                    anns.append(ann)

                coco_ann, label_id = f.create_coco_annotation(
                    coco_ann,
                    label_id,
                    project_meta,
                    dataset,
                    categories_mapping,
                    USER_NAME,
                    batch,
                    anns,
                    pbar,
                )

            with open(os.path.join(ann_dir, "instances.json"), "w") as file:
                json.dump(coco_ann, file)

        return result_dir


app = MyExport()
app.run()
