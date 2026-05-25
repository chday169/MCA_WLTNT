import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 建立模擬 CT Volume
# ==========================================

n = 80

x = np.linspace(-1,1,n)
y = np.linspace(-1,1,n)
z = np.linspace(-1,1,n)

X,Y,Z = np.meshgrid(x,y,z)

# ==========================================
# 模擬心臟 CT 結構
# ==========================================

heart = np.exp(-(X**2 + Y**2 + Z**2)*7)

vessel = 0.35*np.exp(
    -((X-0.35)**2 + Y**2 + Z**2)*60
)

volume = heart + vessel

# iso value
iso = 0.32

# ==========================================
# MCA_WLT Point-Based Surface Sampling
# ==========================================

points = []

# 12 edges of cube

edges = [
    (0,1),(1,2),(2,3),(3,0),
    (4,5),(5,6),(6,7),(7,4),
    (0,4),(1,5),(2,6),(3,7)
]

# cube vertices

cube_offsets = np.array([
    [0,0,0],
    [1,0,0],
    [1,1,0],
    [0,1,0],
    [0,0,1],
    [1,0,1],
    [1,1,1],
    [0,1,1]
])

# ==========================================
# Traversal
# ==========================================

for i in range(n-1):
    for j in range(n-1):
        for k in range(n-1):

            vals = []
            verts = []

            for off in cube_offsets:

                xi = i + off[0]
                yj = j + off[1]
                zk = k + off[2]

                vals.append(volume[xi,yj,zk])
                verts.append([X[xi,yj,zk],
                              Y[xi,yj,zk],
                              Z[xi,yj,zk]])

            vals = np.array(vals)
            verts = np.array(verts)

            # check all 12 edges

            for e in edges:

                a,b = e

                va = vals[a]
                vb = vals[b]

                # surface crossing

                if (va-iso)*(vb-iso) < 0:

                    t = (iso-va)/(vb-va)

                    p = verts[a] + t*(verts[b]-verts[a])

                    points.append(p)

# ==========================================
# Convert
# ==========================================

points = np.array(points)

# ==========================================
# Visualization
# ==========================================

fig = plt.figure(figsize=(10,10))

ax = fig.add_subplot(111, projection='3d')

ax.scatter(
    points[:,0],
    points[:,1],
    points[:,2],
    s=0.15
)

ax.set_title("MCA_WLT Point-Based CT Surface")

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.tight_layout()
plt.show()