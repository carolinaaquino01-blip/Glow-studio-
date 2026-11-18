#!/usr/bin/env python3
# Genera un fondo de terciopelo arrugado 1080x1350: pliegues + iluminación tipo terciopelo + fibras.
# Uso: velvet.py salida.png semilla
import sys
import numpy as np
from PIL import Image, ImageFilter

W, H = 1080, 1350
out, seed = sys.argv[1], int(sys.argv[2])
rng = np.random.default_rng(seed)
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
x /= W; y /= W  # misma escala en ambos ejes

def gblur(a, sig):
    r = int(sig * 3) + 1; k = np.exp(-np.arange(-r, r + 1) ** 2 / (2 * sig * sig)); k /= k.sum()
    a = np.apply_along_axis(lambda v: np.convolve(np.pad(v, r, mode='edge'), k, 'valid'), 1, a)
    return np.apply_along_axis(lambda v: np.convolve(np.pad(v, r, mode='edge'), k, 'valid'), 0, a).astype(np.float32)

def smooth_noise(scale, octaves=3):
    # ruido suave por interpolación bicúbica de una grilla aleatoria
    acc = np.zeros((H, W), np.float32); amp = 1.0; tot = 0
    for o in range(octaves):
        gw, gh = int(scale * 2**o) + 2, int(scale * 2**o * H / W) + 2
        g = rng.standard_normal((gh, gw)).astype(np.float32)
        im = Image.fromarray(g, mode="F").resize((W, H), Image.BICUBIC)
        acc += amp * np.asarray(im); tot += amp; amp *= 0.5
    return acc / tot

# deformación del dominio para que los pliegues sean orgánicos
wx, wy = smooth_noise(2.0) * 0.22, smooth_noise(2.0) * 0.22
px, py = x + wx, y + wy

# pliegues: varias ondas en direcciones distintas, algunas como crestas (abs) = arrugas marcadas
h = np.zeros((H, W), np.float32)
for i in range(5):
    ang = rng.uniform(0, np.pi)
    f = rng.uniform(1.3, 3.0)
    ph = rng.uniform(0, 2 * np.pi)
    a = rng.uniform(0.5, 1.0) / (1 + i * 0.25)
    t = (np.cos(ang) * px + np.sin(ang) * py) * f * 2 * np.pi + ph
    h += a * (1 - np.abs(np.sin(t / 2)) * 2 if i % 3 == 0 else np.sin(t))
h += smooth_noise(6.0, 2) * 0.35
h = gblur(h, 2)

# normales
gy, gx = np.gradient(h * 40.0)
nx, ny, nz = -gx, -gy, np.ones_like(h)
n = np.sqrt(nx**2 + ny**2 + nz**2); nx, ny, nz = nx / n, ny / n, nz / n
L = np.array([-0.45, -0.6, 0.66]); L /= np.linalg.norm(L)
diffuse = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
rim = (1 - nz) ** 1.3  # el terciopelo brilla en las superficies inclinadas
facing = np.clip(nx * L[0] + ny * L[1], -1, 1) * 0.5 + 0.5
sheen = rim * (0.35 + 0.65 * facing)
shade = 0.55 * diffuse + 1.25 * sheen
shade = (shade - shade.min()) / (np.ptp(shade) + 1e-6)

# paleta: sombra profunda -> vino -> bordó -> brillo rosado del terciopelo
stops = [(0.0, (58, 16, 25)), (0.25, (83, 27, 36)), (0.5, (106, 41, 49)), (0.8, (142, 68, 78)), (1.0, (190, 120, 126))]
t = np.clip(shade ** 0.9, 0, 1)
rgb = np.zeros((H, W, 3), np.float32)
for (t0, c0), (t1, c1) in zip(stops[:-1], stops[1:]):
    m = (t >= t0) & (t <= t1)
    k = ((t - t0) / (t1 - t0))[m][:, None]
    rgb[m] = np.array(c0) * (1 - k) + np.array(c1) * k

# fibras: ruido fino estirado en una dirección, más visible en las zonas de brillo
fib = rng.standard_normal((H // 2, W * 2)).astype(np.float32)
fib = np.asarray(Image.fromarray(fib, mode="F").resize((W, H), Image.BILINEAR))
fib = gblur(fib, 0.6)
rgb *= (1 + fib[..., None] * (0.035 + 0.05 * t[..., None]))
grain = rng.standard_normal((H, W, 1)).astype(np.float32)
rgb *= 1 + grain * 0.025

# viñeta
cx, cy = 0.5, 0.62
d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
rgb *= (1 - np.clip((d - 0.55) * 0.8, 0, 0.35))[..., None]

Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).save(out)
print(out, "avg", rgb.reshape(-1, 3).mean(0).astype(int))
