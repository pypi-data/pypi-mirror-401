# Headless playback client for Raphson Music

Client for the [Raphson Music server](https://codeberg.org/raphson/music-server) that can be controlled remotely via a simple web interface or [Home Assistant](https://codeberg.org/raphson/music-headless-ha/).

## Choose a player backend

* `mpv` (recommended): requires libmpv
  * Debian: `apt install libmpv2`
  * Fedora: `dnf install mpv-libs`
* `vlc`: requires libvlc
  * Debian: `apt install vlc`
  * Fedora: `dnf install vlc-libs`

## Installation

Install pipx using your system package manager.

```
pipx install --global raphson-music-headless[mpv]
```
or
```
pipx install --global raphson-music-headless[vlc]
```
or, for the latest development version:
```
pipx install --global "raphson_music_headless[mpv] @ git+https://codeberg.org/raphson/music-headless.git"
```

Run: `raphson-music-headless`

## Usage

1. Create a `config.json` file with credentials (see `config.json.example`).
2. Run `raphson-music-headless --config config.json`

By default, the program looks for a configuration file at `/etc/raphson-music-headless.json`.

See [config.md](./docs/config.md) for a list of options.

## API

See [API.md](./docs/API.md)

## Temporary files (VLC backend only)

The server writes music to temporary files so VLC can access them. On Linux, the `/tmp` directory is used for this purpose. It is strongly recommended to mount `tmpfs` on `/tmp` to avoid unnecessary writes to your disk, especially when using a Raspberry Pi with sd card.

Check if it is the case by running `mount | grep /tmp`. It should show something like: `tmpfs on /tmp type tmpfs ...`

## Cache size

The `cache_size` setting determines the number of cached tracks for each playlist. These tracks are kept in memory, consuming roughly 3 - 6MB per track including cover image. Say `cache_size` is set to 4 and you use a maximum of 10 playlists, you will need around 200MiB of memory.

## Bugs

When playing mono audio (like news), sound may only be played on the left channel. This appears to be an issue with PipeWire.
