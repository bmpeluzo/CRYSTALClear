from CRYSTALClear.crystal_io import Crystal_output
import pandas as pd
import matplotlib.pyplot as plt

scan_out = Crystal_output()._read_output('COF366_Co_slab_ferr_p4m_fieldcon001_scan.out')

# Outer loop over output data to find the scan energies 
for i in reversed(scan_out.data):           # reversed loop because the scan info is often printed last
    scan_info = i.find('MODE(CM-1)')
    if scan_info != -1:
        scan_0 = scan_out.data.index(i)

        # finding the individual scans
        scan_dict = {}
        for j in scan_out.data[scan_0+1:]:
            scan_true = j.find('(')
            if scan_true != -1:
                scan_line = scan_out.data.index(j)
                scan_i = j.split('(')[0]
                scan_dict.update({int(scan_i): scan_line})
        break

# Loop over the scans to build the individual plots:    
for i in list(scan_dict):
    if scan_out.terminated == False:
    
        if i != list(scan_dict)[-1]:         # check if we are in the last element
            scan_points = pd.DataFrame(scan_out.data[scan_dict[i]+2:scan_dict[i+1]])
        else:
            scan_points = pd.DataFrame(scan_out.data[scan_dict[list(scan_dict)[-1]]+2:len(scan_out.data)])
        print(scan_points)
        scan_points = scan_points.iloc[:,0].str.split('\s+', expand=True)
        scan_points.iloc[:,1:3] = scan_points.iloc[:,1:3].astype('float')
        print(scan_points)

        # Plot
        plt.figure()
        plt.xlabel('Displacement')
        plt.ylabel('E - E$_{eq}$')
        plt.title('Scan %d' %i)

        
        if scan_points.iloc[:,1].shape[0] % 2 == 0:      #check if we have an even number of points (in case of non terminated jobs)
            mid_point = 0
        else:
            mid_point = scan_points[scan_points.iloc[:,1]==0].index[0]
        plt.plot(scan_points.iloc[:,1], scan_points.iloc[:,2]-scan_points.iloc[mid_point,2], marker='o', linestyle='dashed')
        plt.show()



