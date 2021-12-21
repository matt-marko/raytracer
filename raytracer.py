"""
Matt Marko
April 2021

    This is a basic ray tracer I wrote for my computer graphics course. It uses
a simplified version of the Blinn-Phong model to calculate the colour at each pixel 
of the scene.

    The code takes a text file as input, examples of which are present in 
the Git repository as test1.txt, test2.txt, and test3.txt. These text files
specify the position of the objects and light sources in the scene, as well as their orientation 
and colour properties. The output is a file named image.ppm which contains the scene. Example outputs are 
also included in the Git repository as test1.png, test2.png, and test3.png.  

    If downloaded, the code can be run by typing "python raytracer.py <input file name>" in the
command line. Exceptions may be raised for ill-condition inputs. Make sure to the have the input file
and raytracer.py in the same directory
"""

import numpy as np
import array
import math
import sys

# Find the file
def getFile(name):
    myFile = open(name,"r")
    return myFile 

# Find the inputs
def getInputs(file):
    lines = []
    for line in file:
        lines.append(line)
    return lines

# Receive spheres
def getSpheres(inputs):
    spheres = []
    numSpheres = 0
    for i in range(0,len(inputs)):
        if(inputs[i] == []):
            continue
        if(inputs[i][0] != "SPHERE"):
            continue
        curr = inputs[i]
        
        spheres.extend([{"pos":[float(curr[2]),float(curr[3]),float(curr[4])]}])
        spheres[numSpheres]["scl"] = [float(curr[5]),float(curr[6]),float(curr[7])]
        spheres[numSpheres]["rgb"] = [float(curr[8]),float(curr[9]),float(curr[10])]
        spheres[numSpheres]["K"] = [float(curr[11]),float(curr[12]),float(curr[13]),float(curr[14])]
        spheres[numSpheres]["n"] = float(curr[15])

        numSpheres += 1  
        
    return spheres

# Receive lights
def getLights(inputs):
    lights = []
    numLights = 0
    for i in range(0,len(inputs)):
        if(inputs[i] == []):
            continue
        if(inputs[i][0] != "LIGHT"):
            continue
        curr = inputs[i]
        
        lights.extend([{"pos":[float(curr[2]),float(curr[3]),float(curr[4])]}])
        lights[numLights]["Irgb"] = [float(curr[5]),float(curr[6]),float(curr[7])]
  
        numLights += 1   
    
    return lights

