# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# by Anime Nyan

from . import fuse_skeletons

bl_info = {
    "name": "Fuse Skeletons",
    "author": "Anime Nyan",
    "version": (1, 0, 0),
    "blender": (2, 92, 0),
    "location": "3D View > Properties > Fuse Skel",
    "description": "Adds the ability to save and load shader maps for 3d Meshes exported from Unreal Engine games and adds default preset shader maps for your convenience ",
    "warning": "",
    "wiki_url": "",
    "category": "Skeletons",
    "tracker_url": "https://github.com/AnimNyan/UEShaderScript"
}

"""
Version': '1.0.0' written by Anime Nyan

Adds two panels one in the Shader Editor View to save different preset shader maps and one in the 3D View to load shader maps.
"""


def register():
    fuse_skeletons.register()

def unregister():
    fuse_skeletons.unregister()

print("(*) Fuse Skeletons add-on loaded")
