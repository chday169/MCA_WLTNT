# MCA_WLTNT  
# Geometric Marching Cubes Without Lookup Tables and Without Triangles  
### 從 2D Marching Squares 到 3D 隱式曲面點雲重建（無查表、無三角形幾何方法）

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

# 🧊 摘要（Abstract）

傳統 **Marching Cubes Algorithm (MCA)** 通常依賴：

- 256 組 Lookup Table
- Triangle Mesh 拓樸建構
- 複雜的 Triangle Connectivity

來自體素（Voxel）標量場建立等值面（Iso-Surface）。

雖然此方法具有良好曲面重建能力，但：

- Lookup Table 過於工程化
- 幾何本質被隱藏
- GPU 平行化存在拓樸同步問題
- Triangle Mesh 建立耗時
- 高維空間延伸困難

因此，本研究提出：

# MCA_WLTNT

（Marching Cube Algorithm Without Lookup Table and No Triangle）

本方法直接從：

\[
f(x,y,z)=0
\]

之隱式函數曲面出發。

在遍歷每個單位立方體（Voxel）時：

- 搜尋 12 條稜線
- 檢測符號變化
- 線性插值求交點
- 不建立 Triangle Mesh
- 直接以 Point Cloud 表示曲面

因此：

- 不需 Lookup Table
- 不需 Triangle Topology
- 不需 Mesh Stitching
- 不需 Vertex Connectivity

形成：

# Dense Point Set ≈ Continuous Surface

當：

\[
dx,dy,dz \rightarrow 0
\]

時，點雲集合即可逼近連續隱式曲面。

本研究將 Marching Cubes 的真正數學本質重新解釋為：

- Sign Crossing Detection
- Edge-based Interpolation
- Implicit Geometry Sampling
- Point-based Surface Reconstruction

而非傳統的 Lookup Table 與 Triangle Topology。

---

# 📐 數學原理（Mathematical Theory）

## 隱式曲面（Implicit Surface）

三維隱式函數：

\[
f(x,y,z)=0
\]

定義一連續曲面。

例如球體：

\[
f(x,y,z)=x^2+y^2+z^2-r^2
\]

將空間離散化為 Voxel Grid 後：

- 每個立方體具有 8 個頂點
- 12 條稜線

對於任一稜線：

\[
P_1,P_2
\]

若：

\[
f(P_1)\cdot f(P_2)<0
\]

表示曲面穿越該稜線。

---

## 線性插值（Linear Interpolation）

交點位置：

\[
P=P_1+t(P_2-P_1)
\]

其中：

\[
t=\frac{|f(P_1)|}{|f(P_1)|+|f(P_2)|}
\]

所得點：

\[
f(P)\approx0
\]

因此位於隱式曲面附近。

---

## Point-based Surface Reconstruction

傳統 Marching Cubes：

```text
Edge Intersections
        ↓
Triangle Construction
        ↓
Mesh Topology
```

MCA_WLTNT：

```text
Edge Intersections
        ↓
Point Cloud
        ↓
Dense Surface Approximation
```

因此：

- 大幅降低幾何複雜度
- 提升 GPU 平行效率
- 降低記憶體需求
- 適合即時運算

---

# 🖥️ Python 程式碼範例（Python Example）

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ==========================================
# Implicit Function
# Sphere
# ==========================================

def f(x, y, z):
    return x**2 + y**2 + z**2 - 1.0

# ==========================================
# Grid
# ==========================================

n = 60

x = np.linspace(-1.5, 1.5, n)
y = np.linspace(-1.5, 1.5, n)
z = np.linspace(-1.5, 1.5, n)

# ==========================================
# Cube Edges
# ==========================================

edges = [
    (0,1),(1,2),(2,3),(3,0),
    (4,5),(5,6),(6,7),(7,4),
    (0,4),(1,5),(2,6),(3,7)
]

# ==========================================
# Point Storage
# ==========================================

points = []

# ==========================================
# Traversal
# ==========================================

for i in range(n-1):
    for j in range(n-1):
        for k in range(n-1):

            cube = [
                (x[i],   y[j],   z[k]),
                (x[i+1], y[j],   z[k]),
                (x[i+1], y[j+1], z[k]),
                (x[i],   y[j+1], z[k]),

                (x[i],   y[j],   z[k+1]),
                (x[i+1], y[j],   z[k+1]),
                (x[i+1], y[j+1], z[k+1]),
                (x[i],   y[j+1], z[k+1])
            ]

            vals = [f(*p) for p in cube]

            for e in edges:

                p1 = np.array(cube[e[0]])
                p2 = np.array(cube[e[1]])

                v1 = vals[e[0]]
                v2 = vals[e[1]]

                if v1 * v2 < 0:

                    t = abs(v1) / (abs(v1) + abs(v2))

                    p = p1 + t * (p2 - p1)

                    points.append(p)

