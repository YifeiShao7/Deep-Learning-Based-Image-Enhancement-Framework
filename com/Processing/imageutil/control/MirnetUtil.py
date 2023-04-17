import cv2
import os
from runpy import run_path
from skimage import img_as_ubyte
import torch.nn.functional as F

import torch

default_params = {
    'inp_channels':3,
    'out_channels':3,
    'n_feat':80,
    'chan_factor':1.5,
    'n_RRG':4,
    'n_MRB':2,
    'height':3,
    'width':2,
    'bias':False,
    'scale':1,
    'task': None
}

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

def get_weights_and_params(task, params, sr_scale):
    if task == 'real_denoising':
        weights = os.path.join('MirnetModel', 'real_denoising.pth')
    elif task == 'lowlight_enhancement':
        weights = os.path.join('MirnetModel', 'enhancement_lol.pth')
    elif task == 'contrast_enhancement':
        weights = os.path.join('MirnetModel', 'enhancement_fivek.pth')
    elif task == 'super_resolution':
        weights = './MirnetModel/sr_x' + str(sr_scale) + '.pth'
        print(weights)
        # weights = os.path.join('MirnetModel', 'sr_x4.pth')
        params['scale'] = sr_scale
    elif task == 'deblurring':
        weights = './MirnetModel/deblurring.pth'
        return weights, params
    params['task'] = task
    return weights, params

def mirnet_process(src_img, task, sr_scale=4):
    tile_default = None
    tile_overlap_default = 32

    if task == 'deblurring':
        weights, params = get_weights_and_params(task, deblur_params, sr_scale)
        load_arch = run_path('./MirnetModel/restormer_arch.py')
        model = load_arch['Restormer'](**params)
        img_multiple_of = 8
    else:
        weights, params = get_weights_and_params(task, default_params, sr_scale)
        load_arch = run_path('./MirnetModel/mirnet_v2_arch.py')
        model = load_arch['MIRNet_v2'](**params)
        # use for completion
        img_multiple_of = 4

    if torch.cuda.is_available():
        device = torch.device('cuda')
    elif torch.backends.mps.is_available():
        device = torch.device('mps')
    else:
        torch.device('cpu')
    # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # device = torch.device('mps')
    model.to(device)

    checkpoint = torch.load(weights)
    model.load_state_dict(checkpoint['params'])
    model.eval()
    with torch.no_grad():
        temp_img = load_img(src_img)
        input_ = torch.from_numpy(temp_img).float().div(255.).permute(2,0,1).unsqueeze(0).to(device)

        height, width = input_.shape[2], input_.shape[3]

        H, W = ((height + img_multiple_of)//img_multiple_of)*img_multiple_of, ((width+img_multiple_of)//img_multiple_of)*img_multiple_of

        padH = H-height if height%img_multiple_of != 0 else 0
        padW = W-width if width%img_multiple_of != 0 else 0

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

        restored = restored[:,:,:height,:width]

        # unpad output
        restored = restored.permute(0, 2, 3, 1).cpu().detach().numpy()
        restored = img_as_ubyte(restored[0])

        print("finish")
        final = save_img(restored)
        return final