# Normalize a vector
def normalize(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return np.array([1,1,1])
    else:
        return vector/norm

# Calculate the light and colour properties
# based on the simplified variation of the
# Phong illumination model
def theLight(sphere,lights,ambient,N,dire):
    # V is the vector from the intersection point to our eye
    V = normalize(dire)
    
    # N is the normal from the surface of the sphere
    N = normalize(N)
    
    # R is the vector of reflection
    R = normalize(2*np.dot(N,V)*N - V)
    
    n = sphere["n"]
	
	# calculate the intensity of the colour red
    red = sphere["K"][0] * ambient[0] * sphere["rgb"][0]

    for i in range(0,len(lights)):
        L = normalize(np.array(lights[i]["pos"]) - np.array(sphere["pos"]))
        NL = max(0,np.dot(N,L))
        RV = max(0,np.dot(R,V))

        red += sphere["K"][1] * lights[i]["Irgb"][0] * sphere["rgb"][0] * NL
        red += sphere["K"][2] * lights[i]["Irgb"][0] * sphere["rgb"][0] * (RV**n)

    # normalize the value to lie in the interval [0,1]
    red = min(red,1)
    red = max(red,0)
        
	# now do it for the colour green
    green = sphere["K"][0] * ambient[1] * sphere["rgb"][1]

    for i in range(0,len(lights)):
        L = normalize(np.array(lights[i]["pos"]) - np.array(sphere["pos"]))
        NL = max(0,np.dot(N,L))
        RV = max(0,np.dot(R,V))
		
        green += sphere["K"][1] * lights[i]["Irgb"][1] * sphere["rgb"][1] * NL
        green += sphere["K"][2] * lights[i]["Irgb"][1] * sphere["rgb"][1] * (RV**n)

    green = min(green,1)
    green = max(green,0)
    
	# again, for the colour blue
    blue = sphere["K"][0] * ambient[2] * sphere["rgb"][2]
    
    for i in range(0,len(lights)):
        L = normalize(np.array(lights[i]["pos"]) - np.array(sphere["pos"]))
        NL = max(0,np.dot(N,L))
        RV = max(0,np.dot(R,V))
		
        blue += sphere["K"][1] * lights[i]["Irgb"][2] * sphere["rgb"][2] * NL
        blue += sphere["K"][2] * lights[i]["Irgb"][2] * sphere["rgb"][2] * (RV**n)

    blue = min(blue,1)
    blue = max(blue,0)

    return np.array([red,green,blue])

# Draw our Spheres
def drawSphere(pixels,spheres,near,res,ambient,lights):
    closest = np.inf
    closestIndex = 0
    progress = 0
    inShadow = False
    
    for i, y in enumerate(np.linspace(1,-1,res[1])):
        for j, x in enumerate(np.linspace(-1,1,res[0])):
            thisPix = np.array([x,y,-near])
            dire = normalize(thisPix)
            
			# print progress bar
            if progress < i:
                progress += res[1]/10
                print(str(math.floor((i/res[1])*100)) + "%")
            
            for l in range(0,len(spheres)):
                hit = intersect(spheres[l]["pos"],dire,spheres[l]["scl"],np.array([0,0,0]))
                
                if(hit != None and hit < closest):
                    closest = hit
                    closestIndex = l
            
            # If a sphere has been intersected, find the corresponding colour of the pixel
            if(closest < np.inf):
                center = np.array(spheres[closestIndex]["pos"])
                dire = dire*closest
                normal = dire-center
                normal[0] = 2*normal[0]*(1/spheres[closestIndex]["scl"][0])
                normal[1] = 2*normal[1]*(1/spheres[closestIndex]["scl"][1])
                normal[2] = 2*normal[2]*(1/spheres[closestIndex]["scl"][2])
                pixels[i][j] = 255*theLight(spheres[closestIndex],lights,ambient,normal,dire)

            closest = np.inf
            
    return pixels
    
# Calculate the intersection of a ray with a sphere
def intersect(center,unscaled,scale,origin):
    # Ray: S + ct
    S = np.array(origin)-np.array(center)
    
    S[0] = S[0]/scale[0] 
    S[1] = S[1]/scale[1]
    S[2] = S[2]/scale[2]
    
    # This is the unit direction vector pointing from our eye to the pixel in question
    dire = normalize(np.array([1/scale[0]*unscaled[0],1/scale[1]*unscaled[1],1/scale[2]*unscaled[2]]))

    b = 2*np.dot(S,dire)
    c = np.linalg.norm(S)**2 - 1
    discriminant = b**2 - 4*c 

    # Substituting the equation of a ray into that of a sphere
    # yields a quadratic. Here we check whether that quadratic 
    # has any real solutions or not
    if discriminant > 0:
        inter1 = (-b + np.sqrt(discriminant)) / 2
        inter2 = (-b - np.sqrt(discriminant)) / 2
        if inter1 > 0 and inter2 > 0:
            return min(inter1,inter2)
        else:
            return None
    else:
        return None

def main():
    # Receive input
    myFile = getFile(sys.argv[1])
    inputs = getInputs(myFile)

    for i in range(0,len(inputs)):
        inputs[i] = inputs[i].split()
    
    for i in range(0,len(inputs)):
        if inputs[i] == []:
            continue
        if inputs[i][0] == "NEAR":
            near = float(inputs[i][1])
        elif inputs[i][0] == "LEFT":
            left = float(inputs[i][1])
        elif inputs[i][0] == "RIGHT":
            right = float(inputs[i][1])
        elif inputs[i][0] == "BOTTOM":
            bottom = float(inputs[i][1])
        elif inputs[i][0] == "TOP":
            top = float(inputs[i][1])
        elif inputs[i][0] == "RES":
            res = [int(inputs[i][1]),int(inputs[i][2])]
        elif inputs[i][0] == "BACK":
            back = [float(inputs[i][1]),float(inputs[i][2]),float(inputs[i][3])]
        elif inputs[i][0] == "AMBIENT":
            ambient = [float(inputs[i][1]),float(inputs[i][2]),float(inputs[i][3])]
        if inputs[i][0] == "OUTPUT":
            output = inputs[i][1]
        
    spheres = getSpheres(inputs)
    lights = getLights(inputs)

    # Declare pixels
    pixels = [[[255*back[0],255*back[1],255*back[2]]]*res[0] for i in range(0,res[1])]
    
    print("Start")
    
    # Colour Parameters
    ncol = res[0]
    nrow = res[1]
    maxval = 255
    
    ppm_header = f'P6 {res[0]} {res[1]} {maxval}\n'

    # Perform the ray tracing
    pixels = drawSphere(pixels,spheres,near,res,ambient,lights)
    
    # Normalize the resolution of the image
    final = [0]*res[0]*res[1]*3

    for i in range(0,nrow):
        for j in range(0,ncol):
            for k in range(0,3):
                final[3*j+i*ncol*3+k] = int(pixels[i][j][k])
    
    image = array.array('B', final)
    
    # Draw the image
    with open('image.ppm','wb') as f:
        f.write(bytearray(ppm_header, 'ascii'))
        image.tofile(f)
    
    print("Done")
    
main()