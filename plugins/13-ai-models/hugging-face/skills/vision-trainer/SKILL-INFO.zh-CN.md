# Hugging Face：视觉模型训练

Hugging Face：视觉模型训练。适用于模型、数据集、训练、评测、推理和模型工作台相关任务；具体输入、步骤和输出见原始技能说明。

- 仓库唯一编号：`hugging-face--vision-trainer`
- 原始技能名：`huggingface-vision-trainer`
- 分类：AI模型与训练
- 兼容性：工具与环境适配
- 依赖：保留 Hugging Face 整包目录；阅读 SKILL.md 确认所需工具。复制技能文件不会安装插件、MCP、CLI或账号授权。
- 许可：本地未发现完整许可文件；不视为获得额外授权
- 来源：Hugging Face 插件 1.0.0

## 原始说明

Trains and fine-tunes vision models for object detection (D-FINE, RT-DETR v2, DETR, YOLOS), image classification (timm models — MobileNetV3, MobileViT, ResNet, ViT/DINOv3 — plus any Transformers classifier), and SAM/SAM2 segmentation using Hugging Face Transformers on Hugging Face Jobs cloud GPUs. Covers COCO-format dataset preparation, Albumentations augmentation, mAP/mAR evaluation, accuracy metrics, SAM segmentation with bbox/point prompts, DiceCE loss, hardware selection, cost estimation, Trackio monitoring, and Hub persistence. Use when users mention training object detection, image classification, SAM, SAM2, segmentation, image matting, DETR, D-FINE, RT-DETR, ViT, timm, MobileNet, ResNet, bounding box models, or fine-tuning vision models on Hugging Face Jobs.

[阅读 SKILL.md](SKILL.md) · [完整技能清单](../../../../../CATALOG.md)
