import argparse
import os
import json
import re

import torch
import numpy as np
from gguf import *

TEXT = "clip.text"
VISION = "clip.vision"
from transformers import SiglipVisionModel, SiglipVisionConfig


def k(raw_key: str, arch: str) -> str:
    return raw_key.format(arch=arch)


def should_skip_tensor(name: str, has_text: bool, has_vision: bool, has_llava: bool) -> bool:
    if name in (
        "logit_scale",
        "text_model.embeddings.position_ids",
        "vision_model.embeddings.position_ids",
    ):
        return True

    if name in (
        "vision_model.head.probe",
        "vision_model.head.attention.in_proj_weight",
        "vision_model.head.attention.in_proj_bias",
        "vision_model.head.attention.out_proj.weight",
        "vision_model.head.attention.out_proj.bias",
        "vision_model.head.layernorm.weight",
        "vision_model.head.layernorm.bias",
        "vision_model.head.mlp.fc1.weight",
        "vision_model.head.mlp.fc1.bias",
        "vision_model.head.mlp.fc2.weight",
        "vision_model.head.mlp.fc2.bias",
    ):
        return True

    if name.startswith("v") and not has_vision:
        return True

    if name.startswith("t") and not has_text:
        return True

    return False


def get_tensor_name(name: str) -> str:
    if "projection" in name:
        return name
    if "mm_projector" in name:
        name = name.replace("model.mm_projector", "mm")
        name = re.sub(r"mm\.mlp\.mlp", "mm.model.mlp", name, count=1)
        name = re.sub(r"mm\.peg\.peg", "mm.model.peg", name, count=1)
        return name

    return (
        name.replace("text_model", "t")
        .replace("vision_model", "v")
        .replace("encoder.layers", "blk")
        .replace("embeddings.", "")
        .replace("_proj", "")
        .replace("self_attn.", "attn_")
        .replace("layer_norm", "ln")
        .replace("layernorm", "ln")
        .replace("mlp.fc1", "ffn_down")
        .replace("mlp.fc2", "ffn_up")
        .replace("embedding", "embd")
        .replace("final", "post")
        .replace("layrnorm", "ln")
    )


def bytes_to_unicode():
    """
    Returns list of utf-8 byte and a corresponding list of unicode strings.
    The reversible bpe codes work on unicode strings.
    This means you need a large # of unicode characters in your vocab if you want to avoid UNKs.
    When you're at something like a 10B token dataset you end up needing around 5K for decent coverage.
    This is a significant percentage of your normal, say, 32K bpe vocab.
    To avoid that, we want lookup tables between utf-8 bytes and unicode strings.
    And avoids mapping to whitespace/control characters the bpe code barfs on.
    """
    bs = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(ord("¡"), ord("¬") + 1))
        + list(range(ord("®"), ord("ÿ") + 1))
    )
    cs = bs[:]
    n = 0
    for b in range(2**8):
        if b not in bs:
            bs.append(b)
            cs.append(2**8 + n)
            n += 1
    cs = [chr(n) for n in cs]
    return dict(zip(bs, cs))


