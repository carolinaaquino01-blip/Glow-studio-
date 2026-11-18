#!/usr/bin/env python3
# Texturas de vino tinto 1080x1350. Uso: wine.py modo(ondas|remolino|mancha) salida.png semilla
import sys
import numpy as np
from PIL import Image

W, H = 1080, 1350
mode, out, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
rng = np.random.default_rng(seed)
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
u, v = x / W, y / W

def gblur(a, sig):
    r = int(sig * 3) + 1; k = np.exp(-np.arange(-r, r + 1) ** 2 / (2 * sig * sig)); k /= k.sum()
    a = np.apply_along_axis(lambda s: np.convolve(np.pad(s, r, mode='edge'), k, 'valid'), 1, a)
    return np.apply_along_axis(lambda s: np.convolve(np.pad(s, r, mode='edge'), k, 'valid'), 0, a).astype(np.float32)

def noise(scale, octaves=3):
    acc = np.zeros((H, W), np.float32); amp = 1.0; tot = 0
    for o in range(octaves):
        gw, gh = int(scale * 2**o) + 2, int(scale * 2**o * H / W) + 2
        g = rng.standard_normal((gh, gw)).astype(np.float32)
        acc += amp * np.asarray(Image.fromarray(g, mode="F").resize((W, H), Image.BICUBIC)); tot += amp; amp *= .5
    return acc / tot

def ramp(t, stops):
    t = np.clip(t, 0, 1); rgb = np.zeros((H, W, 3), np.float32)
    for (t0, c0), (t1, c1) in zip(stops[:-1], stops[1:]):
        m = (t >= t0) & (t <= t1); k = ((t - t0) / (t1 - t0))[m][:, None]
        rgb[m] = np.array(c0) * (1 - k) + np.array(c1) * k
    return rgb

def liquid(h, depth):
    # vino: color por profundidad + reflejo especular brillante tipo líquido
    gy, gx = np.gradient(h)
    nx, ny, nz = -gx, -gy, np.ones_like(h); n = np.sqrt(nx*nx + ny*ny + nz*nz); nx, ny, nz = nx/n, ny/n, nz/n
    # reflejo de una "ventana": luz arriba a la izquierda
    Lx, Ly, Lz = -0.35, -0.55, 0.76; Ln = (Lx*Lx + Ly*Ly + Lz*Lz) ** .5; Lx, Ly, Lz = Lx/Ln, Ly/Ln, Lz/Ln
    Hx, Hy, Hz = Lx, Ly, Lz + 1; Hn = (Hx*Hx + Hy*Hy + Hz*Hz) ** .5; Hx, Hy, Hz = Hx/Hn, Hy/Hn, Hz/Hn
    spec = np.clip(nx*Hx + ny*Hy + nz*Hz, 0, 1) ** 260
    sheen = np.clip(nx*Hx + ny*Hy + nz*Hz, 0, 1) ** 12
    diff = np.clip(nx*Lx + ny*Ly + nz*Lz, 0, 1)
    base = ramp(depth, [(0, (16, 2, 5)), (.35, (36, 6, 12)), (.7, (60, 15, 24)), (1, (84, 22, 34))])
    base *= (0.7 + 0.45 * diff)[..., None]
    return base + spec[..., None] * np.array([240, 200, 196]) * 0.8 + sheen[..., None] * np.array([110, 30, 44]) * 0.25

if mode == "ondas":
    # gota que cae: anillos concéntricos que se apagan, más ondas suaves del líquido
    cx, cy = float(sys.argv[4]) if len(sys.argv) > 4 else rng.uniform(.3, .7), float(sys.argv[5]) if len(sys.argv) > 5 else rng.uniform(.95, 1.15)
    r = np.sqrt((u - cx) ** 2 + (v - cy) ** 2)
    h = np.sin(r * 62 - 1.5) * np.exp(-r * 1.9) * 0.05 * np.clip(r * 8, 0, 1)
    h += noise(1.2, 3) * 0.02
    depth = 0.5 + noise(1.0, 2) * 0.25 + np.exp(-r * 2.5) * 0.25
    rgb = liquid(h * W / 6, depth)
elif mode == "remolino":
    cx, cy = rng.uniform(.4, .6), rng.uniform(.5, .75)
    dx, dy = u - cx, v - cy; r = np.sqrt(dx*dx + dy*dy) + 1e-4; th = np.arctan2(dy, dx)
    warp = noise(2.5, 3) * 0.6
    streak = np.sin(th * 3 + np.log(r) * 9 + warp * 3)
    h = streak * 0.006 + noise(1.5, 3) * 0.015
    depth = 0.5 + 0.35 * np.sin(th * 3 + np.log(r) * 9 + warp * 3 + .8) * np.exp(-r * 1.2) + noise(1.0, 2) * 0.2
    rgb = liquid(gblur(h, 1.5) * W / 6, depth)
else:  # mancha
    rgb = ramp(0.62 + noise(3, 4) * 0.12, [(0, (83, 27, 36)), (1, (120, 50, 58))])
    for i in range(rng.integers(3, 5)):
        cx, cy = rng.uniform(.1, .9), rng.uniform(.1, 1.15)
        R = rng.uniform(.18, .34)
        d = np.sqrt((u - cx) ** 2 + (v - cy) ** 2) / R + noise(4, 3) * 0.12
        inside = np.clip((1 - d) * 25, 0, 1)
        ring = np.exp(-((d - 1) / 0.035) ** 2)   # borde más oscuro, como el aro de una copa
        tint = inside * 0.18 + ring * 0.42
        rgb *= (1 - tint[..., None] * np.array([0.55, 0.75, 0.68]))
    fib = gblur(rng.standard_normal((H, W)).astype(np.float32), 0.8)
    rgb *= 1 + fib[..., None] * 0.06

rgb *= 1 + rng.standard_normal((H, W, 1)).astype(np.float32) * 0.018
Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).save(out)
print(out, rgb.reshape(-1, 3).mean(0).astype(int))
