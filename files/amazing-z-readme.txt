# Amazing Z-Image Workflow v2.1

This workflow is designed for Z-Image-Turbo and extends the ComfyUI base workflow with extra features, focusing on high-quality image styles and ease of use. The repository contains pre-configured workflows for GGUF and SAFETENSORS formats.

## Table of Contents
1. Features
2. Workflows Overview
3. Required Custom Nodes
4. Required Checkpoints Files
5. License

## Features
- Style Selector: Choose from fifteen customizable image styles for experimentation.
- Alternative Sampler Switch: Easily test generation with an alternative sampler.
- Landscape Orientation Switch: Change to horizontal image generation with a single click.
- Preconfigured workflows for each checkpoint format (GGUF / SAFETENSORS).
- Custom sigma values fine-tuned to personal preference (100% subjective).
- Generated images are saved in the "ZImage" folder, organized by date.
- Incorporates a trick to enable automatic CivitAI prompt detection.

## Workflows Overview
The available styles are organized into workflows based on artistic focus:
- `amazing-z-image`: The original general-purpose workflow with a variety of image styles.
- `amazing-z-comic`: Includes comic, anime, and illustration styles.

Each workflow comes in two versions, one for GGUF checkpoints and another for SafeTensors.
The filenames reflect this:
- `amazing-z-###_GGUF.json`: Recommended for GPUs with 12GB or less VRAM.
- `amazing_z-###_SAFETENSORS.json`: Based directly on the ComfyUI example.

When using ComfyUI, you may encounter debates about the best checkpoint format. From personal experience, GGUF quantized models provide a better balance between size and prompt response quality compared to SafeTensors versions. However, ComfyUI optimizations work more efficiently with SafeTensors files, which might make them preferable despite their larger size. The optimal choice depends on various factors like ComfyUI version, PyTorch setup, CUDA configuration, GPU model, VRAM, and RAM.

## Required Custom Nodes
These nodes can be installed via ComfyUI-Manager or downloaded from their respective repositories:
- [rgthree](https://github.com/rgthree/rgthree-comfy): Required for both workflows.
- [ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF): Required if you are using the workflow preconfigured for GGUF checkpoints.

## Required Checkpoints Files

### For "amazing-z-###_GGUF.json"
Workflows with checkpoint in GGUF format. (recommended)
- [z_image_turbo-Q5_K_S.gguf](https://huggingface.co/jayn7/Z-Image-Turbo-GGUF/blob/main/z_image_turbo-Q5_K_S.gguf) (5.19 GB)
  Local Directory: `ComfyUI/models/diffusion_models/`
- [Qwen3-4B.i1-Q5_K_S.gguf](https://huggingface.co/mradermacher/Qwen3-4B-i1-GGUF/blob/main/Qwen3-4B.i1-Q5_K_S.gguf) (2.82 GB)
  Local Directory: `ComfyUI/models/text_encoders/`
- [ae.safetensors](https://huggingface.co/Comfy-Org/z_image_turbo/blob/main/split_files/vae/ae.safetensors) (335 MB)
  Local Directory: `ComfyUI/models/vae/`

### For "amazing-z-###_SAFETENSORS.json"
Based directly on the official ComfyUI example.
- [z_image_turbo_bf16.safetensors](https://huggingface.co/Comfy-Org/z_image_turbo/blob/main/split_files/diffusion_models/z_image_turbo_bf16.safetensors) (12.3 GB)
  Local Directory: `ComfyUI/models/diffusion_models/`
- [qwen_3_4b.safetensors](https://huggingface.co/Comfy-Org/z_image_turbo/blob/main/split_files/text_encoders/qwen_3_4b.safetensors) (8.04 GB)
  Local Directory: `ComfyUI/models/text_encoders/`
- [ae.safetensors](https://huggingface.co/Comfy-Org/z_image_turbo/blob/main/split_files/vae/ae.safetensors) (335 MB)
  Local Directory: `ComfyUI/models/vae/`

### For Low-VRAM Systems
If neither of the two provided versions nor their associated checkpoints perform adequately on your system, you can find links to several alternative checkpoint files below. Feel free to experiment with these options to determine which works best for you.

#### Diffusion Models (ComfyUI/models/diffusion_models/)
* [Z-Image-Turbo (GGUF Quantizations)](https://huggingface.co/jayn7/Z-Image-Turbo-GGUF/tree/main)
    This repository hosts various quantized versions of the `z_image_turbo` model (e.g., Q4_K_S, Q4_K_M, Q3_K_S). While some of these quantizations offer significantly reduced file sizes, this often comes at the expense of final output quality.
* [Z-Image-Turbo (FP8 SafeTensors)](https://huggingface.co/T5B/Z-Image-Turbo-FP8/tree/main)
    Similar to the GGUF options, this repository provides two `z_image_turbo` models quantized to FP8 (8-bit floating point) in SafeTensors format. These can serve as replacements for the original SafeTensors model, but in my opinion, they degrade quality quite a bit.

#### Text Encoders (ComfyUI/models/text_encoders/)
* [Qwen3-4B (Various GGUF Quantizations)](https://huggingface.co/mradermacher/Qwen3-4B-i1-GGUF/tree/main)
    This repository offers various quantized versions of the `Qwen3-4B` text encoder in GGUF format (e.g., Q2_K, Q3_K_M). Note: Quantizations beginning with "IQ" might not work, as the GGUF node did not support them during my testing.

## License
This project is licensed under the Unlicense license.
See the "LICENSE" file for details.

## More Info
- https://github.com/martin-rizzo/AmazingZImageWorkflow
- https://civitai.com/models/2181458/amazing-z-image-workflow



