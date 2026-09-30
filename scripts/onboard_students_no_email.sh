#!/usr/bin/env bash
#
# Onboard students WITHOUT sending any email (SES-sandbox workaround).
#
# For each student this script:
#   1. Creates a Cognito user with MessageAction=SUPPRESS (no invite email),
#      email_verified=true, and the same attributes the app's admin panel sets
#      (given_name, family_name, custom:cohort, custom:enrollment_date).
#   2. Sets a temporary password (valid per the pool policy: >=10 chars, upper,
#      lower, number, symbol; expires in TemporaryPasswordValidityDays).
#   3. Adds the user to the "students" group.
#
# The student then logs in with the temp password and is forced to choose a new
# one on first login (UserStatus FORCE_CHANGE_PASSWORD). You distribute the
# credentials OUT OF BAND (LMS, printout, in person) — nothing is emailed.
#
# It prints a credentials table at the end for you to hand out. Treat that
# output as sensitive.
#
# Usage:
#   ./scripts/onboard_students_no_email.sh students.csv
#
# CSV format (header required), one student per line:
#   email,first_name,last_name,cohort
#   ada@example.com,Ada,Lovelace,cohort-2026-q3
#   alan@example.com,Alan,Turing,cohort-2026-q3
#
# Prereqs:
#   - AWS CLI configured; set AWS_PROFILE / AWS_REGION or edit the vars below.
#   - Run from the repo root.

set -euo pipefail

# ── Config ────────────────────────────────────────────────────────────────────
USER_POOL_ID="${USER_POOL_ID:-eu-west-2_DGuDgCBPY}"
REGION="${AWS_REGION:-eu-west-2}"
PROFILE_ARG=""
[ -n "${AWS_PROFILE:-}" ] && PROFILE_ARG="--profile ${AWS_PROFILE}"

CSV="${1:-}"
if [ -z "$CSV" ] || [ ! -f "$CSV" ]; then
  echo "Usage: $0 students.csv" >&2
  echo "CSV header: email,first_name,last_name,cohort" >&2
  exit 1
fi

ENROLLMENT_DATE="$(date -u +%Y-%m-%d)"

# Generate a policy-valid temporary password:
# 12 random alphanumerics + guaranteed upper/lower/digit/symbol.
gen_password() {
  local base
  base="$(LC_ALL=C tr -dc 'A-Za-z0-9' </dev/urandom | head -c 12)"
  # Append one of each required class to guarantee policy compliance.
  echo "${base}Aa1@"
}

results=()
echo "Onboarding students from ${CSV} into pool ${USER_POOL_ID} (region ${REGION})..."
echo

# Skip the header line, iterate the rest.
tail -n +2 "$CSV" | while IFS=',' read -r email first last cohort; do
  # Trim whitespace/CR.
  email="$(echo "$email" | tr -d '\r' | xargs)"
  first="$(echo "$first" | xargs)"
  last="$(echo "$last" | xargs)"
  cohort="$(echo "$cohort" | tr -d '\r' | xargs)"
  [ -z "$email" ] && continue

  tmp_pw="$(gen_password)"

  # 1. Create the user with NO email (SUPPRESS) + verified email + attributes.
  if aws cognito-idp admin-create-user \
      --user-pool-id "$USER_POOL_ID" --region "$REGION" $PROFILE_ARG \
      --username "$email" \
      --message-action SUPPRESS \
      --temporary-password "$tmp_pw" \
      --user-attributes \
          Name=email,Value="$email" \
          Name=email_verified,Value=true \
          Name=given_name,Value="$first" \
          Name=family_name,Value="$last" \
          Name=custom:cohort,Value="$cohort" \
          Name=custom:enrollment_date,Value="$ENROLLMENT_DATE" \
      >/dev/null 2>/tmp/onboard_err; then

    # 2. Add to the students group.
    aws cognito-idp admin-add-user-to-group \
      --user-pool-id "$USER_POOL_ID" --region "$REGION" $PROFILE_ARG \
      --username "$email" --group-name students >/dev/null

    echo "OK   $email  |  temp password: $tmp_pw"
  else
    err="$(cat /tmp/onboard_err)"
    if echo "$err" | grep -q "UsernameExistsException"; then
      echo "SKIP $email  |  already exists"
    else
      echo "FAIL $email  |  $err"
    fi
  fi
done

echo
echo "Done. Distribute each temp password to its student OUT OF BAND."
echo "Students set a permanent password on first login. Temp passwords expire in"
echo "the pool's TemporaryPasswordValidityDays (currently 7 days)."
