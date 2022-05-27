from scene import Scene
import taichi as ti
from taichi.math import *
scene = Scene(voxel_edges=0.01, exposure=1)
scene.set_floor(-64, (1,1,1)) 
sky_col = [(135,206,235)] 
scene.set_background_color(sky_col[0]) # sky 
@ti.func
def rgb(r,g,b):
    return vec3(r/255.0, g/255.0, b/255.0)
@ti.func
def proj_plane(o, n, t, p): 
    y = dot(p-o,n);xz=p-(o+n*y);bt=cross(t,n);return vec3(dot(xz,t), y, dot(xz, bt))
@ti.func
def elli(rx,ry,rz,p1_unused,p2_unused,p3_unused,p):
    r = p/vec3(rx,ry,rz); return ti.sqrt(dot(r,r))<1
@ti.func
def cyli(r1,h,r2,round, cone, hole_unused, p):
    ms=min(r1,min(h,r2));rr=ms*round;rt=mix(cone*(max(ms-rr,0)),0,float(h-p.y)*0.5/h);r=vec2(p.x/r1,p.z/r2)
    d=vec2((r.norm()-1.0)*ms+rt,ti.abs(p.y)-h)+rr; return min(max(d.x,d.y),0.0)+max(d,0.0).norm()-rr<0
@ti.func
def box(x, y, z, round, cone, unused, p):
    ms=min(x,min(y,z));rr=ms*round;rt=mix(cone*(max(ms-rr,0)),0,float(y-p.y)*0.5/y);q=ti.abs(p)-vec3(x-rt,y,z-rt)+rr
    return ti.max(q, 0.0).norm() + ti.min(ti.max(q.x, ti.max(q.y, q.z)), 0.0) - rr< 0
@ti.func
def make(func: ti.template(), p1, p2, p3, p4, p5, p6, pos, dir, up, color, mat, mode):
    max_r = 2 * int(max(p3,max(p1, p2))); dir = normalize(dir); up = normalize(cross(cross(dir, up), dir))
    for i,j,k in ti.ndrange((-max_r,max_r),(-max_r,max_r),(-max_r,max_r)): 
        xyz = proj_plane(vec3(0.0,0.0,0.0), dir, up, vec3(i,j,k))
        if func(p1,p2,p3,p4,p5,p6,xyz):
            if mode == 0: scene.set_voxel(pos + vec3(i,j,k), mat, color, 0) # additive
            if mode == 1: scene.set_voxel(pos + vec3(i,j,k), 0, color, 0) # subtractive
            if mode == 2 and scene.get_voxel(pos + vec3(i,j,k))[0] > 0: scene.set_voxel(pos + vec3(i,j,k), mat, color,0)
@ti.kernel
def duck(dv:ti.template()):
    make(elli,32.0,21.8,30.4,0.0,0.0,0.0,vec3(5,-20,-17)+dv,vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(255,248,57),1,0)
    make(elli,18.1,18.1,18.1,0.0,0.0,0.0,vec3(6,10,-27)+dv,vec3(0.0,1.0,0.0),vec3(1.0,-0.0,-0.0),rgb(255,245,56),1,0)
    make(elli,18.1,10.3,18.1,0.0,0.0,0.0,vec3(8,-16,7)+dv,vec3(-0.0,0.4,-0.9),vec3(1.0,-0.0,-0.0),rgb(255,245,56),1,0)
    make(elli,7.6,3.6,6.4,0.0,0.0,0.0,vec3(6,13,-45)+dv,vec3(-0.0,0.8,0.6),vec3(1.0,-0.1,0.1),rgb(255,128,55),1,0)
    make(elli,7.6,3.6,6.4,0.0,0.0,0.0,vec3(6,9,-42)+dv,vec3(0.0,0.9,-0.4),vec3(1.0,-0.0,0.1),rgb(255,128,55),1,0)
    make(elli,18.1,9.1,18.1,0.0,0.0,0.0,vec3(-13,-22,-15)+dv,vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(255,245,56),1,0)
    make(elli,18.1,8.4,18.1,0.0,0.0,0.0,vec3(26,-22,-16)+dv,vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(255,245,56),1,0)
    make(elli,2.0,2.4,2.4,0.0,0.0,0.0,vec3(15,17,-40)+dv,vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(0,0,0),1,0)
    make(elli,2.0,2.4,2.4,0.0,0.0,0.0,vec3(-3,17,-39)+dv,vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(0,0,0),1,0)
@ti.kernel
def boat(dv:ti.template()):
    make(cyli,6.1,2.1,10.5,0.1,0.0,0.0,vec3(-62,-39,1)+dv,vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(255,255,255),1,0)
    make(box,3.2,2.9,3.0,0.1,0.0,0.0,vec3(-62,-36,4)+dv,vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(255,255,255),1,0)
    make(cyli,1.2,2.4,1.5,0.1,0.0,0.0,vec3(-62,-31,5)+dv,vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(255,36,11),1,0)
    make(cyli,7.2,2.6,12.4,0.1,0.0,0.0,vec3(-62,-40,1)+dv,vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(0,0,128),1,0)
