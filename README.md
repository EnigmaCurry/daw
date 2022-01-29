# daw

Python Digital Audio Workstation

## Run inside a Linux Shell Container

These instructions are tested on Arch Linux only, but in theory may work on Mac
or Windows (WSL).

 * You need GNU Make and the Bash shell.
 * For audio playback, you must install and run
   [pulseaudio](https://www.freedesktop.org/wiki/Software/PulseAudio/) on your
   host operating system.
 * Install [podman](https://podman.io/getting-started/installation).
 * Install [Linux Shell
   Containers](https://github.com/EnigmaCurry/d.rymcg.tech/tree/master/_terminal/linux)
   (ie. source the `shell.sh` in your `~/.bashrc` to import the
   `shell_container` function).
   
Clone this repository:

```
git clone https://github.com/EnigmaCurry/daw.git ~/git/vendor/enigmacurry/daw
```
   
Create a `shell_container` alias for the daw. Call it `daw`:

```
alias daw='shell_container docker=podman template=daw builddir=${HOME}/git/vendor/enigmacurry/daw dockerfile=${HOME}/git/vendor/enigmacurry/daw/Dockerfile docker_args="--volume=/run/user/$(id -u)/pulse:/run/user/1000/pulse" shared_volume=${HOME}/git/vendor/enigmacurry/daw shared_mount=/app workdir=/app/projects'
```

(See the shell_container
[Examples](https://github.com/EnigmaCurry/d.rymcg.tech/tree/master/_terminal/linux#vendored-dockerfile-example)
for more information on what this all does)

Now you can enter the `daw` subshell anytime:

```
## From the host:
daw
```

You can test if audio is working from inside the container:

```
## Run this inside the daw shell container:
## WARNING: will play loud static noise
## Press Ctrl-C to stop it
pacat -vvvv /dev/urandom
```

Inside the shell, you can run one of your python projects (you don't need any
virtualenv):

```
## Run python in the shell container:
python name_of_project.py
```

You should be able to hear sound through your host OS pulseaudio server.

You can edit any of the files in the host project directory
(`~/git/vendor/enigamcurry/daw`) using your regular editor on your host. This
directory is a shared volume (`shared_volume`) mounted directly inside the
container at `/app` (`shared_mount`), so these files are synced to the container
automatically.

You can quit the shell by pressing `Ctrl-D` or typing `exit`.

The container will remain running in the background. To stop and remove it, run:

```
## From the host:
daw --rm
```

## Run with Docker / Podman directly

If you dislike using [Linux Shell
   Containers](https://github.com/EnigmaCurry/d.rymcg.tech/tree/master/_terminal/linux),
   you can build and run the container directly with Docker or Podman.

Clone this repository:

```
git clone https://github.com/EnigmaCurry/daw.git ~/git/vendor/enigmacurry/daw
```

If using podman, set a temporary alias before following the rest of the
instructions:

```
alias docker=podman
```

Build the container image:

```
docker build -t enigmacurry/daw ~/git/vendor/enigmacurry/daw
```

Run the container:

```
PULSEAUDIO_SOCKET=/run/user/$(id -u)/pulse

docker run --rm -it \
    -v ${PULSEAUDIO_SOCKET}:/run/user/1000/pulse \
    -v ~/git/vendor/enigmacurry/daw:/app \
    --workdir=/app/projects \
    --entrypoint=/bin/bash \
    enigmacurry/daw
```

