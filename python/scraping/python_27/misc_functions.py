import os


def parent_path(num_parent_directories):
    """
    returns the nth parent directory
    :param num_parent_directories: the number of directories under the parent directory
                                    must be >=1 and an integer
    :return: path of parent directory as string
    """
    if num_parent_directories <= 0 or isinstance(num_parent_directories, int) == False:
        print("Input to base_path was invalid")
        raise

    new_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

    for i in range(num_parent_directories - 1):
        new_path = os.path.abspath(os.path.join(new_path, os.pardir))

    return new_path


#Code from https://github.com/julianneq/VCR_Project/blob/master/Soil/convertDBFtoCSV.py
def convertDBFtoCSV(dbf):
    '''Converts database file to a csv'''
    table = dbf
    outfile = dbf[0:-4] + ".csv"

    fields = arcpy.ListFields(table)
    field_names = [field.name for field in fields]
    with open(outfile,'wb') as f:
        dw = csv.DictWriter(f,field_names)
        dw.writeheader()

        with arcpy.da.SearchCursor(table,field_names) as cursor:
            for row in cursor:
                dw.writerow(dict(zip(field_names,row)))

    return None
