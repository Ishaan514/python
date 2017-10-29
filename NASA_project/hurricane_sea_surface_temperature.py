
# NASA data analysis and visualization of Hurricane sea surface temperatures
# Copyright Carl Stahlberg and Eashan Siddalingaiah 2017
# Period 1 Csulak Period 5 Brady
# 3/28/17

import re
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.dates as mdates
import numpy as np
import datetime as dt
import operator

# Create 3D plot
def create_sea_surface_temp_plot3D( indate, label, storm_latitude, storm_longitude, delta_lat, delta_long, all_lines, plotfile) :
    sea_temp = []
    longitude = []
    latitude = []
    # areas to capture mid area points, create empty lists for input values
    storm_sea_temp = []
    storm_long = []
    storm_lat = []
    max_lat = storm_latitude + delta_lat
    min_lat = storm_latitude - delta_lat
    max_long = storm_longitude + delta_long
    min_long = storm_longitude - delta_long

	# Loop through all data
    for line in all_lines :
        #convert all input values to floats to be used in other commands.
        lat,long,date,st = line.split()
        lat = float(lat)
        long = float(long)
        st = float(st)

        # capture middle of plotted area, adds values that are in the correct range to empty lists
        if lat <= max_lat and lat >= min_lat and long <= max_long and long >= min_long and date == indate and st != 0:
            longitude.append(long)
            latitude.append(lat)
            sea_temp.append(st)

		# determine areas for the storm location
        if  abs(lat-storm_latitude) < 0.2 and abs(long-storm_longitude)<0.2 and date == indate and st != 0 :
             storm_long.append(long)
             storm_lat.append(lat)
             storm_sea_temp.append(st)
        
    #define plot characteristics, colors for ranges, etc.
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    plottitle = label + ' Sea Surface Temp on '+ indate
    plt.title(plottitle)

    #loop over temperature ranges
    for color, m, templow, temphigh in [('w','^',0,100),('g','^', 0, 29), ('b','^',29,29.5), ('m','^',29.5,30), ('r','^',30,30.5), ('k','^',30.5,100)]:
         color_temp = []
         color_lat = []
         color_long = []
         #scan data for certain temperature range
         for x in range(0, len(sea_temp)-1 ) :
             if sea_temp[x] >= templow and sea_temp[x] < temphigh :
                color_temp.append(sea_temp[x])
                color_lat.append(latitude[x])
                color_long.append(longitude[x])
         #convert to arrays and scatter plot		
         lat_array = np.asarray(color_lat)
         long_array = np.asarray(color_long)
         temp_array = np.asarray(color_temp)
		 # Avoid empty arrays (see http://stackoverflow.com/questions/22903114/overcome-valueerror-for-empty-array)
         try:
             ax.scatter(-lat_array, -long_array, temp_array, c=color, marker=m)
         except ValueError:
             pass

    # Plot points for the storm
    long_array = np.asarray(storm_long)
    lat_array = np.asarray(storm_lat)
    temp_array = np.asarray(storm_sea_temp)
	# Annotate storm center with yellow circle
    ax.scatter(-lat_array, -long_array, temp_array, c='yellow', s=300,  marker='o', label='Approximate Storm Center')
    ax.legend(loc=3)
    
    # Define graph annotations
    xlabel = 'North Latitude'
    ylabel = 'West Longitude'
    zlabel = 'Temp (C)'
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_zlabel(zlabel)
    ax.view_init(elev = 45, azim = 45)
    # plt.savefig(plotfile) # save the figure to a fill
    plt.show()


