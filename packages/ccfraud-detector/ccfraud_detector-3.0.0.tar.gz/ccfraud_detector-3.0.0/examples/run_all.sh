#!/usr/bin/env bash
#═══════════════════════════════════════════════════════════════════════════════
# CCFraud Detector - Enterprise Test Suite Runner
# Authors: Ekta Bhatia (Lead Developer), Aditya Patange
# Version: 2.0.1
#═══════════════════════════════════════════════════════════════════════════════

# Don't use set -e as we want to continue running tests even if one fails

#───────────────────────────────────────────────────────────────────────────────
# ANSI Color Codes - Sci-Fi Theme
#───────────────────────────────────────────────────────────────────────────────
readonly RESET='\033[0m'
readonly BOLD='\033[1m'
readonly DIM='\033[2m'
readonly ITALIC='\033[3m'
readonly UNDERLINE='\033[4m'
readonly BLINK='\033[5m'
readonly REVERSE='\033[7m'

# Primary Colors
readonly BLACK='\033[30m'
readonly RED='\033[31m'
readonly GREEN='\033[32m'
readonly YELLOW='\033[33m'
readonly BLUE='\033[34m'
readonly MAGENTA='\033[35m'
readonly CYAN='\033[36m'
readonly WHITE='\033[37m'

# Bright Colors
readonly BRIGHT_BLACK='\033[90m'
readonly BRIGHT_RED='\033[91m'
readonly BRIGHT_GREEN='\033[92m'
readonly BRIGHT_YELLOW='\033[93m'
readonly BRIGHT_BLUE='\033[94m'
readonly BRIGHT_MAGENTA='\033[95m'
readonly BRIGHT_CYAN='\033[96m'
readonly BRIGHT_WHITE='\033[97m'

# Background Colors
readonly BG_BLACK='\033[40m'
readonly BG_RED='\033[41m'
readonly BG_GREEN='\033[42m'
readonly BG_BLUE='\033[44m'
readonly BG_MAGENTA='\033[45m'
readonly BG_CYAN='\033[46m'

# Sci-Fi Theme Colors
readonly NEON_CYAN='\033[38;5;51m'
readonly NEON_GREEN='\033[38;5;46m'
readonly NEON_PINK='\033[38;5;199m'
readonly NEON_PURPLE='\033[38;5;129m'
readonly NEON_ORANGE='\033[38;5;208m'
readonly NEON_YELLOW='\033[38;5;226m'
readonly MATRIX_GREEN='\033[38;5;40m'
readonly ELECTRIC_BLUE='\033[38;5;33m'
readonly TERMINAL_GREEN='\033[38;5;34m'
readonly HOLOGRAM_BLUE='\033[38;5;39m'
readonly PLASMA_PURPLE='\033[38;5;93m'
readonly LASER_RED='\033[38;5;196m'

#───────────────────────────────────────────────────────────────────────────────
# Configuration
#───────────────────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PASSED=0
FAILED=0
TOTAL=0
START_TIME=$(date +%s)

#───────────────────────────────────────────────────────────────────────────────
# Helper Functions
#───────────────────────────────────────────────────────────────────────────────

