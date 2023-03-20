import os
import numpy as np
from PIL import Image
from com.Processing.imageutil.GCANetModel.GCANet import GCANet

import torch
from torch.autograd import Variable

def edge_compute(x):
    x_diffx = torch.abs(x[:,:,1:] - x[:,:,:-1])
    x_diffy = torch.abs(x[:,1:,:] - x[:,:-1,:])

    y = x.new(x.size())
    y.fill_(0)
    y[:,:,1:] += x_diffx
    y[:,:,:-1] += x_diffx
    y[:,1:,:] += x_diffy
    y[:,:-1,:] += x_diffy
    y = torch.sum(y,0,keepdim=True)/3
    y /= 4
    return y

def gcanProcess(src_image, task):
    # model config
    if task == 'dehaze':
        model = './GCANetModel/dehaze.pth'
    elif task == 'derain':
        model = './GCANetModel/derain.pth'

    net = GCANet(in_c=4, out_c=3, only_residual= task == 'dehaze')

    net.float()

    net.load_state_dict(torch.load(model, map_location='cpu'))
    net.eval()

#     image processing
    img = Image.fromarray(src_image).convert('RGB')
    width, height = img.size
    if width % 4 != 0 or height % 4 != 0:
        img = img.resize((int(width // 4 * 4), int(height // 4 * 4)))
    img = np.array(img).astype('float')
    img_data = torch.from_numpy(img.transpose((2, 0, 1))).float()
    edge_data = edge_compute(img_data)

    in_data = torch.cat((img_data, edge_data), dim=0).unsqueeze(0) - 128
    in_data = in_data.float()

    with torch.no_grad():
        pred = net(Variable(in_data))
    if task == 'dehaze':
        out_img = (pred.data[0].cpu().float() + img_data).round().clamp(0, 255)
    else:
        out_img = pred.data[0].cpu().float().round().clamp(0, 255)
    output = np.asarray(Image.fromarray(out_img.numpy().astype(np.uint8).transpose(1, 2, 0)))
    print('GCAN finish')
    return output