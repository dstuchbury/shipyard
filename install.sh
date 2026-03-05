#!/usr/bin/env bash
set -euo pipefail

# ----------------------------
# Shipyard installer
# - Works when run from repo: ./install.sh
# - Works when piped: curl ... | bash
#
# Installs:
#   - yq (if missing) to ~/.local/bin/yq (no sudo)
#   - dev to ~/.local/bin/dev (symlink)
#   - shipyard repo to ~/.shipyard (if running via curl)
# ----------------------------

REPO_URL_DEFAULT="https://github.com/dstuchbury/shipyard.git"
REPO_BRANCH_DEFAULT="main"

REPO_URL="${SHIPYARD_REPO_URL:-$REPO_URL_DEFAULT}"
REPO_BRANCH="${SHIPYARD_BRANCH:-$REPO_BRANCH_DEFAULT}"

INSTALL_DIR="${SHIPYARD_HOME:-$HOME/.shipyard}"
LOCAL_BIN="${SHIPYARD_BIN_DIR:-$HOME/.local/bin}"

DEV_TARGET="$LOCAL_BIN/dev"
YQ_TARGET="$LOCAL_BIN/yq"

# IMPORTANT: logs go to stderr so we don't contaminate command substitution outputs
say() { printf "%s\n" "$*" >&2; }
die() { say "❌ $*"; exit 1; }

ensure_path_line() {
  local shell_rc="$1"
  local line="export PATH=\"$LOCAL_BIN:\$PATH\""
  grep -Fq "$line" "$shell_rc" 2>/dev/null || {
    printf "\n# Shipyard\n%s\n" "$line" >> "$shell_rc"
  }
}

detect_shell_rc() {
  if [[ -n "${ZSH_VERSION:-}" ]]; then
    echo "$HOME/.zshrc"
  else
    echo "$HOME/.bashrc"
  fi
}

install_yq_if_missing() {
  if command -v yq >/dev/null 2>&1; then
    say "✅ yq already installed: $(yq --version 2>/dev/null || true)"
    return 0
  fi

  mkdir -p "$LOCAL_BIN"

  say "Installing yq to $YQ_TARGET ..."
  local tmp
  tmp="$(mktemp)"
  curl -fsSL "https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64" -o "$tmp"
  chmod +x "$tmp"
  mv "$tmp" "$YQ_TARGET"

  say "✅ yq installed: $("$YQ_TARGET" --version 2>/dev/null || true)"
}

clone_or_update_repo_if_needed() {
  # If run from inside a cloned repo, use that checkout.
  if [[ -f "${BASH_SOURCE[0]:-}" ]]; then
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [[ -f "$script_dir/bin/dev" ]]; then
      say "✅ Using existing checkout at: $script_dir"
      echo "$script_dir"
      return 0
    fi
  fi

  # Otherwise, curl-install mode: clone/update into INSTALL_DIR
  command -v git >/dev/null 2>&1 || die "git is required but not installed"

  if [[ -d "$INSTALL_DIR/.git" ]]; then
    say "Updating Shipyard in $INSTALL_DIR ..."
    git -C "$INSTALL_DIR" fetch --quiet
    git -C "$INSTALL_DIR" checkout -q "$REPO_BRANCH"
    git -C "$INSTALL_DIR" pull -q
  else
    say "Cloning Shipyard to $INSTALL_DIR ..."
    rm -rf "$INSTALL_DIR"
    git clone --branch "$REPO_BRANCH" --depth 1 "$REPO_URL" "$INSTALL_DIR" >/dev/null
  fi

  echo "$INSTALL_DIR"
}

install_dev_command() {
  local repo_path="$1"
  [[ -f "$repo_path/bin/dev" ]] || die "Expected $repo_path/bin/dev but it wasn't found"

  mkdir -p "$LOCAL_BIN"
  chmod +x "$repo_path/bin/dev"

  ln -sf "$repo_path/bin/dev" "$DEV_TARGET"
  say "✅ Installed dev command at: $DEV_TARGET"
}

main() {
  say ""
  say "⚓ Installing Shipyard..."
  say ""

  install_yq_if_missing

  local repo_path
  repo_path="$(clone_or_update_repo_if_needed)"

  install_dev_command "$repo_path"

  local shell_rc
  shell_rc="$(detect_shell_rc)"
  ensure_path_line "$shell_rc"

  say ""
  say "✅ Done."
  say "Reload your shell:"
  say "  source \"$shell_rc\""
  say ""
  say "Then run:"
  say "  dev doctor"
  say ""
}

main "$@"
