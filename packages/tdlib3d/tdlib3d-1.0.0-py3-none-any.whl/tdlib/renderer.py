import moderngl
import numpy as np
import pygame

class Renderer:
    def __init__(self, width=800, height=600):
        pygame.init()
        # Create OpenGL window
        self.screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
        self.ctx = moderngl.create_context()
        
        # Enable Depth Testing so close objects hide far ones
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        # The Standard 3D Shader
        self.prog = self.ctx.program(
            vertex_shader="""
                #version 330
                uniform mat4 mvp;
                uniform mat4 model;
                in vec3 in_position;
                in vec3 in_normal;
                in vec2 in_texcoord;
                out vec3 v_normal;
                out vec3 v_pos;
                out vec2 v_texcoord;
                void main() {
                    v_pos = vec3(model * vec4(in_position, 1.0));
                    v_normal = mat3(model) * in_normal;
                    v_texcoord = in_texcoord;
                    gl_Position = mvp * vec4(in_position, 1.0);
                }
            """,
            fragment_shader="""
                #version 330
                uniform vec3 lightPos;
                uniform sampler2D u_texture;
                uniform bool use_texture;
                in vec3 v_normal;
                in vec3 v_pos;
                in vec2 v_texcoord;
                out vec4 f_color;
                void main() {
                    float ambient = 0.3;
                    vec3 norm = normalize(v_normal);
                    vec3 lightDir = normalize(lightPos - v_pos);
                    float diff = max(dot(norm, lightDir), 0.0);
                    
                    vec4 baseColor = use_texture ? texture(u_texture, v_texcoord) : vec4(0.7, 0.7, 0.7, 1.0);
                    f_color = vec4(baseColor.rgb * (diff + ambient), baseColor.a);
                }
            """
        )

    def render_object(self, obj_dict, mvp_matrix, model_matrix, light_pos=(5.0, 5.0, 5.0)):
        # Upload matrices to GPU
        self.prog['mvp'].write(mvp_matrix.astype('f4').tobytes())
        self.prog['model'].write(model_matrix.astype('f4').tobytes())
        self.prog['lightPos'].write(np.array(light_pos, dtype='f4').tobytes())

        # Handle texture state
        if obj_dict.get('texture'):
            self.prog['use_texture'].value = True
            obj_dict['texture'].use(0)
        else:
            self.prog['use_texture'].value = False

        obj_dict['vao'].render()

    def clear(self, r=0.1, g=0.1, b=0.1):
        self.ctx.clear(r, g, b)