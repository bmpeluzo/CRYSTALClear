import os

########################## dictionary with symmetry operations ##################################
symm_op_dict = {50: ["\'x, y, z\'\n",
                "\'-x, -y, z\'\n",
                "\'-x, y, -z\'\n",
                "\'x, -y, -z\'\n",
                "\'-x+1/2, -y+1/2, -z\'\n",
                "\'x+1/2, y+1/2, -z\'\n",
                "\'x+1/2, -y+1/2, z\'\n",
                "\'-x+1/2, y+1/2, z\'\n"],
                83: ["\'x, y, z\'\n",
                    "\'-x, -y, -z\'\n",
                    "\'-x, -y, z\'\n",
                    "\'x, y, -z\'\n",
                    "\'-y, x, z\'\n",
                    "\'y, -x, -z\'\n",
                    "\'y, -x, z\'\n",
                    "\'-y, x, -z\'\n"],
                75: ["\'x, y, z\'\n",
                     "\'-x, -y, z\'\n",
                     "\'-y, x, z\'\n",
                     "\'y, -x, z\'\n"]
                }


########################## dictionary with symmetry names - following CRYSTAL convention ##################################
symm_num_dict = {50: 'P b a n', 75: 'P 4', 83: 'P 4/m'}


def get_cif_opt(file,n_symm):         
    f_list = []
    with open(file) as f_obj:
        for l in f_obj:
            f_list.append(l)
    f_obj.close()
    
    f_list_new = []

    for l in range(len(f_list)-1,-1,-1):
        data_opt_line = f_list[l].find("data_OPT_STEP")
        if data_opt_line != -1:
            f_list_new = f_list[l:]
            break
   
    for l in range(len(f_list_new)):
        symm_name_line = f_list_new[l].find("_symmetry_space_group_name")
        if symm_name_line != -1:
            f_list_new[l] = "_space_group_name_H-M_alt              \'"+symm_num_dict[n_symm]+"\'\n"
            f_list_new.insert(l+1,"_space_group_IT_number                 "+str(n_symm)+"\n")
            for l2 in range(l+2,len(f_list_new)):
                gamma_line = f_list_new[l2].find("_cell_angle_gamma")
                if gamma_line != -1:
                    f_list_new.insert(l2+1,"\n")
                    f_list_new.insert(l2+2,"loop_\n")
                    f_list_new.insert(l2+3,"_space_group_symop_operation_xyz\n")
                    for l3 in range(len(symm_op_dict[n_symm])):
                        f_list_new.insert(l2+l3+4,symm_op_dict[n_symm][l3])
                    break
            break

    corr_cif = open(file.split(".")[0]+"_correct.cif", 'w')
    corr_cif.writelines(f_list_new)
    corr_cif.close()
