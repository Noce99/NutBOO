import getpass
import os
import errno


if __name__ == "__main__":
    if getpass.getuser() != "root":
        print("You must be superuser to run this script.")
        exit()

    # Let's create the nut_bus_www_foldr folder
    nut_bus_www_folder = "/var/www/html/NutBus"
    if not os.path.exists(nut_bus_www_folder):
        os.mkdir(nut_bus_www_folder)

    # Let's create the nut_bus_www_foldr/data folder
    data_folder = os.path.join(nut_bus_www_folder, "data")
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)

    # Let's delete all the old files
    src_web_files_old = os.listdir(nut_bus_www_folder)
    for el in src_web_files_old:
        full_path = os.path.join(nut_bus_www_folder, el)
        if not os.path.isdir(full_path):
            os.remove(full_path)

    # Let's copy all the *.js *.html file
    src_web_folder = "./src_web"
    src_web_files = os.listdir(src_web_folder)
    for el in src_web_files:
        full_path = os.path.abspath(os.path.join(src_web_folder, el))
        try:
            os.link(full_path, os.path.join(nut_bus_www_folder, el))
        except OSError as e:
            if e.errno == errno.EEXIST:
                print(os.path.join(nut_bus_www_folder, el) + " is already there.")
            else:
                raise

    # Let's delete all the old files
    data_files_old = os.listdir(os.path.join(nut_bus_www_folder, "data"))
    for el in data_files_old:
        full_path = os.path.join(os.path.join(nut_bus_www_folder, "data"), el)
        if not os.path.isdir(full_path):
            os.remove(full_path)

    # Let's link all the data file
    processed_data_folder = "./datasets/processed_data"
    data_files = os.listdir(processed_data_folder)
    for el in data_files:
        full_path = os.path.abspath(os.path.join(processed_data_folder, el))
        try:
            if not os.path.isdir(os.path.join(processed_data_folder, el)):
                os.link(full_path, os.path.join(nut_bus_www_folder, "data", el))
        except OSError as e:
            if e.errno == errno.EEXIST:
                print(os.path.join(nut_bus_www_folder, "data", el) + " is already there.")
            else:
                raise
