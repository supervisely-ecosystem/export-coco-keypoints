import os

import numpy as np
import supervisely as sly
from supervisely.geometry import graph


def create_project_dir(project):
    result_dir_name = f"{project.id}_{project.name}"
    result_dir = os.path.join(sly.app.get_data_dir(), result_dir_name)
    sly.fs.mkdir(result_dir)
    return result_dir


def create_coco_dataset(project_dir, dataset_name):
    dataset_dir = os.path.join(project_dir, dataset_name)
    sly.fs.mkdir(dataset_dir)
    ann_dir = os.path.join(dataset_dir, "annotations")
    sly.fs.mkdir(ann_dir)
    img_dir = os.path.join(dataset_dir, "images")
    sly.fs.mkdir(img_dir)
    return img_dir, ann_dir


def check_sly_annotations(ann_info, img_info, meta):
    try:
        ann = sly.Annotation.from_json(ann_info.annotation, meta)
    except:
        return sly.Annotation(img_info.height, img_info.width)
    new_labels = []
    bad_labels = []
    for lbl in ann.labels:
        if lbl.obj_class.geometry_type != graph.GraphNodes:
            bad_labels.append(lbl)
        else:
            new_labels.append(lbl)

    if len(bad_labels) > 0:
        sly.logger.warning(
            f"{len(bad_labels)} objects with unsupported geometries in image [ID: {img_info.id}, NAME: {img_info.name}]"
        )
    return ann.clone(labels=new_labels)


def get_categories_map_from_meta(meta):
    obj_classes = meta.obj_classes
    categories_mapping = {}
    idx = 0
    for obj_class in obj_classes:
        if obj_class.geometry_type != graph.GraphNodes:
            continue
        categories_mapping[obj_class.name] = idx + 1
        idx += 1
    return categories_mapping


def get_keypoints_and_skeleton(obj_class):
    nodes = list(obj_class.geometry_config["nodes"].keys())
    edges = obj_class.geometry_config["edges"]
    skeleton = []
    for edge in edges:
        skeleton.append([nodes.index(edge["src"]) + 1, nodes.index(edge["dst"]) + 1])
    return nodes, skeleton


def get_categories_from_meta(meta: sly.ProjectMeta):
    obj_classes = meta.obj_classes
    categories = []
    idx = 0
    for obj_class in obj_classes:
        if obj_class.geometry_type != graph.GraphNodes:
            continue
        keypoints, skeleton = get_keypoints_and_skeleton(obj_class)
        categories.append(
            dict(
                supercategory=obj_class.name,
                id=idx + 1,  # supercategory id
                name=obj_class.name,
                keypoints=keypoints,  # list[str]
                skeleton=skeleton,  # list[list[int]]
            )
        )
        idx += 1
    return categories


def coco_bbox(label):
    bbox = label.geometry.to_bbox()
    bbox: sly.Rectangle
    return [float(bbox.left), float(bbox.top), float(bbox.width), float(bbox.height)]


def create_coco_annotation(
    coco_ann,
    label_id,
    meta,
    dataset,
    categories_mapping,
    user_name,
    image_infos,
    anns,
    progress,
):
    if len(coco_ann) == 0:
        coco_ann = dict(
            info=dict(
                description=dataset.description,
                url="None",
                version=str(1.0),
                year=int(dataset.created_at[:4]),
                contributor=user_name,
                date_created=dataset.created_at,
            ),
            licenses=[dict(url="None", id=0, name="None")],
            images=[
                # license, url, file_name, height, width, date_captured, id
            ],
            # type="instances",
            annotations=[
                # segmentation, area, iscrowd, image_id, bbox, category_id, id
            ],
            categories=get_categories_from_meta(meta),  # supercategory, id, name
        )

    for image_info, ann in zip(image_infos, anns):
        coco_ann["images"].append(
            dict(
                license="None",
                file_name=image_info.name,
                url="None",  # image_info.full_storage_url,  # coco_url, flickr_url
                height=image_info.height,
                width=image_info.width,
                date_captured=image_info.created_at,
                id=image_info.id,
            )
        )

        for label in ann.labels:
            if label.obj_class.geometry_type != graph.GraphNodes:
                continue
            label: sly.Label
            nodes = label.geometry.nodes
            keypoints = []
            keypoint_names, sk = get_keypoints_and_skeleton(label.obj_class)
            for key in keypoint_names:
                if key not in nodes:
                    keypoints.extend([0, 0, 0])
                    continue
                keypoints.append(nodes[key].location.col)
                keypoints.append(nodes[key].location.row)
                keypoints.append(2)

            try:
                bbox = coco_bbox(label)
            except:
                bbox = []

            x = keypoints[0::3]
            y = keypoints[1::3]
            x0, x1, y0, y1 = (
                int(np.min(x)),
                int(np.max(x)),
                int(np.min(y)),
                int(np.max(y)),
            )
            # area = 0 if label.geometry == graph.GraphNodes else label.geometry.area
            area = (x1 - x0) * (y1 - y0)

            label_id += 1
            coco_ann["annotations"].append(
                dict(
                    segmentation=[],  # a list of polygon vertices around the object, but can also be a run-length-encoded (RLE) bit mask
                    area=area,  # Area is measured in pixels (e.g. a 10px by 20px box would have an area of 200)
                    iscrowd=0,  # Is Crowd specifies whether the segmentation is for a single object or for a group/cluster of objects
                    image_id=image_info.id,  # The image id corresponds to a specific image in the dataset
                    bbox=bbox,  # he COCO bounding box format is [top left x position, top left y position, width, height]
                    category_id=categories_mapping[
                        label.obj_class.name
                    ],  # The category id corresponds to a single category specified in the categories section
                    id=label_id,  # Each annotation also has an id (unique to all other annotations in the dataset)
                    keypoints=keypoints,  #: [x1,y1,v1,...] length 3k array where k is the total number of keypoints defined for the category. x,y – 0-indexed location; v is a visibility flag (v=0: not labeled, in which case x=y=0; v=1: labeled but not visible; and v=2: labeled and visible).
                    num_keypoints=len(
                        keypoint_names
                    ),  # int, indicates the number of labeled keypoints (v>0) for a given object
                )
            )
        progress.iter_done_report()

    return coco_ann, label_id
