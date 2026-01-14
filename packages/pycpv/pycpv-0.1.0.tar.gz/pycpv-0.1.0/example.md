Preparation

    We have last tested this tutorial with Python 3.7.

You'll need Git to run the commands in this tutorial. Also, follow these instructions to install DVC if it's not already installed.

    See Running DVC on Windows for important tips to improve your experience on Windows.

Okay! Let's first download the code and set up a Git repository:

git clone https://github.com/iterative/example-versioning.git

cd example-versioning

This command pulls a DVC project with a single script train.py that will train the model.

Let's now install the requirements. But before we do that, we strongly recommend creating a virtual environment:

python3 -m venv .env

source .env/bin/activate

pip install -r requirements.txt

Expand to learn about DVC internals

The repository you cloned is already DVC-initialized. It already contains a .dvc/ directory with the config and .gitignore files. These and other files and directories are hidden from user, as typically there's no need to interact with them directly.
First model version

Now that we're done with preparations, let's add some data and then train the first model. We'll capture everything with DVC, including the input dataset and model metrics.

dvc get https://github.com/iterative/dataset-registry \
          tutorials/versioning/data.zip

unzip -q data.zip

rm -f data.zip

dvc get can download any file or directory tracked in a DVC repository (and stored remotely). It's like wget, but for DVC or Git repos. In this case we use our dataset registry repo as the data source (refer to Data Registry for more info.)

This command downloads and extracts our raw dataset, consisting of 1000 labeled images for training and 800 labeled images for validation. In total, it's a 43 MB dataset, with a directory structure like this:

data
├── train
│   ├── dogs
│   │   ├── dog.1.jpg
│   │   ├── ...
│   │   └── dog.500.jpg
│   └── cats
│       ├── cat.1.jpg
│       ├── ...
│       └── cat.500.jpg
└── validation
   ├── dogs
   │   ├── dog.1001.jpg
   │   ├── ...
   │   └── dog.1400.jpg
   └── cats
       ├── cat.1001.jpg
       ├── ...
       └── cat.1400.jpg

(Who doesn't love ASCII directory art?)

Let's capture the current state of this dataset with dvc add:

dvc add data

You can use this command instead of git add on files or directories that are too large to be tracked with Git: usually input datasets, models, some intermediate results, etc. It tells Git to ignore the directory and puts it into the cache (while keeping a file link to it in the workspace, so you can continue working the same way as before). This is achieved by creating a tiny, human-readable .dvc file that serves as a pointer to the cache.

Next, we train our first model with train.py. Because of the small dataset, this training process should be small enough to run on most computers in a reasonable amount of time (a few minutes). This command outputs a bunch of files, among them model.weights.h5 and metrics.csv, weights of the trained model, and metrics history. The simplest way to capture the current version of the model is to use dvc add again:

python train.py

dvc add model.weights.h5

    We manually added the model output here, which isn't ideal. The preferred way of capturing command outputs is with dvc stage add. More on this later.

Let's commit the current state:

git add data.dvc model.weights.h5.dvc metrics.csv .gitignore

git commit -m "First model, trained with 1000 images"

git tag -a "v1.0" -m "model v1.0, 1000 images"

Expand to learn more about how DVC works

As we mentioned briefly, DVC does not commit the data/ directory and model.weights.h5 file with Git. Instead, dvc add stores them in the cache (usually in .dvc/cache) and adds them to .gitignore.

In this case, we created data.dvc and model.weights.h5.dvc, which contain file hashes that point to cached data. We then git commit these .dvc files.

    Note that executing train.py produced other intermediate files. This is OK, we will use them later.

    git status
    ...
          bottleneck_features_train.npy
          bottleneck_features_validation.npy`

Second model version

Let's imagine that our image dataset doubles in size. The next command extracts 500 new cat images and 500 new dog images into data/train:

dvc get https://github.com/iterative/dataset-registry \
          tutorials/versioning/new-labels.zip

unzip -q new-labels.zip

rm -f new-labels.zip

For simplicity's sake, we keep the validation subset the same. Now our dataset has 2000 images for training and 800 images for validation, with a total size of 67 MB:

data
├── train
│   ├── dogs
│   │   ├── dog.1.jpg
│   │   ├── ...
│   │   └── dog.1000.jpg
│   └── cats
│       ├── cat.1.jpg
│       ├── ...
│       └── cat.1000.jpg
└── validation
   ├── dogs
   │   ├── dog.1001.jpg
   │   ├── ...
   │   └── dog.1400.jpg
   └── cats
       ├── cat.1001.jpg
       ├── ...
       └── cat.1400.jpg

We will now want to leverage these new labels and retrain the model:

dvc add data

python train.py

dvc add model.weights.h5

Let's commit the second version:

git add data.dvc model.weights.h5.dvc metrics.csv

git commit -m "Second model, trained with 2000 images"

git tag -a "v2.0" -m "model v2.0, 2000 images"

That's it! We've tracked a second version of the dataset, model, and metrics in DVC and committed the .dvc files that point to them with Git. Let's now look at how DVC can help us go back to the previous version if we need to.
Switching between workspace versions

The DVC command that helps get a specific committed version of data is designed to be similar to git checkout. All we need to do in our case is to additionally run dvc checkout to get the right data into the workspace.

There are two ways of doing this: a full workspace checkout or checkout of a specific data or model file. Let's consider the full checkout first. It's pretty straightforward:

git checkout v1.0

dvc checkout

These commands will restore the workspace to the first snapshot we made: code, data files, model, all of it. DVC optimizes this operation to avoid copying data or model files each time. So dvc checkout is quick even if you have large datasets, data files, or models.

On the other hand, if we want to keep the current code, but go back to the previous dataset version, we can target specific data, like this:

git checkout v1.0 data.dvc

dvc checkout data.dvc

If you run git status you'll see that data.dvc is modified and currently points to the v1.0 version of the dataset, while code and model files are from the v2.0 tag.
Automating capturing

dvc add makes sense when you need to keep track of different versions of datasets or model files that come from source projects. The data/ directory above (with cats and dogs images) is a good example.

On the other hand, there are files that are the result of running some code. In our example, train.py produces binary files (e.g. bottleneck_features_train.npy), the model file model.weights.h5, and the metrics file metrics.csv.

When you have a script that takes some data as an input and produces other data outputs, a better way to capture them is to use dvc stage add:

    If you tried the commands in the Switching between workspace versions section, go back to the master branch code and data, and remove the model.weights.h5.dvc file with:

git checkout master

dvc checkout

    dvc remove model.weights.h5.dvc

dvc stage add -n train -d train.py -d data \
          -o model.weights.h5 -o bottleneck_features_train.npy \
          -o bottleneck_features_validation.npy -M metrics.csv \
          python train.py

dvc repro

dvc stage add writes a pipeline stage named train (specified using the -n option) in dvc.yaml. It tracks all outputs (-o) the same way as dvc add does. Unlike dvc add, dvc stage add also tracks dependencies (-d) and the command (python train.py) that was run to produce the result.