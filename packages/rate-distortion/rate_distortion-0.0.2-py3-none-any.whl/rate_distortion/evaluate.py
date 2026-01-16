import torch, io, datasets, PIL.Image, numpy as np
from piq import LPIPS, DISTS, SSIMLoss
from torchvision.transforms.v2.functional import pil_to_tensor, resize, to_pil_image

def kodak(encode_fn, decode_fn, resample_factor=1.0, img_format='torch', device='cuda:0'):
    dataset = datasets.load_dataset("danjacobellis/kodak")['validation']
    lpips_loss, dists_loss, ssim_loss = LPIPS().to(device), DISTS().to(device), SSIMLoss().to(device)
    
    def evaluate_quality(sample):
        img = sample['image']
        orig_size = (img.height, img.width)
        pixels = img.width * img.height
        
        if resample_factor != 1.0:
            new_size = (int(img.height * resample_factor), int(img.width * resample_factor))
            img = img.resize((new_size[1], new_size[0]), PIL.Image.LANCZOS)
        
        if img_format == 'torch':
            x_in = pil_to_tensor(img).float() / 127.5 - 1.0
            buff = encode_fn(x_in)
            x_dec = decode_fn(buff)
            if resample_factor != 1.0:
                x_dec = resize(x_dec, orig_size)
            x_hat_01 = (x_dec.to(device) / 2 + 0.5).unsqueeze(0)
        else:
            buff = encode_fn(img)
            dec_img = decode_fn(buff)
            if resample_factor != 1.0:
                dec_img = dec_img.resize((orig_size[1], orig_size[0]), PIL.Image.LANCZOS)
            x_hat_01 = (pil_to_tensor(dec_img).to(device).float() / 127.5 - 1.0).unsqueeze(0) / 2 + 0.5
        
        x_orig_01 = (pil_to_tensor(sample['image']).to(device).float() / 127.5 - 1.0).unsqueeze(0) / 2 + 0.5
        size_bytes = len(buff.getbuffer()) if hasattr(buff, 'getbuffer') else len(buff)
        
        mse = torch.nn.functional.mse_loss(x_orig_01[0], x_hat_01[0])
        return {
            'pixels': pixels,
            'bpp': 8 * size_bytes / pixels,
            'PSNR': -10 * mse.log10().item(),
            'LPIPS_dB': -10 * np.log10(lpips_loss(x_orig_01, x_hat_01).item()),
            'DISTS_dB': -10 * np.log10(dists_loss(x_orig_01, x_hat_01).item()),
            'SSIM': 1 - ssim_loss(x_orig_01, x_hat_01).item(),
        }
    
    results = dataset.map(evaluate_quality)
    return {m: np.mean(results[m]) for m in ['pixels', 'bpp', 'PSNR', 'LPIPS_dB', 'DISTS_dB', 'SSIM']}