# Create 2D plot
def create_sea_temp_plot2D(label, start_date, end_date,reference_lat, reference_long, path_lat, path_long,  all_lines, plotfile):
	# arrays to hold data
    reference_st = []
    reference_date = []
    path_st = []
    path_date = []
    #define beginning and end date ranges for line plots
    start = dt.datetime.strptime(start_date,'%d-%b-%Y').date()
    end =   dt.datetime.strptime(end_date, '%d-%b-%Y').date()

    #loops through all data 
    for line in all_lines:
        lat,long,date,st = line.split()
        lat = float(lat)
        long = float(long)
        st = float(st)
        indate = dt.datetime.strptime(date, '%d-%b-%Y').date() 
        #build list of reference point sea temperature
        if lat == reference_lat and long == reference_long and indate <= end and indate >= start:
            reference_st.append(st)
            reference_date.append(date)

        if lat == path_lat and long == path_long and indate <= end and indate >= start:
        #build a list of path point sea temperatures
            path_st.append(st)
            path_date.append(date)
            
    tempdif = list(map(operator.sub, reference_st, path_st))

    #creates line plot
    tdates = [dt.datetime.strptime(d,'%d-%b-%Y').date() for d in path_date]
    fig = plt.figure()
    plt.plot(tdates, path_st)
    plottitle = label +' at ' + str(path_long) + ' W Long and ' + str(path_lat) + ' N Lat'
  
    xlabel = 'Date'
    ylabel = 'Degrees Centigrade'
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(plottitle)
    fig.autofmt_xdate()
    # plt.savefig(plotfile) # save the figure to a file
    plt.show()

# Create all plots
def create_plots(all_lines) :
	ref_lat   = 27.88
	ref_long  = 89.63
	path_lat  = 26.88
	path_long = 92.38
#
# Katrina: 
# Date: 27-AUG-2005
# Lat: 24.5 = 24.38
# Long:  85.3 = 85.38
#

# Date: 28-AUG-2005
# Lat: 26.3 =26.38
# Long: 88.6 = 88.63
#
#
# Isaac:
# Date: 28-AUG-2012
# Lat: 28 = 27.88
# Long: 88.29 = 88.38
#  Defines annotations for each of three hurricanes
	rita_lat = 26.38
	rita_long = 90.13
	rita_date = '23-SEP-2005'
	rita_plotfile = 'rita' + '.scatterplot' + '.png'
	isaac_lat = 27.88
	isaac_long = 88.38
	isaac_date = '28-AUG-2012'
	isaac_plotfile = 'isaac' +'.scatterplot' + '.png'
	katrina_lat = 26.38
	katrina_long = 88.63
	katrina_date = '27-AUG-2005'
	katrina_plotfile = 'katrina' + '.scatterplot' + '.png'
	katrina_lineplotfile = 'katrina' + '.lineplot' + '.png'
	isaac_lineplotfile = 'isaac' + '.lineplot' + '.png'
	rita_lineplotfile = 'rita' + '.lineplot' + '.png'
    #creates both plots for each hurricane
	create_sea_surface_temp_plot3D( rita_date, 'Rita', rita_lat, rita_long, 4, 10, all_lines, rita_plotfile)
	create_sea_surface_temp_plot3D( katrina_date, 'Katrina', katrina_lat, katrina_long, 4, 10, all_lines, katrina_plotfile)
	create_sea_surface_temp_plot3D( isaac_date, 'Isaac', isaac_lat, isaac_long, 4, 10, all_lines, isaac_plotfile)
	katrina_lineplotfile = 'katrina' + '.lineplot' + '.png'
	create_sea_temp_plot2D('Katrina Sea Surface Temp', '01-AUG-2005', '30-SEP-2005', ref_lat, ref_long, katrina_lat, katrina_long, all_lines, katrina_lineplotfile)
	create_sea_temp_plot2D('Rita Sea Surface Temp', '01-AUG-2005', '30-SEP-2005', ref_lat, ref_long, rita_lat, rita_long, all_lines, rita_lineplotfile)
	create_sea_temp_plot2D('Isaac Sea Surface Temp', '01-AUG-2005', '30-SEP-2005', ref_lat, ref_long, isaac_lat, isaac_long, all_lines, isaac_lineplotfile)


# Class to format raw NASA data
class NASAFile(object):
	# Class constructor
	def __init__(self):
		# Output list containing formatted data
		self.outputList = []

	# format all files supplied as an argument
	def formatAll(self, allFiles):
		for file in allFiles:
			self.format(file)
		return self.outputList
	
	# Format one file
	def format(self, inputFile):
		#Input file
		fin = open(inputFile)		
		numPoints = 0
		line = fin.readline()
		while line:
			# When there is a date, treat it as a date and not data
			match = re.search('\s+TIME +: ([-0-9A-Z]+)', line)
			if match:
				break
			line = fin.readline()
		date = match.group(1)
		# Obtaion longitudes
		line = fin.readline()
		line = line.strip()
		longValues = line.split('   ')
