# DEV Docs



## Running the project

You can run the project by opening the `src` folder in the processing editor and press the `run` button.

### Running from the CLI

If you prefer to use another IDE there is a file `run.sh` which will run the project for you.

``` bash
$ ./run.sh src/src.pyde
```

It works only on Linux (and probably on Unix), soon or later I'll add a Windows version.

Unix requirements:

+ wget
+ Java JRE 8 - OpenJRE isn't supported!



## SRC

`/src` **MUST** contain a file called `src.pyde`, which will be the starting point of the processing app. If you run the project with the `run.sh` script it can be named as you like, with the `.py` extensions, but if you want to use the processing IDE it must be named as above.

`*.pyde` files are plain python files with a different extension, you can simply force your IDE to parse them as python file to use syntax highlighting etc...