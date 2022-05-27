# <a name="title">Taichi Voxel Challenge</a>: Tiny White Boat & Giant Yellow Duck 

<p align="center">
<img src="demo.jpg" width="75%"></img>
</p>

> Figure: result of `main.py`. 

<p align="center">
<img src="./results/v2.gif" width="75%"></img>
</p>

> Figure: animation result of `rubberduck.py`. 

<p align="center">
<img src="./results/360anim.gif" width="75%"></img>
</p>

> Figure: a 360-degree animation result of `rubberduck.py`. 

## My API Extension 
You can find the use of these extensional APIs in [rubberduck.py](./rubberduck.py) 

**Use right mouse button to rotate view**

### 1. GUI Widgets 

+ `sene.add_text(your_text)`
    ```py
    scene.add_text("direct light")
    ```

+ `scene.add_slider(name_of_slider, var, range_min, range_max)`
  
  Use list to pass reference of ``var``. 
  ```py
  duck_z=[11.2]
  scene.add_slider("duck z", duck_z,-64.,64.)
  ```
  

+ `scene.add_color_picker(name_of_color_picker, var)`

  Use list to pass reference of ``var``. 
  ```py
  sky_col = [(135,206,235)] 
  scene.add_color_picker("sky color", sky_col)
  ```

+ `scene.add_callback_button(name_of_callback, callback_func, callback_args_ref)`
  ```py
  scene.add_callback_button("re-light / re-wave", relight, (sky_col,))
  scene.add_callback_button("reset scene", create_scene, ())
  ```
  
+ `scene.display_camera_info()`

### 2. Scene Management 
+ `scene.reset_part_of_scene`
  
  Clear the voxels with "resetable" attributes equal to 1. 
  
  **Reason to add this api** is that the creation of duck and boat in the scene is time-consuming, while the creation of wave and splash requires little time. 
  
  So to adjust the appearence of waves for debugging, we only need to reset the voxels of waves, where we can set the voxels of waves as "resetable = 1", while the voxels of duck and boat as "resetable = 0". 

  You can set this attribute in ``set_voxel``
  ```py
  (method) set_voxel: (idx: Any, mat: Any, color: Any, resetable: int = 1) -> None
  ```

+ `scene.reset_all_scene`
  
  Clear all voxels. 

+ `scene.set_camera(cam_pos, lookat)`

### 3. Other Utilities (Animation Tools.etc)
+ `scene.save_screeshot(path)`
  ```py
  scene.save_screeshot(f"./rot_anim/{i:03d}.png")
  ```
## How to create animation or 360-degree animation

First, generate a sequence of images, then use `ti video -f your_framerate` to generate video. 

Here I introduce how to generate images. 

### 1. A simple fixed-view animation 

![](./results/v2.gif)

```py
def animate():
    scene.set_camera((-3.168, 0.929, -1.915),(-1.46, 0.2557, -0.876))
    n_frame = 40
    for i in range(n_frame):
        if i == 0:
            # arguments are the y-axis offset of duck & boat
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
```
### 2. A 360-degree Animation

![](./results/360anim.gif)
```py
import numpy as np 
from numpy.linalg import norm
def rot360_animate():
    #####################
    # replace with your create scene code / function 
    create_scene(0, 0) 
    #####################
    
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
        
        #############################
        # or scene.reset_all_scene() then create new scene based on your need
        scene.reset_part_of_scene()
        relight()
        #############################

        scene.save_screeshot(f"./rot_anim/{i:03d}.png")

```


---

We invite you to create your voxel artwork, by putting your [Taichi](https://github.com/taichi-dev/taichi) code in `main.py`!

Rules:

+ You can only import two modules: `taichi` (`pip` installation guide below) and `scene.py` (in the repo).
+ The code in `main.py` cannot exceed 99 lines. Each line cannot exceed 120 characters.

The available APIs are:

+ `scene = Scene(voxel_edges, exposure)`
+ `scene.set_voxel(voxel_id, material, color)`
+ `material, color = scene.get_voxel(voxel_id)`
+ `scene.set_floor(height, color)`
+ `scene.set_directional_light(dir, noise, color)`
+ `scene.set_background_color(color)`

Remember to call `scene.finish()` at last.

**Taichi lang documentation:** https://docs.taichi.graphics/

**Modifying files other than `main.py` is not allowed.**


## Installation

Make sure your `pip` is up-to-date:

```bash
pip3 install pip --upgrade
```

Assume you have a Python 3 environment, simply run:

```bash
pip3 install -r requirements.txt
```

to install the dependencies of the voxel renderer.

## Quickstart

```sh
python3 example1.py  # example2/3/.../7/8.py
```

Mouse and keyboard interface:

+ Drag with your left mouse button to rotate the camera.
+ Press `W/A/S/D/Q/E` to move the camera.
+ Press `P` to save a screenshot.

## More examples

<a href="https://github.com/raybobo/taichi-voxel-challenge"><img src="https://github.com/taichi-dev/public_files/blob/master/voxel-challenge/city.jpg" width="45%"></img></a>  <a href="https://github.com/victoriacity/voxel-challenge"><img src="https://github.com/taichi-dev/public_files/blob/master/voxel-challenge/city2.jpg" width="45%"></img></a> 
<a href="https://github.com/yuanming-hu/voxel-art"><img src="https://github.com/taichi-dev/public_files/blob/master/voxel-challenge/tree2.jpg" width="45%"></img></a> <a href="https://github.com/neozhaoliang/voxel-challenge"><img src="https://github.com/taichi-dev/public_files/blob/master/voxel-challenge/desktop.jpg" width="45%"></img></a> 
<a href="https://github.com/maajor/maajor-voxel-challenge"><img src="https://github.com/taichi-dev/public_files/blob/master/voxel-challenge/earring_girl.jpg" width="45%"></img></a>  <a href="https://github.com/rexwangcc/taichi-voxel-challenge"><img src="https://github.com/taichi-dev/public_files/blob/master/voxel-challenge/pika.jpg" width="45%"></img></a> 
<a href="https://github.com/houkensjtu/qbao_voxel_art"><img src="https://github.com/taichi-dev/public_files/blob/master/voxel-challenge/yinyang.jpg" width="45%"></img></a>  <a href="https://github.com/ltt1598/voxel-challenge"><img src="https://github.com/taichi-dev/public_files/blob/master/voxel-challenge/lang.jpg" width="45%"></img></a> 

## Show your artwork 

Please put your artwork at the beginning of this README file. Replacing the `demo.jpg` file with your creation will do the job.
