#!/bin/bash

### Define color variables
BLACK=$(tput setaf 0)
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
BLUE=$(tput setaf 4)
MAGENTA=$(tput setaf 5)
CYAN=$(tput setaf 6)
WHITE=$(tput setaf 7)

BG_BLACK=$(tput setab 0)
BG_RED=$(tput setab 1)
BG_GREEN=$(tput setab 2)
BG_YELLOW=$(tput setab 3)
BG_BLUE=$(tput setab 4)
BG_MAGENTA=$(tput setab 5)
BG_CYAN=$(tput setab 6)
BG_WHITE=$(tput setab 7)

BOLD=$(tput bold)
RESET=$(tput sgr0)

PRE_CSV_RAW="1. CSV-Scraping/"
PRE_CSV_FORMATTED="2. CSV-Transfer/"
PRE_TXT_FINAL="3. TXT-Final/"

### Input env
# Prompt for INPUT if not set
if [[ -z "$INPUT" ]]; then
    read -rp "Input INPUT path (CSV): " INPUT
fi

# Prompt for OUTPUT if not set
if [[ -z "$OUTPUT" ]]; then
    read -rp "Input OUTPUT path (TXT): " OUTPUT
fi

# Check env
if [[ -z "$INPUT" || -z "$OUTPUT" ]]; then
    echo -e "${RED}${BOLD}❌ Error: Please set both INPUT and OUTPUT paths.${RESET}"
    exit 1
fi

# Resolve absolute paths
CSV_RAW_ABS=$(realpath "$PRE_CSV_RAW$INPUT")
CSV_FORMATTED_ABS=$(realpath "$PRE_CSV_FORMATTED$INPUT")
TXT_FINAL_ABS=$(realpath "$PRE_TXT_FINAL$OUTPUT")

# Extract folder paths and filenames
WORKDIR=$(dirname "$CSV_RAW_ABS")
CSV_RAW_FILE=$(basename "$CSV_RAW_ABS")
CSV_FORMATTED_FILE=$(basename "$CSV_FORMATTED_ABS")
TXT_FINAL_FILE=$(basename "$TXT_FINAL_ABS")

echo -e "${BG_MAGENTA}${BOLD}🚀 Starting Execution${RESET}"
echo -e "${CYAN}CSV RAW : $CSV_RAW_ABS${RESET}"
echo -e "${CYAN}CSV FORMATTED : $CSV_FORMATTED_ABS${RESET}"
echo -e "${CYAN}TXT FINAL : $TXT_FINAL_ABS${RESET}"


# Transfer csv raw to csv formatted
docker run --rm \
  -v "$(pwd)":/app \
  trung2305/transfer_to_csv \
  "/app/$PRE_CSV_RAW$INPUT" "/app/$PRE_CSV_FORMATTED$INPUT"

# Transfer csv formatted to txt final
docker run --rm \
  -v "$(pwd)":/app \
  trung2305/transfer_to_txt \
  "/app/$PRE_CSV_FORMATTED$INPUT" "/app/$PRE_TXT_FINAL$OUTPUT"