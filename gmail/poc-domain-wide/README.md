1. enable APIs in GCP console.
  - https://console.cloud.google.com/apis/api/sheets.googleapis.com/overview
1. add service account, download the key json.
1. add OAuth consent screen, choose internal.
1. get the clientID from the service account, add it into GWS admin console.
  - https://admin.google.com/ac/owl/domainwidedelegation
1. Install required libraries.
  - pip install -r requirements.txt
1. update global variables in code.