ap = argparse.ArgumentParser()
ap.add_argument(
    "-m",
    "--model-dir",
    help="Path to model directory cloned from HF Hub",
    required=True,
)
ap.add_argument("--use-f32", action="store_true", default=False, help="Use f32 instead of f16")
ap.add_argument(
    "--text-only",
    action="store_true",
    required=False,
    help="Save a text-only model. It can't be used to encode images",
)
ap.add_argument(
    "--vision-only",
    action="store_true",
    required=False,
    help="Save a vision-only model. It can't be used to encode texts",
)
ap.add_argument(
    "--clip-model-is-vision",
    action="store_true",
    required=False,
    help="The clip model is a pure vision model (ShareGPT4V vision extract for example)",
)
ap.add_argument(
    "--clip-model-is-openclip",
    action="store_true",
    required=False,
    help="The clip model is from openclip (for ViT-SO400M type))",
)
ap.add_argument(
    "--llava-projector",
    help="Path to llava.projector file. If specified, save an image encoder for LLaVA models.",
)
ap.add_argument(
    "--projector-type",
    help="Type of projector. Possible values: mlp, ldp, ldpv2",
    choices=["mlp", "ldp", "ldpv2", "adapter"],
    default="adapter",
)
ap.add_argument(
    "-o",
    "--output-dir",
    help="Directory to save GGUF files. Default is the original model directory",
    default=None,
)
# Example --image_mean 0.48145466 0.4578275 0.40821073 --image_std 0.26862954 0.26130258 0.27577711
# Example --image_mean 0.5 0.5 0.5 --image_std 0.5 0.5 0.5
default_image_mean = [0.5, 0.5, 0.5]
default_image_std = [0.5, 0.5, 0.5]
ap.add_argument(
    "--image-mean",
    type=float,
    nargs="+",
    help="Mean of the images for normalization (overrides processor) ",
    default=None,
)
ap.add_argument(
    "--image-std",
    type=float,
    nargs="+",
    help="Standard deviation of the images for normalization (overrides processor)",
    default=None,
)

# with proper
args = ap.parse_args()


if args.text_only and args.vision_only:
    print("--text-only and --image-only arguments cannot be specified at the same time.")
    exit(1)

if args.use_f32:
    print(
        "WARNING: Weights for the convolution op is always saved in f16, as the convolution op in GGML does not support 32-bit kernel weights yet."
    )

# output in the same directory as the model if output_dir is None
dir_model = args.model_dir

if (
    args.clip_model_is_vision
    or not os.path.exists(dir_model + "/vocab.json")
    or args.clip_model_is_openclip
):
    vocab = None
    tokens = None
else:
    with open(dir_model + "/vocab.json", "r", encoding="utf-8") as f:
        vocab = json.load(f)
        tokens = [key for key in vocab]

