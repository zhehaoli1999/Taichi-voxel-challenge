from scene import Scene
import taichi as ti
from taichi.math import *
scene = Scene(voxel_edges=0.01, exposure=1)
scene.set_floor(0, (0 / 255.,191 / 255.,255 / 255.))
scene.set_background_color((1., 1., 1.))
scene.set_directional_light((-1, 1, 0.), 0.0, (1, 1, 1))
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
def tri(r1, h, r2, round_unused, cone, vertex, p):
    r = vec3(p.x/r1, p.y, p.z/r2);rt=mix(1.0-cone,1.0,float(h-p.y)*0.5/h);r.z+=(r.x+1)*mix(-0.577, 0.577, vertex)
    q = ti.abs(r); return max(q.y-h,max(q.z*0.866025+r.x*0.5,-r.x)-0.5*rt)< 0
@ti.func
def make(func: ti.template(), p1, p2, p3, p4, p5, p6, pos, dir, up, color, mat, mode):
    max_r = 2 * int(max(p3,max(p1, p2))); dir = normalize(dir); up = normalize(cross(cross(dir, up), dir))
    for i,j,k in ti.ndrange((-max_r,max_r),(-max_r,max_r),(-max_r,max_r)): 
        xyz = proj_plane(vec3(0.0,0.0,0.0), dir, up, vec3(i,j,k))
        if func(p1,p2,p3,p4,p5,p6,xyz):
            if mode == 0: scene.set_voxel(pos + vec3(i,j,k), mat, color) # additive
            if mode == 1: scene.set_voxel(pos + vec3(i,j,k), 0, color) # subtractive
            if mode == 2 and scene.get_voxel(pos + vec3(i,j,k))[0] > 0: scene.set_voxel(pos + vec3(i,j,k), mat, color)
@ti.kernel
def initialize_voxels():
    make(elli,35.3,24.1,33.6,0.0,0.0,0.0,vec3(-6,138,-4),vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(255,248,57),1,0)
    make(elli,20.0,20.0,20.0,0.0,0.0,0.0,vec3(-5,170,-15),vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(255,245,56),1,0)
    make(elli,20.0,11.4,20.0,0.0,0.0,0.0,vec3(-4,141,22),vec3(-0.0,0.4,-0.9),vec3(1.0,-0.0,-0.0),rgb(255,245,56),1,0)
    make(elli,8.4,4.0,7.1,0.0,0.0,0.0,vec3(-5,173,-35),vec3(-0.1,0.6,0.8),vec3(1.0,0.1,0.1),rgb(255,128,55),1,0)
    make(elli,8.4,4.0,7.1,0.0,0.0,0.0,vec3(-5,169,-32),vec3(-0.0,1.0,-0.3),vec3(1.0,0.0,0.1),rgb(255,128,55),1,0)
    make(elli,20.0,10.0,20.0,0.0,0.0,0.0,vec3(-27,138,-3),vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(255,245,56),1,0)
    make(elli,20.0,9.3,20.0,0.0,0.0,0.0,vec3(17,138,-3),vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(255,245,56),1,0)
    make(elli,2.0,3.0,2.0,0.0,0.0,0.0,vec3(6,178,-30),vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(0,0,0),1,0)
    make(elli,2.0,3.0,2.0,0.0,0.0,0.0,vec3(-15,178,-31),vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(0,0,0),1,0)
initialize_voxels()
scene.finish()
