#!/bin/sh
# Uninstall the global `astra` command installed by scripts/install.sh.
set -eu

MARKER="# astra-cli launcher"

ASTRA_HOME=${ASTRA_HOME:-"$HOME/.local/share/astra"}
BIN_DIR=${ASTRA_BIN_DIR:-"$HOME/.local/bin"}
PURGE=0
FORCE=0

usage() {
    cat <<'EOF'
Usage: scripts/uninstall.sh [options]

Removes the `astra` command and the package installed by scripts/install.sh.
Your config and credentials in ~/.astra are kept.

Options:
  --home DIR       Package location (default: ~/.local/share/astra, or $ASTRA_HOME)
  --bin-dir DIR    Launcher location (default: ~/.local/bin, or $ASTRA_BIN_DIR)
  --purge          Also delete ~/.astra (stored config and API keys)
  --force          Remove a launcher this script did not write
  -h, --help       Show this help
EOF
}

while [ $# -gt 0 ]; do
    case "$1" in
        --home)     ASTRA_HOME=$2; shift 2 ;;
        --bin-dir)  BIN_DIR=$2; shift 2 ;;
        --purge)    PURGE=1; shift ;;
        --force)    FORCE=1; shift ;;
        -h|--help)  usage; exit 0 ;;
        *)          echo "astra uninstall: unknown option '$1'" >&2; usage >&2; exit 2 ;;
    esac
done

LAUNCHER="$BIN_DIR/astra"
if [ -f "$ASTRA_HOME/install.txt" ]; then
    RECORDED=$(sed -n 's/^launcher=//p' "$ASTRA_HOME/install.txt" | head -n 1)
    if [ -n "$RECORDED" ]; then
        LAUNCHER=$RECORDED
    fi
fi

REMOVED=0

if [ -e "$LAUNCHER" ]; then
    if grep -qF "$MARKER" "$LAUNCHER" 2>/dev/null || [ "$FORCE" = 1 ]; then
        rm -f "$LAUNCHER"
        echo "removed $LAUNCHER"
        REMOVED=1
    else
        echo "astra uninstall: $LAUNCHER was not installed by this script (use --force to remove it)" >&2
    fi
fi

if [ -d "$ASTRA_HOME" ]; then
    rm -rf "$ASTRA_HOME"
    echo "removed $ASTRA_HOME"
    REMOVED=1
fi

for rc in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
    [ -f "$rc" ] || continue
    if grep -q '# >>> astra-cli >>>' "$rc" 2>/dev/null; then
        sed '/# >>> astra-cli >>>/,/# <<< astra-cli <<</d' "$rc" > "$rc.astra-tmp"
        mv "$rc.astra-tmp" "$rc"
        echo "removed the astra PATH entry from $rc"
    fi
done

if [ "$PURGE" = 1 ]; then
    if [ -d "$HOME/.astra" ]; then
        rm -rf "$HOME/.astra"
        echo "removed stored config and credentials ($HOME/.astra)"
    fi
elif [ -d "$HOME/.astra" ]; then
    echo "kept $HOME/.astra (config and credentials); use --purge to delete it"
fi

if [ "$REMOVED" = 0 ]; then
    echo "astra was not installed in $BIN_DIR or $ASTRA_HOME"
fi
