#!/bin/bash
set -e

export SECRET_ARN=$M2M_SECRET_ARN
if [ "$IS_DEV" = "true" ]; then
    aws codeartifact login --tool pip --domain quantum_lab-cadmium --repository Pypi-SoftQuantus-Non-Prod
fi

aws secretsmanager get-secret-value --secret-id "$SECRET_ARN" | \
jq '{"quantum_labTokenAccount": .SecretString | fromjson | .access_token }' > "${HOME}/.quantum_lab-credentials"
