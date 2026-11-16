#!/usr/bin/env bash
# Revisa las herramientas para editar. Con --install instala lo que falta (Claude lo corre con el OK de la persona).
#   bash setup_check.sh            → solo revisa
#   bash setup_check.sh --install  → revisa e instala lo que se pueda sin contraseña
INSTALL=0; [ "$1" = "--install" ] && INSTALL=1
OS="$(uname -s)"
MISSING=(); MANUAL=()
ok(){ printf "  ✅ %s\n" "$1"; }
miss(){ printf "  ❌ %s\n" "$1"; MISSING+=("$1"); }

# Homebrew en Mac: si no está en el PATH pero sí instalado, cargarlo
if [ "$OS" = "Darwin" ] && ! command -v brew >/dev/null; then
  for b in /opt/homebrew/bin/brew /usr/local/bin/brew; do [ -x "$b" ] && eval "$($b shellenv)"; done
fi

pkg_install(){  # $1 = paquete brew, $2 = paquete apt, $3 = paquete winget
  if [ "$OS" = "Darwin" ]; then
    command -v brew >/dev/null || return 2
    brew install "$1"
  elif command -v apt-get >/dev/null; then
    sudo -n true 2>/dev/null || return 3
    sudo apt-get install -y "$2"
  elif command -v winget >/dev/null; then
    winget install --silent -e --id "$3"
  else
    return 2
  fi
}

check_all(){
  MISSING=()
  echo "Herramientas para editar:"
  command -v ffmpeg >/dev/null && ok "ffmpeg" || miss "ffmpeg"
  command -v whisper-cli >/dev/null && ok "whisper-cli" || miss "whisper-cli"
  MODEL="${WHISPER_MODEL:-$(ls ~/.cache/hyperframes/whisper/models/*medium*.bin ~/.cache/whisper/*medium*.bin 2>/dev/null | head -1)}"
  [ -n "$MODEL" ] && ok "modelo de whisper" || miss "modelo-whisper"
  command -v node >/dev/null && ok "node $(node -v)" || miss "node"
  command -v python3 >/dev/null && ok "python3" || miss "python3"
  { [ -d "/Applications/Google Chrome.app" ] || command -v google-chrome >/dev/null || [ -f "/c/Program Files/Google/Chrome/Application/chrome.exe" ]; } \
    && ok "Google Chrome" || miss "chrome"
  if command -v node >/dev/null; then
    node -e "require('puppeteer-core')" 2>/dev/null || ls ~/.npm/_npx/*/node_modules/puppeteer-core >/dev/null 2>&1 \
      || [ -d "$(npm root -g 2>/dev/null)/puppeteer-core" ] && ok "puppeteer-core (capturas de webs)" || miss "puppeteer-core"
    npx --yes hyperframes --version >/dev/null 2>&1 && ok "HyperFrames" || miss "hyperframes"
  fi
  [ "$OS" = "Darwin" ] && { command -v avconvert >/dev/null && ok "avconvert (videos HDR de iPhone)"; }
}

check_all
[ ${#MISSING[@]} -eq 0 ] && { echo "Todo listo."; exit 0; }
[ $INSTALL -eq 0 ] && { echo "FALTAN: ${MISSING[*]}"; echo "Para instalarlo solo: bash $0 --install"; exit 1; }

echo; echo "Instalando lo que falta…"
for m in "${MISSING[@]}"; do
  case "$m" in
    ffmpeg)      pkg_install ffmpeg ffmpeg Gyan.FFmpeg ;;
    whisper-cli) pkg_install whisper-cpp whisper-cpp ggerganov.whisper.cpp ;;
    node)        pkg_install node nodejs OpenJS.NodeJS.LTS ;;
    python3)     pkg_install python python3 Python.Python.3.12 ;;
    chrome)      if [ "$OS" = "Darwin" ] && command -v brew >/dev/null; then brew install --cask google-chrome
                 elif command -v winget >/dev/null; then winget install --silent -e --id Google.Chrome
                 else false; fi ;;
    modelo-whisper) mkdir -p ~/.cache/whisper && echo "  bajando el modelo de whisper (≈1,5 GB, tarda unos minutos)…" \
                 && curl -L --fail -o ~/.cache/whisper/ggml-medium.bin \
                    https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.bin ;;
    puppeteer-core) npm install -g puppeteer-core ;;
    hyperframes) npx --yes hyperframes --version ;;
  esac
  r=$?
  if [ $r -eq 0 ]; then echo "  ✅ $m instalado"
  elif [ $r -eq 2 ]; then MANUAL+=("homebrew")
  elif [ $r -eq 3 ]; then MANUAL+=("sudo:$m")
  else MANUAL+=("$m"); fi
done

echo; check_all
if [ ${#MANUAL[@]} -gt 0 ]; then
  echo
  echo "NECESITA_A_LA_PERSONA:"
  printf '%s\n' "${MANUAL[@]}" | sort -u | while read -r x; do
    case "$x" in
      homebrew) echo "  • Homebrew (pide la contraseña de la compu). Abrir la app Terminal, pegar esto y apretar Enter:"
                echo '      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
                echo "    Cuando termine, avisar a Claude para que siga instalando." ;;
      sudo:*)   echo "  • ${x#sudo:}: pegar en la Terminal  sudo apt-get install -y ${x#sudo:}  (pide la contraseña)" ;;
      chrome)   echo "  • Google Chrome: bajarlo de https://www.google.com/chrome e instalarlo" ;;
      *)        echo "  • $x: no se pudo instalar solo; Claude te explica cómo" ;;
    esac
  done
  exit 1
fi
echo "Todo listo."