#		fout.write(str(len(longValues)-1) + '\n')
		line = fin.readline()
		line = fin.readline()
		numLats = 0
		# Get first line of data
		while line:
			columns = line.strip().split()
			# Treat latitude column unlike data
			lat = columns[0].strip()[0:-1]
			# Get latitude points
			if (len(columns) == len(longValues) + 3):
				numLats = numLats + 1
				for i in range(3, len(longValues)):
					# Get longitude
					long = longValues[i-3].strip()[0:-1]
					# Get temperature
					temp = columns[i].strip()
					if temp == '....':
						# Write BAD value to output doc in order
						self.outputList.append((str(lat) + ' ' + str(long) + ' ' + str(date) + ' ' + '0' + '\n' ))
					else:
						# Write data to output doc in order
						self.outputList.append((str(lat) + ' ' + str(long) + ' ' + str(date) + ' ' + str(temp)) + '\n' )
					# Recalculate the number of lines
					numPoints = numPoints + 1
			# Get next line
			line = fin.readline()
		fin.close()
		
if __name__ == '__main__':
	# List of all raw input data files
	allFiles = ['August.1.2005.txt','August.2.2005.txt','August.3.2005.txt','August.4.2005.txt','August.5.2005.txt','August.6.2005.txt','August.7.2005.txt','August.8.2005.txt','August.9.2005.txt','August.10.2005.txt','August.11.2005.txt','August.12.2005.txt','August.13.2005.txt','August.14.2005.txt','August.15.2005.txt','August.16.2005.txt','August.17.2005.txt','August.18.2005.txt','August.19.2005.txt','August.20.2005.txt','August.21.2005.txt','August.22.2005.txt','August.23.2005.txt','August.24.2005.txt','August.25.2005.txt','August.26.2005.txt','August.27.2005.txt','August.28.2005.txt','August.29.2005.txt','August.30.2005.txt','August.31.2005.txt','September.1.2005.txt','September.2.2005.txt','September.3.2005.txt','September.4.2005.txt','September.5.2005.txt','September.6.2005.txt','September.7.2005.txt','September.8.2005.txt','September.9.2005.txt','September.10.2005.txt','September.11.2005.txt','September.12.2005.txt','September.13.2005.txt','September.14.2005.txt','September.15.2005.txt','September.16.2005.txt','September.17.2005.txt','September.18.2005.txt','September.19.2005.txt','September.20.2005.txt','September.21.2005.txt','September.22.2005.txt','September.23.2005.txt','September.24.2005.txt','September.25.2005.txt','September.26.2005.txt','September.27.2005.txt','September.28.2005.txt','September.29.2005.txt','September.30.2005.txt','August.1.2012.txt','August.2.2012.txt','August.3.2012.txt','August.4.2012.txt','August.5.2012.txt','August.6.2012.txt','August.7.2012.txt','August.8.2012.txt','August.9.2012.txt','August.10.2012.txt','August.11.2012.txt','August.12.2012.txt','August.13.2012.txt','August.14.2012.txt','August.15.2012.txt','August.16.2012.txt','August.17.2012.txt','August.18.2012.txt','August.19.2012.txt','August.20.2012.txt','August.21.2012.txt','August.22.2012.txt','August.23.2012.txt','August.24.2012.txt','August.25.2012.txt','August.26.2012.txt','August.27.2012.txt','August.28.2012.txt','August.29.2012.txt','August.30.2012.txt','August.31.2012.txt','September.1.2012.txt','September.2.2012.txt','September.3.2012.txt','September.4.2012.txt','September.5.2012.txt','September.6.2012.txt','September.7.2012.txt','September.8.2012.txt','September.9.2012.txt','September.10.2012.txt','September.11.2012.txt','September.12.2012.txt','September.13.2012.txt','September.14.2012.txt','September.15.2012.txt','September.16.2012.txt','September.17.2012.txt','September.18.2012.txt','September.19.2012.txt','September.20.2012.txt','September.21.2012.txt','September.22.2012.txt','September.23.2012.txt','September.24.2012.txt','September.25.2012.txt','September.26.2012.txt','September.27.2012.txt','September.28.2012.txt','September.29.2012.txt','September.30.2012.txt',]

	# Read and format the files to a list in memory
	nasaFile = NASAFile()
	data = nasaFile.formatAll(allFiles)
	print('Data Formated')

	# Create plots from the data
	create_plots(data)
