<div align="center" markdown>
<!-- <img src="https://user-images.githubusercontent.com/48913536/183899083-64d7683d-57f9-4f7a-b5f4-bf9e7ffd3246.png"/> -->

# Export to COCO Keypoints

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Use">How To Use</a> •
  <a href="#Results">Results</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/export-coco-keypoints)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/export-coco-keypoints)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/export-coco-keypoints.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/export-coco-keypoints.png)](https://supervise.ly)

</div>

# export-coco-keypoints

Converts Supervisely to COCO Keypoints format and prepares tar archive for download

# Overview

App converts [Supervisely format](https://docs.supervise.ly/data-organization/00_ann_format_navi) project to [COCO Keypoints format](https://cocodataset.org/#format-data) as a **downloadable .tar archive**

Application key points:

- Supports **person_keypoints.json** from **COCO** format
- Сonverts **Supervisely** keypoints to **COCO** keypoints and bboxes.
- ⚠️ Сonverts all annotations as visible keypoints.

- Backward compatible with [Import COCO keypoints](https://github.com/supervisely-ecosystem/import-coco-keypoints)

# How to Use

1. Add [Export to COCO Keypoints](https://ecosystem.supervise.ly/apps/export-coco-keypoints) to your team from Ecosystem

   <!-- <img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/export-coco-keypoints" src="" width="350px" style='padding-bottom: 20px'/> -->

2. Run app from the context menu of **Images Project**:

<!-- <img src="" /> -->

3. Select options in the modal window and press the **RUN** button

<!-- <img src=""/> -->

# Results

After running the application, you will be redirected to the `Tasks` page. Once application processing has finished, your link for downloading will be available. Click on the `file name` to download it.

<!-- <img src=""/> -->

To explore warnings just open `Log` in the `⋮` menu:

<!-- <img src=""/> -->

You can also find your converted project in
`Team Files` -> `tmp` -> `supervisely` -> `export` -> `export-COCO-keypoints` -> `<taskId>_<projectName>.tar`

<!-- <img src=""/> -->
