#!/bin/bash
set -e

# Define colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

IP_ONLY=false
if [[ "$1" == "--iponly" ]]; then
    IP_ONLY=true
    echo -e "${BLUE}=== TPU IP Configuration Helper (IP Only Mode) ===${NC}\n"
else
    echo -e "${BLUE}=== TPU Cluster Interactive Initialization Tool ===${NC}\n"
fi

# 1. Pre-check SSH keys
if [ "$IP_ONLY" = false ]; then
echo -e "${RED}Pre-check:${NC}"
echo "Please confirm the following SSH keys have been created:"
echo "  1. ~/.ssh/id_rsa"
echo "  2. ~/.ssh/id_rsa_github (if you need to configure GitHub SSH key)"
echo ""
read -p "Press [Enter] to continue if ready, or any other key to exit: " check_key

# Exit if user inputs anything other than Enter
if [[ -n "$check_key" ]]; then
    echo -e "\n${RED}Initialization cancelled. Please run 'ssh-keygen' to create the required keys first.${NC}"
    exit 1
fi
fi

# 2. Input IP list
if [ "$IP_ONLY" = true ]; then
    echo -e "\n${GREEN}[1/2] Configure TPU Node IPs${NC}"
    echo "Paste IP addresses directly (supports multiple lines, spaces, commas, tabs)."
    echo -e "${YELLOW}After pasting, press [Enter] for a new line, then press [Ctrl+D] to finish:${NC}"
    raw_input=$(cat)
else
    echo -e "\n${GREEN}[1/4] Configure TPU Node IPs${NC}"
    echo "Default: Fetch IPs from Google Cloud metadata service."
    read -p "Fetch from metadata? [Y/n]: " use_metadata
    use_metadata=${use_metadata:-Y}

    if [[ "$use_metadata" =~ ^[Yy]$ ]]; then
        echo "Fetching IPs from metadata..."
        METADATA_URL="http://metadata.google.internal/computeMetadata/v1/instance/attributes/worker-network-endpoints"
        raw_input=$(curl -s -H "Metadata-Flavor: Google" "$METADATA_URL" 2>/dev/null) || raw_input=""
        if [ -z "$raw_input" ]; then
            echo -e "${YELLOW}Failed to fetch from metadata. Please enter manually.${NC}"
            echo "Paste IP addresses directly (supports multiple lines, spaces, commas, tabs)."
            echo -e "${YELLOW}After pasting, press [Enter] for a new line, then press [Ctrl+D] to finish:${NC}"
            raw_input=$(cat)
        else
            echo "Metadata fetched successfully."
        fi
    else
        echo "Paste IP addresses directly (supports multiple lines, spaces, commas, tabs)."
        echo -e "${YELLOW}After pasting, press [Enter] for a new line, then press [Ctrl+D] to finish:${NC}"
        raw_input=$(cat)
    fi
fi

TARGET_IP_FILE="$HOME/podips.txt"
if [ "$IP_ONLY" = true ]; then
    read -p "Enter filename to save IPs (default: podips -> ~/podips.txt): " ip_filename
    if [[ -n "$ip_filename" ]]; then
        TARGET_IP_FILE="$HOME/${ip_filename}.txt"
    fi
fi

# --- Core cleanup logic ---
# Logic: Extract all IPs -> Deduplicate -> Exclude local machine IPs
# <(hostname -I | xargs -n1) dynamically generates a virtual file with one local IP per line for grep
echo "$raw_input" | grep -oE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' \
                  | sort -u \
                  | grep -v -F -w -f <(hostname -I | xargs -n1) > "$TARGET_IP_FILE" || true
# ----------------------------------

IP_COUNT=$(wc -l < "$TARGET_IP_FILE")

if [ "$IP_COUNT" -eq 0 ]; then
    echo -e "${RED}No valid remote IP addresses found after excluding local IPs. Please check your input!${NC}"
    exit 1
fi

echo -e "\nIdentified $IP_COUNT remote node(s) (local addresses excluded), saved to $TARGET_IP_FILE"

# 3. Configure SSH warning handling
if [ "$IP_ONLY" = true ]; then
    echo -e "\n${GREEN}[2/2] Append SSH Warning Configuration${NC}"
