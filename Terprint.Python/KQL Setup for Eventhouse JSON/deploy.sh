
#!/usr/bin/env bash
set -euo pipefail

# Env vars expected:
#   CLUSTER_URI   e.g., https://<cluster>.<region>.kusto.windows.net
#   DATABASE      e.g., YourDatabase
#   KQL_FILE      default: Trulieve_Fabric_Setup.kql

: "${CLUSTER_URI:?CLUSTER_URI is required}"
: "${DATABASE:?DATABASE is required}"
KQL_FILE=${KQL_FILE:-Trulieve_Fabric_Setup.kql}

if [ ! -f "$KQL_FILE" ]; then
  echo "KQL file not found: $KQL_FILE" >&2
  exit 1
fi

echo "Getting AAD token via Azure CLI..."
TOKEN=$(az account get-access-token --resource https://kusto.kusto.windows.net --query accessToken -o tsv)

MGMT="$CLUSTER_URI/v1/rest/mgmt"

# Escape newlines for JSON payload safely
CSL=$(python - <<'PY'
import json,sys
csl=open(sys.argv[1],'r',encoding='utf-8').read()
print(json.dumps(csl))
PY
"$KQL_FILE")

PAYLOAD=$(cat <<JSON
{"db":"$DATABASE","csl":$CSL,"properties":{"Options":{"results":"true"}}}
JSON
)

echo "Posting script to $MGMT (database: $DATABASE)"
curl -sS -X POST "$MGMT" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD"

echo "Deployment complete."