print_char_by_char() {
    local text="$1"
    local delay="${2:-0.002}"
    for (( i=0; i<${#text}; i++ )); do
        printf "%s" "${text:$i:1}"
        sleep "$delay"
    done
}

cyber_line() {
    local char="${1:-═}"
    local color="${2:-$NEON_CYAN}"
    local width="${3:-78}"
    echo -ne "${color}"
    printf '%*s' "$width" | tr ' ' "$char"
    echo -e "${RESET}"
}

matrix_rain() {
    local lines="${1:-3}"
    local chars="01アイウエオカキクケコサシスセソタチツテト"
    for ((i=0; i<lines; i++)); do
        echo -ne "${MATRIX_GREEN}${DIM}"
        for ((j=0; j<78; j++)); do
            echo -n "${chars:RANDOM%${#chars}:1}"
        done
        echo -e "${RESET}"
        sleep 0.02
    done
}

loading_bar() {
    local duration="${1:-2}"
    local width=50
    local fill_char="█"
    local empty_char="░"

    echo -ne "${NEON_CYAN}  ["
    for ((i=0; i<=width; i++)); do
        local percent=$((i * 100 / width))
        echo -ne "\r${NEON_CYAN}  [${NEON_GREEN}"
        for ((j=0; j<i; j++)); do echo -n "$fill_char"; done
        echo -ne "${BRIGHT_BLACK}"
        for ((j=i; j<width; j++)); do echo -n "$empty_char"; done
        echo -ne "${NEON_CYAN}] ${NEON_YELLOW}${percent}%%${RESET}"
        sleep $(echo "scale=4; $duration / $width" | bc)
    done
    echo ""
}

spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " ${NEON_CYAN}[%c]${RESET}" "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b"
    done
    printf "     \b\b\b\b\b"
}

print_header() {
    clear
    echo ""
    matrix_rain 2
    echo ""

    echo -e "${NEON_CYAN}${BOLD}"
    cat << 'EOF'
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║   ██████╗ ██████╗███████╗██████╗  █████╗ ██╗   ██╗██████╗                 ║
    ║  ██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗██║   ██║██╔══██╗                ║
    ║  ██║     ██║     █████╗  ██████╔╝███████║██║   ██║██║  ██║                ║
    ║  ██║     ██║     ██╔══╝  ██╔══██╗██╔══██║██║   ██║██║  ██║                ║
    ║  ╚██████╗╚██████╗██║     ██║  ██║██║  ██║╚██████╔╝██████╔╝                ║
    ║   ╚═════╝ ╚═════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝                 ║
    ║                                                                           ║
    ║        ██████╗ ███████╗████████╗███████╗ ██████╗████████╗ ██████╗ ██████╗ ║
    ║        ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗║
    ║        ██║  ██║█████╗     ██║   █████╗  ██║        ██║   ██║   ██║██████╔╝║
    ║        ██║  ██║██╔══╝     ██║   ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗║
    ║        ██████╔╝███████╗   ██║   ███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║║
    ║        ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${RESET}"

    echo ""
    echo -e "${HOLOGRAM_BLUE}${BOLD}    ┌─────────────────────────────────────────────────────────────────────┐${RESET}"
    echo -e "${HOLOGRAM_BLUE}${BOLD}    │${RESET}  ${NEON_PINK}◆${RESET} ${WHITE}ENTERPRISE FRAUD DETECTION TEST SUITE${RESET}                ${NEON_PINK}◆${RESET}  ${HOLOGRAM_BLUE}${BOLD}│${RESET}"
    echo -e "${HOLOGRAM_BLUE}${BOLD}    │${RESET}  ${DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}  ${HOLOGRAM_BLUE}${BOLD}│${RESET}"
    echo -e "${HOLOGRAM_BLUE}${BOLD}    │${RESET}  ${NEON_CYAN}►${RESET} Lead Developer: ${NEON_GREEN}Ekta Bhatia${RESET}                              ${HOLOGRAM_BLUE}${BOLD}│${RESET}"
    echo -e "${HOLOGRAM_BLUE}${BOLD}    │${RESET}  ${NEON_CYAN}►${RESET} Co-Developer:   ${NEON_GREEN}Aditya Patange${RESET}                           ${HOLOGRAM_BLUE}${BOLD}│${RESET}"
    echo -e "${HOLOGRAM_BLUE}${BOLD}    │${RESET}  ${NEON_CYAN}►${RESET} Version:        ${NEON_YELLOW}2.0.1${RESET}                                    ${HOLOGRAM_BLUE}${BOLD}│${RESET}"
    echo -e "${HOLOGRAM_BLUE}${BOLD}    │${RESET}  ${NEON_CYAN}►${RESET} Contact:        ${NEON_PURPLE}ekta.bhatia@gmail.com${RESET}                    ${HOLOGRAM_BLUE}${BOLD}│${RESET}"
    echo -e "${HOLOGRAM_BLUE}${BOLD}    └─────────────────────────────────────────────────────────────────────┘${RESET}"
    echo ""
}

print_system_init() {
    echo ""
    cyber_line "─" "$BRIGHT_BLACK" 78
    echo -e "${NEON_CYAN}${BOLD}  ◈ SYSTEM INITIALIZATION${RESET}"
    cyber_line "─" "$BRIGHT_BLACK" 78
    echo ""

    local init_messages=(
        "Initializing quantum fraud detection matrix..."
        "Loading neural network weights..."
        "Establishing secure Anthropic API connection..."
        "Calibrating AI classification algorithms..."
        "Activating real-time monitoring systems..."
        "System ready."
    )

    for msg in "${init_messages[@]}"; do
        echo -ne "  ${MATRIX_GREEN}▸${RESET} ${DIM}${msg}${RESET}"
        sleep 0.3
        echo -e " ${NEON_GREEN}✓${RESET}"
    done

    echo ""
    loading_bar 1
    echo ""
}

print_test_header() {
    local num="$1"
    local name="$2"
    local desc="$3"

    echo ""
    cyber_line "═" "$PLASMA_PURPLE" 78
    echo -e "${BOLD}${NEON_PINK}  ◉ TEST MODULE ${num}/12${RESET}"
    echo -e "${BOLD}${WHITE}    ${name}${RESET}"
    echo -e "${DIM}${BRIGHT_CYAN}    ${desc}${RESET}"
    cyber_line "─" "$BRIGHT_BLACK" 78
    echo ""
}

print_executing() {
    local script="$1"
    echo -e "  ${NEON_CYAN}⚡${RESET} ${DIM}Executing:${RESET} ${ELECTRIC_BLUE}${script}${RESET}"
    echo -e "  ${NEON_CYAN}◷${RESET} ${DIM}Timestamp:${RESET} ${BRIGHT_BLACK}$(date '+%Y-%m-%d %H:%M:%S.%3N')${RESET}"
    echo ""
}

print_output_start() {
    echo -e "  ${NEON_PURPLE}┌$( printf '─%.0s' {1..72} )┐${RESET}"
    echo -e "  ${NEON_PURPLE}│${RESET} ${BOLD}${WHITE}OUTPUT STREAM${RESET}                                                        ${NEON_PURPLE}│${RESET}"
    echo -e "  ${NEON_PURPLE}├$( printf '─%.0s' {1..72} )┤${RESET}"
}

print_output_end() {
    echo -e "  ${NEON_PURPLE}└$( printf '─%.0s' {1..72} )┘${RESET}"
}

print_success() {
    local duration="$1"
    echo ""
    echo -e "  ${BG_GREEN}${BLACK}${BOLD}  ✓ TEST PASSED  ${RESET}  ${NEON_GREEN}Duration: ${duration}s${RESET}"
    ((PASSED++))
}

print_failure() {
    local duration="$1"
    echo ""
    echo -e "  ${BG_RED}${WHITE}${BOLD}  ✗ TEST FAILED  ${RESET}  ${LASER_RED}Duration: ${duration}s${RESET}"
    ((FAILED++))
}

run_example() {
    local num="$1"
    local script="$2"
    local name="$3"
    local desc="$4"

    ((TOTAL++))

    print_test_header "$num" "$name" "$desc"
    print_executing "$script"
    print_output_start

    local test_start=$(date +%s)

    # Run the script and capture output
    output=$(python "$SCRIPT_DIR/$script" 2>&1)
    local exit_code=$?

    # Print output with indentation
    while IFS= read -r line; do
        echo -e "  ${NEON_PURPLE}│${RESET}  ${line}"
    done <<< "$output"

    print_output_end

    local test_end=$(date +%s)
    local duration=$((test_end - test_start))

    if [ $exit_code -eq 0 ]; then
        print_success "$duration"
    else
        print_failure "$duration"
    fi
}

print_summary() {
    local end_time=$(date +%s)
    local total_duration=$((end_time - START_TIME))
    local success_rate=0
    if [ $TOTAL -gt 0 ]; then
        success_rate=$((PASSED * 100 / TOTAL))
    fi

    echo ""
    echo ""
    matrix_rain 1
    echo ""

    cyber_line "═" "$NEON_CYAN" 78
    echo -e "${BOLD}${NEON_CYAN}"
    cat << 'EOF'
      ╔═══════════════════════════════════════════════════════════════════╗
      ║                    TEST EXECUTION COMPLETE                        ║
      ╚═══════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${RESET}"

    echo -e "${HOLOGRAM_BLUE}      ┌───────────────────────────────────────────────────────────────┐${RESET}"
    echo -e "${HOLOGRAM_BLUE}      │${RESET}                    ${BOLD}${WHITE}EXECUTION SUMMARY${RESET}                        ${HOLOGRAM_BLUE}│${RESET}"
    echo -e "${HOLOGRAM_BLUE}      ├───────────────────────────────────────────────────────────────┤${RESET}"
    echo -e "${HOLOGRAM_BLUE}      │${RESET}                                                               ${HOLOGRAM_BLUE}│${RESET}"
    echo -e "${HOLOGRAM_BLUE}      │${RESET}   ${NEON_CYAN}◆${RESET} Total Tests:      ${BOLD}${WHITE}${TOTAL}${RESET}                                      ${HOLOGRAM_BLUE}│${RESET}"
    echo -e "${HOLOGRAM_BLUE}      │${RESET}   ${NEON_GREEN}◆${RESET} Passed:           ${BOLD}${NEON_GREEN}${PASSED}${RESET}                                      ${HOLOGRAM_BLUE}│${RESET}"
    echo -e "${HOLOGRAM_BLUE}      │${RESET}   ${LASER_RED}◆${RESET} Failed:           ${BOLD}${LASER_RED}${FAILED}${RESET}                                      ${HOLOGRAM_BLUE}│${RESET}"
    echo -e "${HOLOGRAM_BLUE}      │${RESET}   ${NEON_YELLOW}◆${RESET} Success Rate:    ${BOLD}${NEON_YELLOW}${success_rate}%%${RESET}                                    ${HOLOGRAM_BLUE}│${RESET}"
    echo -e "${HOLOGRAM_BLUE}      │${RESET}   ${NEON_PURPLE}◆${RESET} Total Duration:  ${BOLD}${NEON_PURPLE}${total_duration}s${RESET}                                     ${HOLOGRAM_BLUE}│${RESET}"
    echo -e "${HOLOGRAM_BLUE}      │${RESET}                                                               ${HOLOGRAM_BLUE}│${RESET}"
    echo -e "${HOLOGRAM_BLUE}      └───────────────────────────────────────────────────────────────┘${RESET}"
    echo ""

    # Status indicator
    if [ $FAILED -eq 0 ]; then
        echo -e "${NEON_GREEN}${BOLD}"
        cat << 'EOF'
      ╔═══════════════════════════════════════════════════════════════════╗
      ║     █████╗ ██╗     ██╗         ████████╗███████╗███████╗████████╗ ║
      ║    ██╔══██╗██║     ██║         ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝ ║
      ║    ███████║██║     ██║            ██║   █████╗  ███████╗   ██║    ║
      ║    ██╔══██║██║     ██║            ██║   ██╔══╝  ╚════██║   ██║    ║
      ║    ██║  ██║███████╗███████╗       ██║   ███████╗███████║   ██║    ║
      ║    ╚═╝  ╚═╝╚══════╝╚══════╝       ╚═╝   ╚══════╝╚══════╝   ╚═╝    ║
      ║                                                                   ║
      ║    ██████╗  █████╗ ███████╗███████╗███████╗██████╗  ██╗██╗        ║
      ║    ██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗ ██║██║        ║
      ║    ██████╔╝███████║███████╗███████╗█████╗  ██║  ██║ ██║██║        ║
      ║    ██╔═══╝ ██╔══██║╚════██║╚════██║██╔══╝  ██║  ██║ ╚═╝╚═╝        ║
      ║    ██║     ██║  ██║███████║███████║███████╗██████╔╝ ██╗██╗        ║
      ║    ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═════╝  ╚═╝╚═╝        ║
      ╚═══════════════════════════════════════════════════════════════════╝
EOF
        echo -e "${RESET}"
    else
        echo -e "${LASER_RED}${BOLD}"
        cat << 'EOF'
      ╔═══════════════════════════════════════════════════════════════════╗
      ║           ███████╗ ██████╗ ███╗   ███╗███████╗                    ║
      ║           ██╔════╝██╔═══██╗████╗ ████║██╔════╝                    ║
      ║           ███████╗██║   ██║██╔████╔██║█████╗                      ║
      ║           ╚════██║██║   ██║██║╚██╔╝██║██╔══╝                      ║
      ║           ███████║╚██████╔╝██║ ╚═╝ ██║███████╗                    ║
      ║           ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝                    ║
      ║                                                                   ║
      ║          ████████╗███████╗███████╗████████╗███████╗               ║
      ║          ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔════╝               ║
      ║             ██║   █████╗  ███████╗   ██║   ███████╗               ║
      ║             ██║   ██╔══╝  ╚════██║   ██║   ╚════██║               ║
      ║             ██║   ███████╗███████║   ██║   ███████║               ║
      ║             ╚═╝   ╚══════╝╚══════╝   ╚═╝   ╚══════╝               ║
      ║                                                                   ║
      ║           ███████╗ █████╗ ██╗██╗     ███████╗██████╗              ║
      ║           ██╔════╝██╔══██╗██║██║     ██╔════╝██╔══██╗             ║
      ║           █████╗  ███████║██║██║     █████╗  ██║  ██║             ║
      ║           ██╔══╝  ██╔══██║██║██║     ██╔══╝  ██║  ██║             ║
      ║           ██║     ██║  ██║██║███████╗███████╗██████╔╝             ║
      ║           ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝              ║
      ╚═══════════════════════════════════════════════════════════════════╝
EOF
        echo -e "${RESET}"
    fi

    echo ""
    cyber_line "─" "$BRIGHT_BLACK" 78
    echo -e "  ${DIM}Execution completed at $(date '+%Y-%m-%d %H:%M:%S')${RESET}"
    echo -e "  ${DIM}CCFraud Detector v2.0.1 | Ekta Bhatia (Lead Developer), Aditya Patange${RESET}"
    cyber_line "─" "$BRIGHT_BLACK" 78
    echo ""

    matrix_rain 2
    echo ""

    return $FAILED
}

#───────────────────────────────────────────────────────────────────────────────
# Main Execution
#───────────────────────────────────────────────────────────────────────────────

main() {
    print_header
    print_system_init

    echo ""
    cyber_line "═" "$NEON_PINK" 78
    echo -e "${BOLD}${NEON_PINK}  ◈ COMMENCING TEST SEQUENCE${RESET}"
    cyber_line "═" "$NEON_PINK" 78

    # Run all 12 examples
    run_example "01" "01_basic_transaction.py" \
        "BASIC TRANSACTION ANALYSIS" \
        "Analyzing standard credit card transactions for fraud indicators."

    run_example "02" "02_suspicious_transaction.py" \
        "SUSPICIOUS TRANSACTION DETECTION" \
        "Detecting high-risk transactions with multiple red flags."

    run_example "03" "03_card_validation.py" \
        "CARD NUMBER VALIDATION" \
        "Validating card numbers using Luhn algorithm and AI analysis."

    run_example "04" "04_cvv_validation.py" \
        "CVV PATTERN VALIDATION" \
        "Analyzing CVV codes for suspicious patterns and anomalies."

    run_example "05" "05_field_signals.py" \
        "FORM FIELD SIGNAL ANALYSIS" \
        "Detecting bot submissions and suspicious form data patterns."

    run_example "06" "06_scam_detection.py" \
        "SCAM DETECTION SUITE" \
        "Identifying phishing, investment fraud, and advance fee scams."

    run_example "07" "07_batch_analysis.py" \
        "BATCH TRANSACTION PROCESSING" \
        "Processing multiple transactions in batch mode with summary report."

    run_example "08" "08_full_analysis.py" \
        "COMPREHENSIVE FULL ANALYSIS" \
        "Multi-factor fraud analysis using all available detection methods."

    run_example "09" "09_realtime_monitoring.py" \
        "REAL-TIME MONITORING SIMULATION" \
        "Simulating real-time transaction monitoring and alerting."

    run_example "10" "10_geographic_analysis.py" \
        "GEOGRAPHIC IMPOSSIBILITY DETECTION" \
        "Detecting physically impossible transaction patterns."

    run_example "11" "11_image_analysis.py" \
        "CARD & IDENTITY IMAGE ANALYSIS" \
        "Analyzing card images and identity photos for fraud indicators."

    run_example "12" "12_enterprise_integration.py" \
        "ENTERPRISE INTEGRATION PATTERNS" \
        "Demonstrating enterprise-grade fraud detection integration."

    print_summary
}

# Run main function
main "$@"
