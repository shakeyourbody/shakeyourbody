# DEV Docs



## Run the source code

### Processing IDE

Open the `/src` folder in the processing IDE, and press the run button

### CLI

> :exclamation: 
>
> This method won't run on Windows, and is tested only on Linux. Soon or later there will be a Windows patch.

Run the following command:

``` bash
$ ./scripts/run.sh src/src.pyde
```

Requirements:

+ wget
+ Java JRE 8 - OpenJRE isn't supported!



## .pyde

The "main" python source file should be named `src.pyde` and placed in the `/src` folder. This is **mandatory** for the Processing IDE, but with the CLI scripts it can be named as a normal `.py` file.

`.pyde` is the "processing python mode" takes on files extension, and it allow the processing IDE to recognise the python mode. Behind the scenes it's a plain python file, so it's sane to force the IDE syntax to python. (this _should_ be automatised on VSCode)

