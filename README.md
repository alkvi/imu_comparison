# imu_comparison

Opal vs ActiGraph in MobGap algorithms. Data included.

# Running it yourself

~~~
git clone https://github.com/alkvi/imu_comparison.git
cd imu_comparison
python -m venv venv
~~~

If on Windows:

~~~
.\venv\Scripts\activate.bat
~~~

If on Mac or Linux:

~~~
source venv/bin/activate
~~~

~~~
python -m pip install -r requirements.txt
jupyter notebook
~~~

Note: if jupyter doesn't find the imports, you might have to install the virtual environment as a jupyter kernel. Then you can select it from the Kernel dropdown menu in Jupyter.

~~~
python -m ipykernel install --user --name=venv --display-name "Python (venv)"
jupyter notebook
~~~
