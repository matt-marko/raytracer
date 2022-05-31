# Ray tracer information:
This is a ray tracer I wrote in Python for my computer graphics course. It uses
a simplified version of the Blinn-Phong model to calculate the colour at each pixel 
of a prespecified scene. All of the code is contained in raytracer.py

The code takes a text file as input, examples of which are present in 
the Git repository as test1.txt, test2.txt, and test3.txt. These text files
specify the position of the objects and light sources in the scene, as well as their orientation 
and colour properties. The output is a file named image.ppm which contains the scene. Example outputs are 
also included in the Git repository as test1.png, test2.png, and test3.png.  

# How to use:
Once raytracer.py is downloaded, the code can be run by typing "python raytracer.py \<input file name\>" in the
command line. For examples of test files, see the included test.txt files. Exceptions may be raised for ill-condition inputs. Make sure to the have the input file
and raytracer.py in the same directory!

# Input File Format:
The content and syntax of the file is as follows:

Content
The near plane**, left**, right**, top**, and bottom**

The resolution of the image nColumns* X nRows*

The position** and scaling** (non-uniform), color***, Ka***, Kd***, Ks***, Kr*** and the specular exponent n* of a sphere

The position** and intensity*** of a point light source

The background colour ***

The scene’s ambient intensity***

The output file name (you should limit this to 20 characters with no spaces)
 

* int         ** float          *** float between 0 and 1

 

Syntax
NEAR <n>

LEFT <l>

RIGHT <r>

BOTTOM <b>

TOP <t>

RES <x> <y>

SPHERE <name> <pos x> <pos y> <pos z> <scl x> <scl y> <scl z> <r> <g> <b> <Ka> <Kd> <Ks> <Kr> <n>

… up to 14 additional sphere specifications

LIGHT <name> <pos x> <pos y> <pos z> <Ir> <Ig> <Ib>

… up to 9 additional light specifications

BACK <r> <g > <b>

AMBIENT <Ir> <Ig> <Ib>

OUTPUT <name>
