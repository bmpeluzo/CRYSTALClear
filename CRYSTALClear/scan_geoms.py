import time
from CRYSTALClear.crystal_io import Crystal_output
import pandas as pd
import matplotlib.pyplot as plt

t0 = time.perf_counter()

scan_out = Crystal_output()._read_output('COF366_Co_slab_ferr_p4m_fieldcon001_scan.out')

# Outer loop over output data to find the scan energies 
for index, i in enumerate(reversed(scan_out.data)):           # reversed loop because the scan info is often printed last
    scan_info = i.find('MODE(CM-1)')
    if scan_info != -1:
        scan_0 = len(scan_out.data)-index-1

        # finding the individual scans and the line it finishes
        scan_dict = {}
        for index2, j in enumerate(scan_out.data[scan_0+1:]):
            scan_true = j.find('(')

            if scan_true != -1:
                scan_i = j.split('(')[0]
                scan_dict.update({int(scan_i): index2+scan_0+1}) 

            # searches for the ending line
            scan_term = j.find('SCANMODE')

            if scan_term != -1:
                scan_term_l = index2+scan_0+1
                break
        break


# Loop over the scans to build the individual plots:    
for i in list(scan_dict):

    # check if we are in the last scan
    if i == list(scan_dict)[-1]:
        
        # Two cases: scan terminated or not
        if scan_out.terminated == True:
            scan_list = scan_out.data[scan_dict[list(scan_dict)[-1]]+2:scan_term_l]
        else:
            scan_list = scan_out.data[scan_dict[list(scan_dict)[-1]]+2:len(scan_out.data)]
    else:
        scan_list = scan_out.data[scan_dict[i]+2:scan_dict[i+1]]

    for data_i, data_item in enumerate(scan_list):
        scan_list[data_i] = data_item.split()

    scan_points = pd.DataFrame(scan_list)
    scan_points.iloc[:,0:2] = scan_points.iloc[:,0:2].astype('float')

    # Plot
    plt.figure()
    plt.xlabel('Displacement')
    plt.ylabel('E - E$_{eq}$')
    plt.title('Scan %d' %i)

        
    if scan_points.iloc[:,0].shape[0] % 2 == 0:      #check if we have an even number of points (in case of non terminated jobs)
        mid_point = 0
    else:
        mid_point = scan_points[scan_points.iloc[:,0]==0].index[0]
    plt.plot(scan_points.iloc[:,0], scan_points.iloc[:,1]-scan_points.iloc[mid_point,1], marker='o', linestyle='dashed')

print(time.perf_counter()-t0)

plt.show()
plt.close()


