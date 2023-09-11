<div align="center" markdown>
<img src="https://github.com/supervisely-ecosystem/export-coco-keypoints/assets/119248312/5777a6fb-efe5-41c3-93b9-4abe92006b77"/>

# Export COCO Keypoints

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#How-To-Use">How To Use</a> •
  <a href="#Results">Result</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/export-coco-keypoints)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/export-coco-keypoints)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/export-coco-keypoints.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/export-coco-keypoints.png)](https://supervise.ly)

</div>

# Overview

App converts [Supervisely format](https://docs.supervisely.com/data-organization/00_ann_format_navi) project to [COCO Keypoints format](https://cocodataset.org/#format-data) as a **downloadable .tar archive**.

Application key points:

- Сonverts **Supervisely** keypoints (graph) to **COCO** keypoints and bboxes.
- ⚠️ Сonverts annotations as visible keypoints (`visibility == 2`).
- Supports `graph` (`keypoints`) geometry type only. **Other geometry types will be ignored.** To convert `bitmap`, `polygon` and `rectangles` geometry types use [Export to COCO](https://ecosystem.supervisely.com/apps/export-to-coco) app or [Export to COCO mask](https://ecosystem.supervisely.com/apps/export-to-coco-mask) for `polygons` geometry type (to preserve holes in polygons).

- Backward compatible with [Import COCO keypoints](https://ecosystem.supervisely.com/apps/import-coco-keypoints)

# How to Run

**•** Go to **Ecosystem** page and find the app [Export COCO Keypoints](https://ecosystem.supervisely.com/apps/export-coco-keypoints).

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/export-coco-keypoints" img src="XXX" width="500px" style='padding-bottom: 20px'/> 

**•**  Run the application from the **Ecosystem**.

<img src="https://github.com/supervisely-ecosystem/export-to-coco-mask/assets/119248312/155055d6-1b13-4e97-8407-ffaf4f4a4fbc" />

**•** Or open the `context menu` of **Images Project** -> `Download via App` -> `Export COCO Keypoints`. 

<img src="https://github.com/supervisely-ecosystem/export-to-coco-mask/assets/119248312/155055d6-1b13-4e97-8407-ffaf4f4a4fbc" />


# How to Use

Select options in the modal window and press the `RUN` button.

<img src="https://github.com/supervisely-ecosystem/export-to-coco-mask/assets/119248312/155055d6-1b13-4e97-8407-ffaf4f4a4fbc" />


# Result

After running the application, you will be redirected to the **Workspace Tasks** page. Once application processing has finished, your link for downloading will be available. Click on the `file name` to download it.

<img src="https://github.com/supervisely-ecosystem/export-to-coco-mask/assets/119248312/155055d6-1b13-4e97-8407-ffaf4f4a4fbc" />

To explore warnings, just open `Log` in the `⋮` menu:

<img src="https://github.com/supervisely-ecosystem/export-to-coco-mask/assets/119248312/155055d6-1b13-4e97-8407-ffaf4f4a4fbc" />

You can also find your converted project in
`Team Files` -> `tmp` -> `supervisely` -> `export` -> `export-COCO-keypoints` -> `<taskId>_<projectName>.tar`

<img src="https://github.com/supervisely-ecosystem/export-to-coco-mask/assets/119248312/155055d6-1b13-4e97-8407-ffaf4f4a4fbc" />
