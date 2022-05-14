from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(exposure=10)
scene.set_floor(-0.8, (1.0, 1.0, 1.0))
scene.set_background_color((0.0, 0., 0.))


@ti.kernel
def initialize_voxels():
    # Your code here! :-)
    scene.set_voxel(vec3(0, 0, 0), 2, vec3(0.9, 0.1, 0.1))

@ti.kernel
def set_ground():
    # 1 moon 
    # 11 stars 
    r0 = 0.2
    r1=0.025;r2=0.05;r3=0.05;r4=0.025;r5=0.05;r6=0.025;r7=0.1;r8=0.025;r9=0.025;r10=0.05;r11=0.05

    # (left-or-right, height, front-or-back,)
    x0 = vec3(0.7,0.6,-0.95)
    x1= vec3(-0.9,0.,-0.9);x2=vec3(-0.8,0.8,-0.8);x3=vec3(-0.75,0.,-0.8);x4=vec3(-0.7,0.9,-0.8);x5=vec3(-0.65,0.6,-0.8)
    x6= vec3(-0.45,0.3,-0.8);x7=vec3(-0.3,-0.1,-0.8);x8=vec3(-0.45,0.9,-0.8);x9=vec3(-0.2,0.8,-0.8);x10=vec3(0.2,0.8,-0.8)
    x11=vec3(0.5,0.4,-0.8)

    for i,j,k in ti.ndrange((-64,64), (-64,64), (-64,64)):
        x,y,z = i / 64. , j / 64., k/64.
        if y < -0.5 + 0.2 * ti.sin(x) + 0.2 * ti.sin(z) and y > -0.8: # set ground
            scene.set_voxel(vec3(i,j,k),1,vec3(64, 105, 255)/255.)

        set_stars(vec3(x,y,z),x1,r1,i,j,k);set_stars(vec3(x,y,z),x2,r2,i,j,k);set_stars(vec3(x,y,z),x3,r3,i,j,k)
        set_stars(vec3(x,y,z),x4,r4,i,j,k);set_stars(vec3(x,y,z),x5,r5,i,j,k);set_stars(vec3(x,y,z),x6,r6,i,j,k)
        set_stars(vec3(x,y,z),x7,r7,i,j,k);set_stars(vec3(x,y,z),x8,r8,i,j,k);set_stars(vec3(x,y,z),x9,r9,i,j,k)
        set_stars(vec3(x,y,z),x10,r10,i,j,k);set_stars(vec3(x,y,z),x11,r11,i,j,k);set_stars(vec3(x,y,z),x0,r0,i,j,k)

@ti.func
def set_stars(v,x,r,i,j,k):
    v = v - x
    if v.dot(v) < r**2 * 1.5:
        scene.set_voxel(vec3(i, j, k), 2, vec3(0.9, 0.9, 0.3))

#initialize_voxels()
set_ground()

scene.finish()