@ti.kernel 
def sea(duck_z:ti.f32, prob:ti.f32, scale:ti.f32,r_boat:ti.f32): # i: left/right wing,  j: head/tail
    for i, h, j in ti.ndrange((-64, 64), (-64, -40), (-64, 64)):
        scene.set_voxel(vec3(i, h, j), 1, rgb(85+2*h,205+2*h,255)) # sea base 
    for i, h, j in ti.ndrange((-15, 59), (-40, -38), (-17+duck_z-36, 64)):
        if scene.get_voxel(vec3(i, h, j))[0]==0:
            if j < 0:
                t = (vec2(i, j) - vec2(20,-15+duck_z));r = 37
                if t.dot(t) < r**2 and ti.random(float) > 0.9:                
                    scene.set_voxel(vec3(i, h, j), 2, rgb(255,255,255)) # wave
            elif ti.random(float) > prob - scale * abs(i-20):
                scene.set_voxel(vec3(i, h, j), 2, rgb(255,255,255)) # wave
    for i, h, j in ti.ndrange((-51, -33), (-40, -39), (-12, 64)):
        if scene.get_voxel(vec3(i, h, j))[0]==0:
            if j < 10:
                if j < 1:
                    s = 12.4 / 7.2;t = vec2((i-(-42)) *s, j-1)
                    if ti.random(float) > 0.8 and t.dot(t) < r_boat**2:  
                        scene.set_voxel(vec3(i, h, j), 2, rgb(255,255,255)) # wave
                elif ti.random(float) > 0.8:  
                    scene.set_voxel(vec3(i, h, j), 2, rgb(255,255,255)) # wave
            elif ti.random(float) > 0.85 - 0.005 * abs(i+42) + 0.0015 * (j+13):
                scene.set_voxel(vec3(i, h, j), 2, rgb(255,255,255)) # wave
dir_x = [-0.5];dir_y = [1.78];dir_z = [-1.26]
duck_x=[15.];duck_y=[-12.];duck_z=[11.2]
bx=[20.];by=[0.];bz=[0.] # boat 
prob= [1.0];scale=[0.002];r_boat=[15.4]
def relight(sky_col):
    scene.set_background_color(sky_col[0])
    scene.set_directional_light([dir_x[0], dir_y[0], dir_z[0]], 0.0, (1, 1, 1));sea(duck_z[0],prob[0],scale[0],r_boat[0])
def create_scene(offset_duck=0,offset_boat=0):
    scene.reset_all_scene();duck(vec3(duck_x[0],duck_y[0]+offset_duck,duck_z[0]));boat(vec3(bx[0],by[0]+offset_boat,bz[0]));relight(sky_col)

def animate():
    scene.set_camera((-3.168, 0.929, -1.915),(-1.46, 0.2557, -0.876))
    n_frame = 40
    for i in range(n_frame):
        if i == 0:
            create_scene(0, 0)
        elif i == 8:
            create_scene(1, 0)
        elif i == 16:
            create_scene(1, -1)
        elif i == 24:
            create_scene(0, 0)
        elif i == 32:
            create_scene(-1, 1)
        else:
            scene.reset_part_of_scene()
            relight()
        scene.save_screeshot(f"./anim/{i:03d}.png")

import numpy as np 
from numpy.linalg import norm
def rot360_animate():
    create_scene(0, 0) # replace with your create scene code / function 
    
    lookat = (0, -0.3, 0)
    init_pos = (-3.168, 0.929, -1.915)
    rot_center = (lookat[0], init_pos[1], lookat[2])
    radius = norm(np.array(init_pos) - np.array(rot_center))

    n_frame = 100
    for i in range(n_frame):
        theta = (2 * np.pi / n_frame) * i
        cam_pos = np.array(rot_center) + radius * np.array([np.sin(theta), 0., np.cos(theta)])
        print(f"cam_pos = {cam_pos}")
        scene.set_camera(cam_pos, lookat)
        scene.reset_part_of_scene()
        relight()

        scene.save_screeshot(f"./rot_anim2/{i:03d}.png")

create_scene()
scene.add_text("Use right mouse button to rotate view")
scene.add_text("position offset")
scene.add_slider("duck x",duck_x,-64.,64.)
scene.add_slider("duck y",duck_y,-64.,64.)
scene.add_slider("duck z", duck_z,-64.,64.)
scene.add_slider("boat x",bx, -64.,64.)
scene.add_slider("boat y",by, -64, 64.)
scene.add_slider("boat z",bz, -64, 64)

scene.add_text("wave")
scene.add_slider("prob",prob,0.,1.)
scene.add_slider("scale",scale,0.,0.005)
scene.add_slider("r boat", r_boat, 0., 30)

scene.add_text("direct light")
scene.add_slider("direct light x",dir_x, -2., 2. )
scene.add_slider("direct light y",dir_y, -2., 5. )
scene.add_slider("direct light z",dir_z, -2., 2. )

scene.add_color_picker("sky color", sky_col)

scene.add_callback_button("re-light / re-wave", relight, (sky_col,))
scene.add_callback_button("reset scene", create_scene, ())
scene.display_camera_info()

#animate()

# rot360_animate()

scene.finish()