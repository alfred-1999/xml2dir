# xml2dir

A C++17 service that watches a queue directory for XML files and routes each
file into a subdirectory based on its `<route>` tag. All activity is logged.

## How it works

1. Drop an XML file into the **queue** directory.
2. The service reads it and parses the `<route>` tag (e.g. `<route>A</route>`).
3. The file is moved to `outputRoot/A/`. If the tag is missing or the XML is
   invalid, it goes to `outputRoot/UNSORTED/`.
4. Files already present at the destination are skipped.

Example input:

```xml
<message>
  <route>A</route>
  <payload>hello</payload>
</message>
```

## Dependencies

```sh
# openSUSE
sudo zypper install gcc-c++ cmake pugixml-devel gtest

# Debian/Ubuntu
sudo apt install g++ cmake libpugixml-dev libgtest-dev
```

## Build

```sh
mkdir -p build && cd build
cmake ..
cmake --build .
```

## Run

```sh
./xml2dir ../config/xml2dir.conf
```

Stop it cleanly with `Ctrl+C` (SIGINT) or `SIGTERM`.

## Configuration

Edit `config/xml2dir.conf`:

```ini
queueDir=/var/lib/xml2dir/queue
outputRoot=/var/lib/xml2dir/output
logFile=/var/log/xml2dir/xml2dir.log
pollIntervalMs=1000
```

## Run as a systemd service

```sh
sudo cp systemd/xml2dir.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now xml2dir
sudo systemctl status xml2dir     # check it's running
sudo systemctl stop xml2dir       # stop it (service no longer routes)
```

## Tests

```sh
cd build
cmake .. -DBUILD_TESTS=ON
cmake --build .
ctest --output-on-failure
```

## Packaging (OBS / RPM)

See `obs/xml2dir.spec`. Build with `osc build` against your OBS project.