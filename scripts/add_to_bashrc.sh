#!/bin/bash
# Legg til ANTHROPIC_API_KEY i ~/.bashrc

echo ""
echo "=== Legg til API Key i ~/.bashrc ==="
echo ""

# Hent API key fra environment variable
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "[X] ANTHROPIC_API_KEY ikke funnet i denne sesjonen"
    echo ""
    echo "Sett den først med:"
    echo "  export ANTHROPIC_API_KEY=\"sk-ant-api03-DIN_KEY\""
    echo ""
    exit 1
fi

# Finn hjemmemappe
if [ -f "$HOME/.bashrc" ]; then
    BASHRC_FILE="$HOME/.bashrc"
elif [ -f "$HOME/.bash_profile" ]; then
    BASHRC_FILE="$HOME/.bash_profile"
else
    BASHRC_FILE="$HOME/.bashrc"
    echo "[*] Oppretter ~/.bashrc..."
fi

# Sjekk om key allerede er i filen
if grep -q "ANTHROPIC_API_KEY" "$BASHRC_FILE" 2>/dev/null; then
    echo "[!] ANTHROPIC_API_KEY finnes allerede i $BASHRC_FILE"
    echo ""
    read -p "Vil du oppdatere den? (y/N): " update
    if [ "$update" != "y" ] && [ "$update" != "Y" ]; then
        echo "Avbrutt."
        exit 0
    fi

    # Oppdater eksisterende
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s|export ANTHROPIC_API_KEY=.*|export ANTHROPIC_API_KEY=\"$ANTHROPIC_API_KEY\"|" "$BASHRC_FILE"
    else
        # Linux/Git Bash
        sed -i "s|export ANTHROPIC_API_KEY=.*|export ANTHROPIC_API_KEY=\"$ANTHROPIC_API_KEY\"|" "$BASHRC_FILE"
    fi

    echo "[OK] Oppdatert i $BASHRC_FILE"
else
    # Legg til ny
    echo "" >> "$BASHRC_FILE"
    echo "# Anthropic API Key (lagt til $(date +%Y-%m-%d))" >> "$BASHRC_FILE"
    echo "export ANTHROPIC_API_KEY=\"$ANTHROPIC_API_KEY\"" >> "$BASHRC_FILE"

    echo "[OK] Lagt til i $BASHRC_FILE"
fi

echo ""
echo "For å aktivere i denne sesjonen, kjør:"
echo "  source $BASHRC_FILE"
echo ""
echo "Eller restart bash-terminalen."

