import csv
import bpy
import math

#MARK: reads path from file
#reads into xpoints, ypoints, zpoints
x= open('C:/Users/Larissa/Desktop/Fall 2016/EECS 398/Blender/floor/floor.csv')
reader= csv.reader(x)
# first row: labels
fi = list(reader)


#store labels separately
labels = [' '] * len(fi[0])
x = 0
for label in fi[0]:
    labels[x] = label
    x = x + 1

#store each value as a number
for val in fi:
    i = 0
    for v in val:
        try: 
            val[i] = float(v)
            if (math.isnan(val[i])):
                val[i] = 0
        except ValueError:
            val[i] = 0
        i = i + 1


def import_curve(curve_name):
    hand_i = -1
    x = 0
    for label in labels:
        if (label == curve_name):
            hand_i = x
            break
        x = x + 1

        
    if hand_i != -1:
        #create new curve to pin cube to
        xpoints = [0] *(len(fi) - 2)
        zpoints = [0] * len(xpoints)
        ypoints = [0] * len(xpoints)
        for n in range(len(fi) - 2):
            x = fi[n + 1][hand_i] * 0.01
            y = fi[n + 1][hand_i + 1] * 0.01
            z = fi[n + 1][hand_i + 2] * 0.01
            # if value is 0 (dropped): use average of previous/next if next isn't out of range or also zero
            # otherwise, just use previous value
            if (x == 0):
                if (n + 2 < len(fi)) and (fi[n + 2][hand_i] != 0):
                    x = (prevX + fi[n + 2][hand_i] * 0.01) / 2
                else:
                    x = prevX
            if (y == 0):
                if (n + 2 < len(fi)) and (fi[n + 2][hand_i + 1] != 0):
                    y = (prevY + fi[n + 2][hand_i + 1] * 0.01) / 2
                else:
                    y = prevY
            if (z == 0):
                if (n + 2 < len(fi)) and (fi[n + 2][hand_i + 2] != 0):
                    z = (prevZ + fi[n + 2][hand_i + 2] * 0.01) / 2
                else:
                    z = prevZ
            xpoints[n] = x
            ypoints[n] = y
            zpoints[n] = z
            prevX = x
            prevY = y
            prevZ = z



    #MARK: build curve from points collected in xpoints, ypoints, zpoints arrays
    # clear out all objects so our references don't get confused


        # create new curve
        curveData = bpy.data.curves.new('Curve_' + curve_name, type='CURVE')
        curveData.dimensions = '3D'
        curveData.resolution_u = 2
        # map coords to spline
        polyline = curveData.splines.new('NURBS')
        polyline.points.add(len(xpoints))

        # copy points onto curve
        for n in range(len(xpoints)):
            polyline.points[n].co = (xpoints[n], ypoints[n], zpoints[n], 1)


        curveOB = bpy.data.objects.new('Curve_' + curve_name, curveData)

        # attach to scene and validate context
        scn = bpy.context.scene
        scn.objects.link(curveOB)
        scn.objects.active = curveOB


        # create a cube so it follows along the path
        bpy.ops.object.empty_add(type='PLAIN_AXES', radius=1, view_align=False, location=(0, 0, 0), rotation=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        cube = bpy.data.objects['Empty']
        #make it small so its easier to see
        bpy.context.object.scale = (0.125, 0.125, 0.125)

        # direct this cube along the path
        cube.select = True
        #curve.select = True
        bpy.ops.object.constraint_add(type='FOLLOW_PATH')
        cube.constraints["Follow Path"].target = curveOB# this was really frustrating
        force={'constraint':cube.constraints["Follow Path"]}
        bpy.ops.constraint.followpath_path_animate(force, constraint="Follow Path", owner='OBJECT', frame_start=1, length=100)
        cube.name = 'Empty_' + curve_name


#get all of the necessary curves
import_curve('WRU_RightWristUpper') 

bpy.context.scene.frame_end = 110

# NOTE: shortcut for viewing animation: with mouse over the scene (the view where you can actually see the path/cube), press Alt + A