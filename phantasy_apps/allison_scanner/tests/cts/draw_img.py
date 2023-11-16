"""Generate an image file from pixel values.
"""
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("image-20231110T110123-data.csv", index_col=0)
x, y = df.x, df.y
xdim = len(df.x.unique())
ydim = len(df.y.unique())
z = df.z.to_numpy().reshape(ydim, xdim)

fig, ax = plt.subplots(1, 1)
ax.imshow(z, extent=(min(x), max(x), min(y), max(y)), origin="lower", aspect="auto", cmap="jet")
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
fig.savefig("image.png", dpi=120)
