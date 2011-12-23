
class MapComplex(object):
    """Takes in dimensions as list [xmin, xmax, imin, imax]\
            and returns a map of the imaginary points"""

    def __init__(self, dimensions, density):
        if (dimensions[3] - dimensions[2] <= 0) or (dimensions[1] - dimensions[0] <=0):
            raise NameError("MapComplex: Invalid input size!")

        self.complexMap = self._createMap(dimensions,density)
        return

    def _createMap(self,dimensions, density):
        """Maps the pixels to the complex numbers"""
        compMap = []
        xmin, xmax = dimensions[0], dimensions[1]
        imin, imax = dimensions[2], dimensions[3]

        #Ideally the hsteps and the vsteps are the same
        hsteps = int((xmax - xmin)/density)
        vsteps = int((imax - imin)/density)

        for im in range(vsteps):
            compMap.append([])
            for x in range(hsteps):
                myComplexPair = complex(xmin + (density * x), imin + (density * im))
                compMap[im].append(myComplexPair)
        compMap.reverse()
        return compMap

    def __call__(self):
        return self.complexMap

def mandelbrot(c):
    """The default function for generating fractals, the Mandelbrot"""
    tolerance = 30
    threshold = 3

    # This is the mandelbrot set
    #Uncomment and comment the Julia set block below
    
    # M = lambda x: pow(x, 2) + c
    # nterm = M(0)

    # End Mandelbrot set

    # This is the Julia Set
    x = c
    c = complex(-0.4,0.6)
    M = lambda x: pow(x, 2) + c
    nterm = M(x)
    #End Julia Set

    for i in xrange(tolerance):
        try:
            nterm = M(nterm)
        except OverflowError:
            return 1

    square = lambda x: pow(x, 2)
    try:
        if (square(nterm.real) + square(nterm.imag)) < threshold:
            return 0
        else:
            return 1
    except OverflowError:
        return 1

class Fractals(object):
    """Wrapper class for the Fractal object which can be plotted"""
    gridsize = 100


    def __init__(self, dimensions = [-1, 1, -1, 1], density=0.01, f=mandelbrot):
        self.fractalset = []

        grid_map = self._createGrid(dimensions, density)
        
        #Map the grids generated from above into complex form
        self._complexGrids = self._mapGrid(grid_map, density)

        #Map the complex grids into fractal grids
        self.fractal = self._fractalize(f, self._complexGrids)

    def _fractalize(self, f, compMap):
        """Takes in a list of a list of ComplexMap instances\
                Which contains a list of list of complex numbers\
                Whew"""

        from PIL import Image

        def toImage(cmObject):
            """cmObject is the ComplexMap instance"""
            size = self.gridsize, self.gridsize
            cm = cmObject()
            master = []
            for item in cm:
                master.extend(item)

            #Apply default Mandelbrot Set Function
            master = map(f, master)

            col1 = (0,0,102,0)
            col2 = (255,204,51,0)

            def select_color(x):
                if x == 1: return col1
                else: return col2

            master = map(select_color, master)
            
            image = Image.new("RGBA", size, (0,0,0,0))
            image.putdata(master)
            return image

        image_width = 0
        image_height = 0
        image_list = []
        #Unpack row
        for (y, row) in enumerate(compMap):
            image_row = []

            #Unpack columns
            for item in row:
                #Unpack the individual
                image_row.append(toImage(item))

            width = len(image_row) * self.gridsize
            height = self.gridsize
            row_holder_image = Image.new("RGBA", (width, height), (0,0,0,0)) 

            for (n, image) in enumerate(image_row):
                row_holder_image.paste(image, ((n*self.gridsize),0))

            image_list.append(row_holder_image)
            
            image_width = width
            image_height = len(image_list) * self.gridsize

        image_whole = Image.new("RGBA", (image_width, image_height), (0,0,0,0))
        for (n, image) in enumerate(image_list):
            image_whole.paste(image, (0, (n*self.gridsize)))
        image_whole.save("fractal.jpg", "JPEG")

        return
        

    def _createGrid(self, dimensions, density):
        """Creates a grid system of 100 x 100 complex number\
                and returns a list of list coordinates as [ [xmin, xmax, imin, imax] ]\
                Basically, splice up your coords"""
        import math

        xmin, xmax = dimensions[0], dimensions[1]
        imin, imax = dimensions[2], dimensions[3]

        hsteps = math.ceil((xmax - xmin)/density)
        vsteps = math.ceil((imax - imin)/density)

        hgrids = int(math.ceil(hsteps/self.gridsize))
        vgrids = int(math.ceil(vsteps/self.gridsize))

        grid_inc = density * self.gridsize
        
        #Add one inside the range() because you want to include the last one
        horizontal = [[xmin + (x * grid_inc), xmin + ((x+1) * grid_inc)] for x in range(hgrids)]
        vertical = [[imin + (im * grid_inc), imin + ((im+1) * grid_inc)] for im in range(vgrids)]

        #This makes the negative to positive less confusing, positive is at index = 0
        vertical.reverse()

        grid_map = []

        for im in vertical:
            temp = []
            for x in horizontal:
                my_x = list(x)
                my_x.extend(im)
                temp.append(my_x)
            grid_map.append(temp)

        return grid_map

    def _mapGrid(self, grid_map, density):
        grids = []
        for row in grid_map:
            temp = []
            for item in row:
                temp.append(MapComplex(item, density))
            grids.append(temp)
        return grids
