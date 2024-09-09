# Create a virtual environment from the root directory
    python -m venv env_name
# To activate the virtual environment run the below command
    env_name\Scripts\activate
# Install requirements.txt in virtual environment
    pip install -r requirements.txt
-------------------------------------------------------------
            Creating library

# Include __init__.py file in the script folder so that the folder is considered as a package
# (Optional) Create a setup.py file: If you want to make your package installable via pip, you can create a setup.py file.

# Go to the path of the library folder and run the below command

    pip install -e .

With the package installed in editable(-e) mode, changes to the source files will be reflected immediately without needing to reinstall.

# Now you can import these libraries in the testapp and run testapp.