# ==========================================
# Convert
# ==========================================

points = np.array(points)

# ==========================================
# Visualization
# ==========================================

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(
    points[:,0],
    points[:,1],
    points[:,2],
    s=0.5
)

ax.set_title("MCA_WLTNT Point-based Iso-Surface")

plt.show()
```

完整程式請見：

```text
mca_wltnt.py
```

---

# 📸 執行結果（Results）

本演算法成功重建隱式曲面：

- 完全不使用 Lookup Table
- 完全不建立 Triangle Mesh
- 僅利用 Point Cloud 表示曲面

---

## Sphere

\[
x^2+y^2+z^2-0.49=0
\]

```text
images/sphere.png
```

---

## Hyperboloid

\[
x^2+y^2-2z^2-0.49=0
\]

```text
images/hyperboloid.png
```

---

## CT Medical Reconstruction

MCA_WLTNT 可直接應用於：

- CT
- MRI
- Organ Segmentation
- Medical Digital Twin

利用：

```text
Density Field → Iso-point Extraction → Point Cloud Reconstruction
```

建立即時醫學點雲模型。

---

# 🚀 GPU 與 AI（GPU and AI）

MCA_WLTNT 特別適合 GPU：

- One Thread Per Voxel
- No Triangle Synchronization
- No Mesh Connectivity
- SIMD Friendly
- Extremely Parallel

可進一步結合：

- CUDA
- OpenCL
- TensorFlow
- PyTorch
- Neural Implicit Surface
- DeepSDF
- NeRF

形成：

# AI-driven Implicit Geometry Reconstruction

---

# 🎮 Scratch / TurboWarp 整合

本方法極適合教育用途。

因為：

- 不需 Triangle Topology
- 僅需：
  - 邊掃描
  - 符號判定
  - 插值
  - 點生成

因此可直接以：

- Scratch
- TurboWarp
- Blockly

建立：

- 幾何教學
- 曲面生成動畫
- 互動式數學視覺化

---

# 📂 專案結構（Project Structure）

```text
MCA_WLTNT/
├── images/
│   ├── author.jpg
│   ├── sphere.png
│   ├── hyperboloid.png
│   └── ct_reconstruction.png
│
├── mca_wltnt.py
├── ct_reconstruction.py
├── extended_abstract.html
├── about-me.html
├── README.md
├── LICENSE
└── .nojekyll
```

---

# 👤 作者（Author）

<img src="images/author.jpg"
     alt="C.H. Day"
     width="100"
     style="border-radius:50%;"
     onerror="this.style.display='none';
     this.insertAdjacentHTML(
     'afterend',
     '<span style=&quot;display:inline-block;
     width:100px;
     height:100px;
     border-radius:50%;
     background:#2c7da0;
     color:white;
     text-align:center;
     line-height:100px;
     font-size:2rem;&quot;>CT</span>');">

戴清河  
C.H. Day (chday169)

土木及水利工程技師（退休）

研究方向：

- Implicit Geometry
- CFD
- Flood Simulation
- GPU Computing
- AI Geometry
- Medical Digital Twin
- Mathematical Visualization

---

# 📄 授權（License）

MIT License

詳見：

```text
LICENSE
```

---

# 🔗 引用（Citation）

若於學術或教育研究中引用本方法，建議：

```text
C.H. Day.

MCA_WLTNT:
Geometric Marching Cubes Without Lookup Tables and Without Triangles.

GitHub Repository, 2026.

https://github.com/chday169/MCA_WLTNT
```

---

# 🌐 官方網站（GitHub Pages）

```text
https://chday169.github.io/MCA_WLTNT/
```

---

# 🧠 核心思想（Core Philosophy）

傳統 Marching Cubes：

```text
Lookup Table → Triangle Mesh
```

MCA_WLTNT：

```text
Implicit Geometry
        ↓
Edge Sampling
        ↓
Point Cloud
        ↓
Continuous Surface Approximation
```

---

# 🌌 未來研究方向（Future Research）

- Neural Implicit Surface
- AI Geometry Learning
- Medical Digital Twin
- Real-time CFD
- Smart City Simulation
- Quantum Geometry
- Autonomous Vehicle Mapping
- GPU Cloud Geometry

---

# 保持好奇 · 享受幾何