else
    echo -e "\n${GREEN}[2/4] Configure SSH Warning Handling${NC}"
fi

# Auto-calculate: extract first 3 octets of IPs, deduplicate, append .*, merge into space-separated line
auto_pattern=$(cut -d. -f1-3 "$TARGET_IP_FILE" | sort -u | sed 's/$/.*/' | tr '\n' ' ' | sed 's/ $//')

if [ -z "$auto_pattern" ]; then
    auto_pattern="*"
    echo -e "${YELLOW}Could not identify subnet, using global wildcard [*]${NC}"
else
    echo -e "Auto-detected subnet pattern from IPs: ${YELLOW}$auto_pattern${NC}"
fi

read -p "Press [Enter] to confirm, or enter a custom pattern: " input_pattern
ip_pattern=${input_pattern:-$auto_pattern}

# Append config and exit in IP Only mode
if [ "$IP_ONLY" = true ]; then
    mkdir -p ~/.ssh
    cat >> ~/.ssh/config << INNER_EOF

Host $ip_pattern
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    LogLevel ERROR
INNER_EOF
    echo "SSH config appended to ~/.ssh/config"
    echo -e "${GREEN}Done! IP file: $TARGET_IP_FILE${NC}"
    exit 0
fi

# 4. GitHub configuration
echo -e "\n${GREEN}[3/4] Configure GitHub SSH (optional)${NC}"
read -p "Do you want to configure GitHub SSH key? (y/n): " setup_github

# Initialize/rewrite ~/.ssh/config
mkdir -p ~/.ssh
cat > ~/.ssh/config << INNER_EOF
Host $ip_pattern
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    LogLevel ERROR
INNER_EOF

GH_KEY_FILE=""
if [[ "$setup_github" =~ ^[Yy]$ ]]; then
    read -p "Enter GitHub SSH key filename in ~/.ssh/ (default: id_rsa_github): " gh_key_name
    gh_key_name=${gh_key_name:-id_rsa_github}
    GH_KEY_FILE="$gh_key_name"

    cat >> ~/.ssh/config << INNER_EOF

Host github.com
    HostName github.com
    IdentityFile ~/.ssh/$gh_key_name
INNER_EOF
    echo "GitHub config added to ~/.ssh/config"
fi

# 5. Install dependencies and tools
echo -e "\n${GREEN}[4/4] Install Dependencies and Download Tools${NC}"

# Set file permissions
chmod 600 ~/.ssh/config ~/.ssh/id_rsa 2>/dev/null || true
if [ -n "$GH_KEY_FILE" ]; then
    chmod 600 ~/.ssh/"$GH_KEY_FILE" 2>/dev/null || true
fi

# Install Fabric
echo "Installing fabric..."
pip3 install fabric --user --quiet

# Download tools (podsync, podrun, podloop)
USER_BIN="$HOME/.local/bin"
mkdir -p "$USER_BIN"

GIST_URL="https://gist.githubusercontent.com/hainuo-wang/73d31abb46dfc21fe6b0e03464dbaa52/raw"
echo "Downloading latest tool scripts from Gist..."
wget -q -O "$USER_BIN/podsync" ${GIST_URL}/podsync
wget -q -O "$USER_BIN/podrun" ${GIST_URL}/podrun
wget -q -O "$USER_BIN/podloop" ${GIST_URL}/podloop

# Set executable permissions
chmod +x "$USER_BIN/podsync" "$USER_BIN/podrun" "$USER_BIN/podloop"

# Check if PATH includes ~/.local/bin
if [[ ":$PATH:" != *":$USER_BIN:"* ]]; then
    echo -e "${YELLOW}Note: Please add ~/.local/bin to PATH, e.g., add to ~/.bashrc:${NC}"
    echo -e "  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo -e "\n${BLUE}=================================${NC}"
echo -e "${GREEN}Initialization complete!${NC}"
echo -e "Tools path: ~/.local/bin/ (podrun, podsync, podloop)"
echo -e "IP list: $(tr '\n' ' ' < ~/podips.txt)"
echo -e "${BLUE}=================================${NC}"