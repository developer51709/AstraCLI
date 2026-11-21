#!/bin/sh
# Install AstraCLI as a global `astra` command.
set -eu

MARKER="# astra-cli launcher"

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_DIR=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
PKG_SRC="$REPO_DIR/astra"

ASTRA_HOME=${ASTRA_HOME:-"$HOME/.local/share/astra"}
BIN_DIR=${ASTRA_BIN_DIR:-"$HOME/.local/bin"}
PYTHON=${PYTHON:-python3}
ADD_TO_PATH=0
FORCE=0

usage() {
    cat <<'EOF'
Usage: scripts/install.sh [options]

Installs AstraCLI as the `astra` command, usable from any directory.

Options:
  --home DIR       Where to copy the package (default: ~/.local/share/astra,
                   or $ASTRA_HOME)
  --bin-dir DIR    Where to write the `astra` launcher (default: ~/.local/bin,
                   or $ASTRA_BIN_DIR)
  --python PATH    Interpreter to run it with (default: python3, or $PYTHON)
  --add-to-path    Add the launcher directory to your shell profile if it is
                   not already on PATH
  --force          Replace an existing `astra` command this script did not write
  -h, --help       Show this help
EOF
}

die() {
    echo "astra install: $*" >&2
    exit 1
}

while [ $# -gt 0 ]; do
    case "$1" in
        --home)         ASTRA_HOME=$2; shift 2 ;;
        --bin-dir)      BIN_DIR=$2; shift 2 ;;
        --python)       PYTHON=$2; shift 2 ;;
        --add-to-path)  ADD_TO_PATH=1; shift ;;
        --force)        FORCE=1; shift ;;
        -h|--help)      usage; exit 0 ;;
        *)              echo "astra install: unknown option '$1'" >&2; usage >&2; exit 2 ;;
    esac
done

LAUNCHER="$BIN_DIR/astra"
RC_FILE=$(case "$(basename "${SHELL:-sh}")" in
    bash) echo "$HOME/.bashrc" ;;
    zsh)  echo "$HOME/.zshrc" ;;
    *)    echo "$HOME/.profile" ;;
esac)

[ -f "$PKG_SRC/__main__.py" ] || die "cannot find the astra package next to this script (expected $PKG_SRC)"

PYTHON_PATH=$(command -v "$PYTHON" 2>/dev/null || true)
[ -n "$PYTHON_PATH" ] || die "python interpreter '$PYTHON' not found"

"$PYTHON_PATH" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' \
    || die "Python 3.8 or newer is required"

if ! "$PYTHON_PATH" -c 'import yaml, requests' >/dev/null 2>&1; then
    die "dependencies missing for $PYTHON_PATH
  run: $PYTHON_PATH -m pip install -r \"$REPO_DIR/requirements.txt\""
fi

if [ -e "$LAUNCHER" ] && ! grep -qF "$MARKER" "$LAUNCHER" 2>/dev/null; then
    [ "$FORCE" = 1 ] || die "$LAUNCHER already exists and was not installed by this script (use --force to replace it)"
fi

mkdir -p "$ASTRA_HOME" "$BIN_DIR"

# Preserve model configs the user added to the installed copy. Files shipped
# with the package are replaced by the new versions; extra files are kept.
KEEP_MODELS="$ASTRA_HOME/.models-backup"
rm -rf "$KEEP_MODELS"
mkdir -p "$KEEP_MODELS"
if [ -d "$ASTRA_HOME/astra/models" ]; then
    cp -R "$ASTRA_HOME/astra/models/." "$KEEP_MODELS/"
fi

rm -rf "$ASTRA_HOME/astra"
cp -R "$PKG_SRC" "$ASTRA_HOME/astra"
find "$ASTRA_HOME/astra" -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true

KEPT=""
for f in "$KEEP_MODELS"/*; do
    [ -e "$f" ] || continue
    name=$(basename "$f")
    if [ ! -e "$ASTRA_HOME/astra/models/$name" ]; then
        cp -R "$f" "$ASTRA_HOME/astra/models/$name"
        KEPT="$KEPT $name"
    fi
done
rm -rf "$KEEP_MODELS"
if [ -n "$KEPT" ]; then
    echo "kept your model configs:$KEPT"
fi

cat > "$LAUNCHER" <<EOF
#!/bin/sh
$MARKER - remove with scripts/uninstall.sh
PYTHONPATH="$ASTRA_HOME\${PYTHONPATH:+:\$PYTHONPATH}" exec "$PYTHON_PATH" -m astra "\$@"
EOF
chmod 755 "$LAUNCHER"

cat > "$ASTRA_HOME/install.txt" <<EOF
launcher=$LAUNCHER
home=$ASTRA_HOME
python=$PYTHON_PATH
source=$REPO_DIR
installed=$(date -u +%Y-%m-%dT%H:%M:%SZ)
EOF

case ":${PATH:-}:" in
    *":$BIN_DIR:"*)
        ON_PATH=1
        ;;
    *)
        ON_PATH=0
        if [ "$ADD_TO_PATH" = 1 ]; then
            if grep -q '# >>> astra-cli >>>' "$RC_FILE" 2>/dev/null; then
                echo "$BIN_DIR is already added to $RC_FILE"
            else
                {
                    echo '# >>> astra-cli >>>'
                    echo "export PATH=\"$BIN_DIR:\$PATH\""
                    echo '# <<< astra-cli <<<'
                } >> "$RC_FILE"
                echo "added $BIN_DIR to PATH in $RC_FILE (open a new shell to pick it up)"
            fi
        fi
        ;;
esac

if ! ( cd / && "$LAUNCHER" help >/dev/null 2>&1 ); then
    die "installed to $LAUNCHER but it did not run; check $PYTHON_PATH and its dependencies"
fi

echo "AstraCLI installed."
echo "  command:    $LAUNCHER"
echo "  package:    $ASTRA_HOME/astra"
echo "  interpreter: $PYTHON_PATH"

if [ "$ON_PATH" = 0 ]; then
    echo
    echo "warning: $BIN_DIR is not on your PATH, so 'astra' will not resolve yet."
    echo "  add it with:  export PATH=\"$BIN_DIR:\$PATH\""
    echo "  or re-run:    $0 --add-to-path"
fi

echo
echo "Uninstall with: $REPO_DIR/scripts/uninstall.sh"
