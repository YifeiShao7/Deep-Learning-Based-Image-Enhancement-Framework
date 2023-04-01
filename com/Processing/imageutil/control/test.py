import cv2
import os
from runpy import run_path
from skimage import img_as_ubyte
import torch.nn.functional as F

import torch

deblur_params = {
    'inp_channels':3,
    'out_channels':3,
    'dim':48,
    'num_blocks':[4,6,6,8],
    'num_refinement_blocks':4,
    'heads':[1,2,4,8],
    'ffn_expansion_factor':2.66,
    'bias':False,
    'LayerNorm_type':'WithBias',
    'dual_pixel_task':False
}

def load_img(img_src):
    return cv2.cvtColor(img_src, cv2.COLOR_BGR2RGB)

def save_img(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

def get_weight_and_params(task, params):
    if task == 'deblurring':
        weights = os.path.join('MirnetModel', 'deblurring.pth')
    return weights, params

def deblurring(src_img, task):
    tile_default = None
    tile_overlap_default = 32

    weights, params = get_weight_and_params(task, deblur_params)
    load_arch = run_path('./MirnetModel/restormer_arch.py')
    model = load_arch['Restormer'](**params)
    img_multiple_of = 8

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    checkpoint = torch.load(weights)
    model.load_state_dict(checkpoint['params'])
    model.eval()

    temp_img = load_img(src_img)
    input_ = torch.from_numpy(temp_img).float().div(255.).permute(2, 0, 1).unsqueeze(0).to(device)

    height, width = input_.shape[2], input_.shape[3]

    H, W = ((height + img_multiple_of) // img_multiple_of) * img_multiple_of, (
                (width + img_multiple_of) // img_multiple_of) * img_multiple_of

    padH = H - height if height % img_multiple_of != 0 else 0
    padW = W - width if width % img_multiple_of != 0 else 0

    input_ = F.pad(input_, (0, padW, 0, padH), 'reflect')

    if tile_default is None:
        restored = model(input_)
    else:
        b, c, h, w = input_.shape
        tile = min(tile_default, h, w)

        assert tile % img_multiple_of == 0, "tile size should be multiple of 4 or 8"
        tile_overlap = tile_overlap_default

        stride = tile - tile_overlap
        h_idx_list = list(range(0, h-tile, stride)) + [h-tile]
        w_idx_list = list(range(0, w-tile, stride)) + [w-tile]
        E = torch.zeros(b, c, h, w).type_as(input_)
        W = torch.zeros_like(E)

        for h_idx in h_idx_list:
            for w_idx in w_idx_list:
                in_patch = input_[..., h_idx:h_idx + tile, w_idx:w_idx + tile]
                out_patch = model(in_patch)
                out_patch_mask = torch.ones_like(out_patch)

                E[..., h_idx:(h_idx + tile), w_idx:(w_idx + tile)].add_(out_patch)
                W[..., h_idx:(h_idx + tile), w_idx:(w_idx + tile)].add_(out_patch_mask)
        restored = E.div_(W)

    restored = torch.clamp(restored, 0, 1)

    restored = restored[:, :, :height, :width]

    print("3")
    # unpad output
    restored = restored.permute(0, 2, 3, 1).cpu().detach().numpy()
    restored = img_as_ubyte(restored[0])

    print("finish")
    final = save_img(restored)
    return final