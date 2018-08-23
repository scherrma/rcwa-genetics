# rcwa-genetics
This is a RCWA-based genetic algorithm setup using S4 for simulations.

Any search using project will use at code from at least three files: a top level file directing the particular search (eg single.py), a particular type of grating (eg gratings/zcg.py), and the generic grating class (gratings/grating.py).

--

The generic grating class handles most details shared between the specific gratings types: basic initialization, string representation, equality checking, find a peak and determining the figure of merit of a transmittance curve, and mutating and crossbreeding gratings. The generic grating should work for any type of grating that can be described with a relatively short list of numbers - each zero-contrast grating can be described with just five values - but will not work for a grating that requires a more detailed description (eg, a two-dimensional grating with a polygon on the surface). If you're looking to change something about all gratings, this is the place to do so.

__init__ has three arguments: params, wavelengths, and target. params is a tuple of numbers that will describe the grating; the count and order of these values is determined by the specific grating subclass. wavelengths is a numeric triplet: the first wavelength to simulate at, the last wavelength to simulate at, and the total number of wavelengths to simulate. Finally, target is the wavelength that the grating should evaluate performance at (a perfect filter at 11um is not useful if you want to filter at 9um, after all).

setparam lets you lock a parameter in one of three ways (depending on the mode selected). Enter the textual name of the parameter (the one in the labels defined in the specific gratings), a numeric value to lock to, and a mode: '=', '<', or '>'. Mode '=' sets the parameter equal to the value you entered, mode '<' requires that the parameter be less than or equal to the entered value, and mode '>' requires that the parameter be greater than or equal to the entered value.

--

The specific grating classes are subclasses of the generic grating class and describe the unique aspects of the grating. These subclasses usually do three things: finish initialization, define materials, and define the simulation that will generate their transmittance curve.

These classes overwrite the generic grating's __init__, but should immediately run that as their first line. Following lines should establish what the parameters actually are (eg d, ff, tline, tslab, and tstep for a ZCG) and determine the textual labels for these values that will be used when the grating is printed.

Material definition should happen at the beginning of the class. Data on the refractive index and extinction coefficient is stored in the materials folder; data sets for new materials should also be stored there.

The evaluate function of a specific grating is what really distinguishes different grating subclasses. This is where the S4 model used in simulation is constructed and used to determine the transmittance curve in the range of interest.

Changes that only alter a specific type of grating should be made in that grating type's file.

--

The top level file is what sets up a particular run. In the simple case, where a single grating is evaluated, that grating is constructed, evaluated, and printed. single.py is a faily good example of this kind of bery basic work.

Alternatively, the top-level file can be more complex (as in search.py, which conducts a genetic algorithm search using a generation of gratings).

These are the files to look at if you want to use these gratings but don't need to change any of the underlying structure.

--

The generation file handles many of the details of the genetic algorithm work. It should work on any object that has evaluate(), mutate(), and crossbreed() functions and a fom member variable, whether that be a grating or a cat-herding algorithm. When constructed it takes a seed (an example of the thing to be experimented on), the number of objects in a generation, a mutation rate, and the number of the best gratings to automatically pass on to the next generation (ie, elite = 4 means that the top four members of the generation will automatically be added to the next generation). It handles string representation, evaluation and comparison of the members of that generation, and the construction of a new generation from the current one. 

Changes to the genetic algorithm search process should take place here.`
