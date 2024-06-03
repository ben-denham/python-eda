## Tutorial Resources

### Tutorial 1: Loading and Visualising

* [Speaker notes](tutorial_1/speaker_notes.html)
* [Runnable notebook with speaker notes](https://colab.research.google.com/github/ben-denham/python-eda/blob/main/tutorial_1/python_eda_tutorial_1_runnable.ipynb)

### Tutorial 2: Filtering and Transforming

* [Speaker notes](tutorial_2/speaker_notes.html)
* [Runnable notebook with speaker notes](https://colab.research.google.com/github/ben-denham/python-eda/blob/main/tutorial_2/python_eda_tutorial_2_runnable.ipynb)

### Tutorial 3: Grouping and Presenting

* [Speaker notes](tutorial_3/speaker_notes.html)
* [Runnable notebook with speaker notes](https://colab.research.google.com/github/ben-denham/python-eda/blob/main/tutorial_3/python_eda_tutorial_3_runnable.ipynb)

## Notebook Outputs

When updating the notebooks in this repo that are shared with
learners, you should not commit the outputs of notebook cells to your
Git repository. If you have Python 3 installed, you can use
[nbstripout](https://github.com/kynan/nbstripout) to configure your
Git repository to exclude the outputs of notebook cells when running
`git add`:

1. `python3 -m pip install nbstripout nbconvert`
2. Run `nbstripout --install` in this directory (installs hooks into
   `.git`).
