# `gen/` Directory

Generated files for by the container go here.  This directory is because the
source path for the `Dockerfile` [`COPY`][1] statement must be in the build
context, which is the working directory where the `docker build` command is run.
For the `Makefile`, this is the project root directory.

[1]: https://docs.docker.com/engine/reference/builder/#copy

All other temporary output should go in the `Makefile`'s `$(TMP)` directory.