with open(dir_model + "/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)
    if args.clip_model_is_vision:
        v_hparams = config
        t_hparams = None
    else:
        v_hparams = config["vision_config"]
        t_hparams = None

# possible data types
#   ftype == 0 -> float32
#   ftype == 1 -> float16
#
# map from ftype to string
ftype_str = ["f32", "f16"]

ftype = 1
if args.use_f32:
    ftype = 0

vision_config = SiglipVisionConfig(**v_hparams)
model = SiglipVisionModel(vision_config)
model.load_state_dict(torch.load(os.path.join(dir_model, "glm.clip")))

fname_middle = None
has_text_encoder = False
has_vision_encoder = True
has_glm_projector = True
if args.text_only:
    fname_middle = "text-"
    has_vision_encoder = False
elif args.llava_projector is not None:
    fname_middle = "mmproj-"
    has_text_encoder = False
    has_glm_projector = True
elif args.vision_only:
    fname_middle = "vision-"
    has_text_encoder = False
else:
    fname_middle = ""

output_dir = args.output_dir if args.output_dir is not None else dir_model
os.makedirs(output_dir, exist_ok=True)
output_prefix = os.path.basename(output_dir).replace("ggml_", "")
fname_out = os.path.join(output_dir, f"{fname_middle}model-{ftype_str[ftype]}.gguf")
fout = GGUFWriter(path=fname_out, arch="clip")

fout.add_bool("clip.has_text_encoder", has_text_encoder)
fout.add_bool("clip.has_vision_encoder", has_vision_encoder)
fout.add_bool("clip.has_glm_projector", has_glm_projector)
fout.add_file_type(ftype)
model_name = config["_name_or_path"] if "_name_or_path" in config else os.path.basename(dir_model)
fout.add_name(model_name)
if has_glm_projector:
    fout.add_description("image encoder for glm4v")
    fout.add_string("clip.projector_type", "adapter")
else:
    fout.add_description("two-tower CLIP model")

if has_text_encoder:
    assert t_hparams is not None
    assert tokens is not None
    # text_model hparams
    fout.add_uint32(k(KEY_CONTEXT_LENGTH, TEXT), t_hparams["max_position_embeddings"])
    fout.add_uint32(k(KEY_EMBEDDING_LENGTH, TEXT), t_hparams["hidden_size"])
    fout.add_uint32(k(KEY_FEED_FORWARD_LENGTH, TEXT), t_hparams["intermediate_size"])
    fout.add_uint32(
        "clip.text.projection_dim",
        t_hparams.get("projection_dim", config["projection_dim"]),
    )
    fout.add_uint32(k(KEY_ATTENTION_HEAD_COUNT, TEXT), t_hparams["num_attention_heads"])
    fout.add_float32(k(KEY_ATTENTION_LAYERNORM_EPS, TEXT), t_hparams["layer_norm_eps"])
    fout.add_uint32(k(KEY_BLOCK_COUNT, TEXT), t_hparams["num_hidden_layers"])
    fout.add_token_list(tokens)

if has_vision_encoder:
    # vision_model hparams
    fout.add_uint32("clip.vision.image_size", v_hparams["image_size"])
    fout.add_uint32("clip.vision.patch_size", v_hparams["patch_size"])
    fout.add_uint32(k(KEY_EMBEDDING_LENGTH, VISION), v_hparams["hidden_size"])
    fout.add_uint32(k(KEY_FEED_FORWARD_LENGTH, VISION), v_hparams["intermediate_size"])
    fout.add_uint32("clip.vision.projection_dim", 0)
    fout.add_uint32(k(KEY_ATTENTION_HEAD_COUNT, VISION), v_hparams["num_attention_heads"])
    fout.add_float32(k(KEY_ATTENTION_LAYERNORM_EPS, VISION), 1e-6)
    fout.add_uint32(k(KEY_BLOCK_COUNT, VISION), v_hparams["num_hidden_layers"])

    image_mean = args.image_mean if args.image_mean is not None else default_image_mean
    image_std = args.image_std if args.image_std is not None else default_image_std
    fout.add_array("clip.vision.image_mean", image_mean)
    fout.add_array("clip.vision.image_std", image_std)

fout.add_bool("clip.use_gelu", True)


if has_glm_projector:
    # model.vision_model.encoder.layers.pop(-1)  # pyright: ignore[reportAttributeAccessIssue]
    projector = torch.load(args.llava_projector)
    for name, data in projector.items():
        name = get_tensor_name(name)
        # pw and dw conv ndim==4
        if data.ndim == 2 or data.ndim == 4:
            data = data.squeeze().numpy().astype(np.float16)
        else:
            data = data.squeeze().numpy().astype(np.float32)
        if name.startswith("vision."):
            name = name.replace("vision.", "")
        fout.add_tensor(name, data)
        print(f"Projector {name} - {data.dtype} - shape = {data.shape}")
        # print(f"Projector {name} tensors added\n")

state_dict = model.state_dict()  # pyright: ignore[reportAttributeAccessIssue]
for name, data in state_dict.items():
    if should_skip_tensor(name, has_text_encoder, has_vision_encoder, has_glm_projector):
        # we don't need this
        print(f"skipping parameter: {name}")
        continue

    name = get_tensor_name(name)
    data = data.squeeze().numpy()

    n_dims = len(data.shape)

    # ftype == 0 -> float32, ftype == 1 -> float16
    ftype_cur = 0
    if n_dims == 4:
        print(f"tensor {name} is always saved in f16")
        data = data.astype(np.float16)
        ftype_cur = 1
    elif ftype == 1:
        if name[-7:] == ".weight" and n_dims == 2:
            # print("  Converting to float16")
            data = data.astype(np.float16)
            ftype_cur = 1
        else:
            # print("  Converting to float32")
            data = data.astype(np.float32)
            ftype_cur = 0
    else:
        if data.dtype != np.float32:
            # print("  Converting to float32")
            data = data.astype(np.float32)
            ftype_cur = 0
    print(f"siglip {name} - {data.dtype} - shape = {data.shape}")
    # print(f"{name} - {ftype_str[ftype_cur]} - shape = {data.shape}")
    fout.add_tensor(name, data)


fout.write_header_to_file()
fout.write_kv_data_to_file()
fout.write_tensors_to_file()
fout.close()

print("Done. Output file: " + fname_out)
