import ast
import json
import os
from distutils.util import strtobool
from supervisely.io.exception_handlers import handle_exception

import supervisely as sly
from dotenv import load_dotenv

import functions as f
import workflow as w

import asyncio

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))


USER_NAME = "Supervisely User"
selected_output = os.environ["modal.state.selectedOutput"]
selected_filter = os.environ["modal.state.selectedFilter"]
all_datasets = bool(strtobool(os.getenv("modal.state.allDatasets")))
selected_datasets = ast.literal_eval(os.environ.get("modal.state.datasets", []))

api = sly.Api.from_env()


class MyExport(sly.app.Export):
    def process(self, context: sly.app.Export.Context):
        project = api.project.get_info_by_id(id=context.project_id)
        if context.dataset_id is not None:
            datasets = [api.dataset.get_info_by_id(context.dataset_id)]
            w.workflow_input(api, datasets[0].id, type="dataset")
        elif len(selected_datasets) > 0 and not all_datasets:
            datasets = [api.dataset.get_info_by_id(dataset_id) for dataset_id in selected_datasets]
            if len(datasets) == 1:
                w.workflow_input(api, datasets[0].id, type="dataset")
            else:
                w.workflow_input(api, project.id, type="project")
        else:
            datasets = api.dataset.get_list(project.id)
            w.workflow_input(api, project.id, type="project")

        project_meta = sly.ProjectMeta.from_json(api.project.get_meta(project.id))
        categories_mapping = f.get_categories_map_from_meta(project_meta)

        result_dir = f.create_project_dir(project)
        label_id = 0
        for dataset in datasets:
            img_dir, ann_dir = f.create_coco_dataset(result_dir, dataset.name)

            images = api.image.get_list(dataset.id)

            if selected_filter == "annotated":
                images = [
                    image for image in images if image.labels_count > 0 or len(image.tags) > 0
                ]

            coco_ann = {}

            if selected_output == "images":
                image_ids = [image_info.id for image_info in images]
                paths = [os.path.join(img_dir, image_info.name) for image_info in images]

                di_pbar = sly.tqdm_sly(desc=f"Downloading images", total=len(image_ids))
                coro = api.image.download_paths_async(image_ids, paths, progress_cb=di_pbar)
                loop = sly.utils.get_or_create_event_loop()
                if loop.is_running():
                    future = asyncio.run_coroutine_threadsafe(coro, loop)
                    future.result()
                else:
                    loop.run_until_complete(coro)

            da_pbar = sly.tqdm_sly(desc=f"Downloading annotaions", total=len(image_ids))
            ann_infos = f.get_anns_list(api, dataset.id, image_ids, progress_cb=da_pbar)
            anns = []

            pbar = sly.tqdm_sly(desc=f"Converting dataset {dataset.name} items", total=len(images))
            unsupported_anns = {}
            for ann_info, img_info in zip(ann_infos, images):
                ann = f.check_sly_annotations(ann_info, img_info, project_meta, unsupported_anns)
                anns.append(ann)
            if unsupported_anns:
                sly.logger.warning(
                    f"Objects with unsupported geometries for images were found: {json.dumps(unsupported_anns, indent=2)}"
                )
            coco_ann, label_id = f.create_coco_annotation(
                coco_ann,
                label_id,
                project_meta,
                dataset,
                categories_mapping,
                USER_NAME,
                images,
                anns,
                pbar,
            )

            with open(os.path.join(ann_dir, "instances.json"), "w") as file:
                json.dump(coco_ann, file)

        return result_dir


def main():
    try:
        app = MyExport()
        app.run()
        w.workflow_output(api, app.output_file)
    except Exception as e:
        exception_handler = handle_exception(e)
        if exception_handler:
            raise Exception(exception_handler.get_message_for_modal_window()) from e
        else:
            raise e
    finally:
        if not sly.is_development():
            sly.logger.info(f"Remove temp directory: {sly.app.get_data_dir()}")
            sly.fs.remove_dir(sly.app.get_data_dir())


if __name__ == "__main__":
    sly.main_wrapper("main", main)
