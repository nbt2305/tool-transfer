#!/bin/bash

### Define color variables (optional for Windows, vẫn giữ để đẹp)
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

# Sửa tên folder không có dấu cách để tránh lỗi trên Windows
PRE_CSV_RAW="1_CSV-Scraping/"
PRE_CSV_FORMATTED="2_CSV-Transfer/"
PRE_TXT_FINAL="3_TXT-Final/"

### Input env
# Prompt for INPUT if not set
if [[ -z "$INPUT" ]]; then
    read -rp "📥 Input INPUT file name (e.g., data.csv): " INPUT
fi

# Prompt for OUTPUT if not set
if [[ -z "$OUTPUT" ]]; then
    read -rp "📤 Input OUTPUT file name (e.g., result.txt): " OUTPUT
fi

# Check env
if [[ -z "$INPUT" || -z "$OUTPUT" ]]; then
    echo -e "${RED}${BOLD}❌ Error: Please set both INPUT and OUTPUT file names.${RESET}"
    exit 1
fi

# Không dùng realpath, xử lý thủ công
CSV_RAW_REL="$PRE_CSV_RAW$INPUT"
CSV_FORMATTED_REL="$PRE_CSV_FORMATTED$INPUT"
TXT_FINAL_REL="$PRE_TXT_FINAL$OUTPUT"

echo -e "${BG_MAGENTA}${BOLD}🚀 Starting Execution${RESET}"
echo -e "${CYAN}CSV RAW       : $CSV_RAW_REL${RESET}"
echo -e "${CYAN}CSV FORMATTED : $CSV_FORMATTED_REL${RESET}"
echo -e "${CYAN}TXT FINAL     : $TXT_FINAL_REL${RESET}"

# Get current absolute path (Windows-compatible)
CURRENT_DIR="$(pwd)"

# Transfer CSV raw → CSV formatted
docker run --rm \
  -v "$CURRENT_DIR:/app" \
  trung2305/transfer_to_csv \
  "/app/$CSV_RAW_REL" "/app/$CSV_FORMATTED_REL"

# Transfer CSV formatted → TXT final
docker run --rm \
  -v "$CURRENT_DIR:/app" \
  trung2305/transfer_to_txt \
  "/app/$CSV_FORMATTED_REL" "/app/$TXT_FINAL_REL"
