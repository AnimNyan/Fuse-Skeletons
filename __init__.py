# ##### BEGIN CC0 LICENSE BLOCK #####
#
# CC0 is a public domain dedication from Creative Commons. A work released under CC0 is 
# dedicated to the public domain to the fullest extent permitted by law. If that is not 
# possible for any reason, CC0 also provides a simple permissive license as a fallback. 
# Both public domain works and the simple license provided by CC0 are compatible with the GNU GPL.
#
#  You should have received a copy of the Creative Commons Zero Licence
#
# ##### END CC0 LICENSE BLOCK #####

# by Anime Nyan

from . import fuse_skeletons

bl_info = {
    "name": "Fuse Skeletons",
    "author": "Anime Nyan",
    "version": (1, 0, 0),
    "blender": (2, 92, 0),
    "location": "3D View > Properties > Fuse Skel",
    "description": "Adds ability to join selected Skeletons together, delete duplicate bones with the same name and reparent bones which are not duplicates to bones to the original skeleton.",
    "warning": "",
    "wiki_url": "https://github.com/AnimNyan/Fuse-Skeletons/wiki",
    "category": "Skeleton",
    "tracker_url": "https://github.com/AnimNyan/Fuse-Skeletons"
}

"""
Version': '1.0.0' written by Anime Nyan

Adds one panel in the 3d View to join Skeletons together, delete duplicate bones with the same name and reparent bones which are not duplicates to bones to the original skeleton.
"""


def register():
    fuse_skeletons.register()

def unregister():
    fuse_skeletons.unregister()

print("(*) Fuse Skeletons add-on loaded")
