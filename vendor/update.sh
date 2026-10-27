#!/bin/bash
set -e

export VENDOR="$(pwd)/vendor"
echo "[+] Vendor path: $VENDOR"

# pip stores license notices in the package's dist-info directory, which is
# removed below. Copy them into the importable package directory first.
preserve_dist_info_licenses() {
    echo "[+] Preserve license notices before stripping dist-info"
    for dist_info in "$VENDOR"/*.dist-info; do
        [ -d "$dist_info" ] || continue

        if [ -f "$dist_info/top_level.txt" ]; then
            packages=$(cat "$dist_info/top_level.txt")
        else
            name=$(basename "$dist_info" .dist-info | sed -E 's/-[0-9].*$//')
            name_lc=$(echo "$name" | tr '[:upper:]' '[:lower:]')
            case "$name_lc" in
                pyyaml) packages="yaml _yaml" ;;
                *) packages="$name" ;;
            esac
        fi

        for pkg in $packages; do
            [ -d "$VENDOR/$pkg" ] || continue
            find "$dist_info" -type f \( -iname 'LICENSE*' -o -iname 'COPYING*' -o -iname 'NOTICE*' \) -print0 |
                while IFS= read -r -d '' notice; do
                    dest_name=$(basename "$notice")
                    case "$dest_name" in
                        *.md) dest_name="${dest_name%.md}" ;;
                    esac
                    cp "$notice" "$VENDOR/$pkg/$dest_name"
                done
        done
    done
}

echo "[+] Delete all folders in vendor"
rm -rf "$VENDOR/*/"

if [ -f $PWD/Pipfile ]; then
    echo "[+] Install all dependencies (pipenv)"
    pipenv run pip freeze > "$VENDOR/requirements.txt"
    pip install -r "$VENDOR/requirements.txt" --target=$VENDOR --upgrade

    preserve_dist_info_licenses

    echo "[+] Clean up vendor folder"
    rm -rf $VENDOR/*dist-info && \
        rm -rf $VENDOR/requirements.txt

elif [ -f $PWD/requirements.txt ]; then
    echo "[+] Install all dependencies (pip -> requirements)"
    pip install -r $PWD/requirements.txt --target=$VENDOR --upgrade

    preserve_dist_info_licenses

    echo "[+] Clean up vendor folder"
    rm -rf $VENDOR/*dist-info && \
        rm -rf $VENDOR/requirements.txt

else 
    echo "[!] Unsupported Python installer, please update the 'vendor/update.sh' script"
    exit 1
fi

echo "[+] Completed vendor update"
