import trimesh
import pygame
import numpy as np

def load_resource(renderer, file_path, texture_path=None):
    """
    Parses a 3D file and returns a dictionary containing 
    the VAO (Vertex Array Object) and Texture.
    """
    # Load with trimesh (supports .obj, .stl, .glb, etc.)
    mesh = trimesh.load(file_path)
    if isinstance(mesh, trimesh.Scene):
        mesh = mesh.dump(concatenate=True)

    # Convert geometry to bytes for ModernGL
    v_data = mesh.vertices.astype('f4').tobytes()
    n_data = mesh.vertex_normals.astype('f4').tobytes()
    
    # Handle UV coordinates for textures
    if hasattr(mesh.visual, 'uv'):
        t_data = mesh.visual.uv.astype('f4').tobytes()
    else:
        # Fallback to zeros if no UVs exist
        t_data = np.zeros((len(mesh.vertices), 2), dtype='f4').tobytes()

    # Create Buffers on the GPU
    vbo = renderer.ctx.buffer(v_data)
    nbo = renderer.ctx.buffer(n_data)
    tbo = renderer.ctx.buffer(t_data)

    # Link buffers to the shader variables
    vao = renderer.ctx.vertex_array(renderer.prog, [
        (vbo, '3f', 'in_position'),
        (nbo, '3f', 'in_normal'),
        (tbo, '2f', 'in_texcoord')
    ])

    texture = None
    if texture_path:
        texture = load_texture(renderer, texture_path)

    return {"vao": vao, "texture": texture}

def load_texture(renderer, path):
    """Loads an image file as an OpenGL texture."""
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.flip(img, False, True) # Flip for OpenGL coordinate system
    data = pygame.image.tostring(img, "RGBA")
    
    tex = renderer.ctx.texture(img.get_size(), 4, data)
    tex.build_mipmaps()
    return tex