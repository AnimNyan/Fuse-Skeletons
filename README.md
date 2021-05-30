# Fuse-Skeletons

## Discord
First things first, I have a discord server for questions, support and bugs find me here: https://discord.gg/rkkWSH2EMz

# Installation
### To install Fuse Skeletons:
1. Go here: https://github.com/AnimNyan/Fuse-Skeletons/releases Right click on "Fuse_Skeletons_v.X.X.X.zip" > Save Link As do NOT unzip it.
2. Open Blender and click Edit > Preferences > Add-Ons > Install > in the file explorer find "Fuse_Skeletons_v.X.X.X.zip" and select it.
3. In the Add-Ons search, search for Fuse Skeletons and enable the Add On to complete the installation.

## Video Demo and Tutorial for Fuse Skeletons
[![Fuse Skeletons Demo](https://i.ytimg.com/vi/Bq9n8KiK7qQ/maxresdefault.jpg)](https://www.youtube.com/watch?v=Bq9n8KiK7qQ "Fuse Skeletons Demo")

## What does Fuse Skeletons do?
Fuse Skeletons is a free Blender Plugin. Basically it fuses all selected skeletons into one skeleton it deletes 
any duplicates with the same name and any bones which are not duplicates it parents to the skeleton you've chosen to fuse to.

### Disclaimer: When should this plugin not be used
This plugin will consider any bone with the same name as a duplicate, even if the bones are drastically different size and
have very different transforms. Therefore, this plugin operates on the assumption that bones with the same names from different skeletons
(e.g. joint_Head_01 from Skeleton_01.ao and joint_Head from Skeleton_02.ao) are bones with the of the same size, location and scale.
If this assumption is not true, this plugin will NOT help as it have considered the wrong bones as duplicates and deleted them.

### What is the Original Skeleton/Base Skeleton?
So the original or base skeleton are just interchangeable terms I'm using to describe the skeleton you've selected to fuse to.

### What is considered a duplicate bone?
The first step is all selected skeletons are joined together.

Then a duplicate bone is considered a bone on an armature/skeleton that fulfills the following criteria:
1. It must have .001/.002/etc as suffix as this suffix occurs when skeletons are joined together and bones have the same name.
2. The bone name without the suffix must be in the original skeleton bones list.
3. The bone name with suffix must NOT be in the original skeleton bones list, otherwise it might be a bone named head.001 in the original skeleton.

### How does it do this parenting of non duplicate bones?
The plugin looks for the parent of the the non duplicate bone let's say it's joint_Head_01.001, the plugin then takes away the suffix so
the name is joint_Head_01 and then it parents the non duplicate bone to joint_Head_01 the name without the suffix from the original skeleton.