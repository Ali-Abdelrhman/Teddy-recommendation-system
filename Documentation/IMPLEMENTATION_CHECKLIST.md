# Teddy Demo 2025 - Implementation Checklist

## 🎯 Pre-Implementation Checklist
- [x] **GCP Project Created**: `teddy-demo-2025` ✅
- [x] **Service Account Created**: `teddy-recommendation-service@teddy-demo-2025.iam.gserviceaccount.com` ✅
- [x] **Fake Data Generated**: 300 products, 32,000 events ✅
- [x] **NDJSON Files Ready**: `gcp_retail_products.ndjson`, `gcp_retail_events.ndjson` ✅

## 🚀 Implementation Steps

### Phase 1: Environment Setup (10 minutes)
- [ ] **Install gcloud CLI** (if not installed)
  ```bash
  # Download from: https://cloud.google.com/sdk/docs/install
  ```

- [ ] **Authenticate with GCP**
  ```bash
  gcloud auth login
  gcloud config set project teddy-demo-2025
  ```

- [ ] **Verify current directory**
  ```bash
  # Ensure you're in: GCP_Import_Ready folder
  ls -la *.ndjson  # Should show both files
  ```

### Phase 2: API and Storage Setup (15 minutes)
- [ ] **Enable Required APIs**
  ```bash
  gcloud services enable retail.googleapis.com
  gcloud services enable storage.googleapis.com
  ```

- [ ] **Create Service Account Key**
  ```bash
  gcloud iam service-accounts keys create teddy-retail-api-key.json \
      --iam-account=teddy-recommendation-service@teddy-demo-2025.iam.gserviceaccount.com
  ```

- [ ] **Set Authentication**
  ```bash
  export GOOGLE_APPLICATION_CREDENTIALS="teddy-retail-api-key.json"
  ```

- [ ] **Create Cloud Storage Bucket**
  ```bash
  gsutil mb gs://teddy-demo-2025-retail-data
  ```

### Phase 3: Data Upload (10 minutes)
- [ ] **Upload Product Catalog**
  ```bash
  gsutil cp gcp_retail_products.ndjson gs://teddy-demo-2025-retail-data/
  ```

- [ ] **Upload User Events**
  ```bash
  gsutil cp gcp_retail_events.ndjson gs://teddy-demo-2025-retail-data/
  ```

- [ ] **Verify Upload**
  ```bash
  gsutil ls -l gs://teddy-demo-2025-retail-data/
  ```

### Phase 4: Import Products (20 minutes)
- [ ] **Start Product Import**
  ```bash
  curl -X POST \
    "https://retail.googleapis.com/v2/projects/teddy-demo-2025/locations/global/catalogs/default_catalog/branches/default_branch/products:import" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d '{
      "inputConfig": {
        "gcsSource": {
          "inputUris": ["gs://teddy-demo-2025-retail-data/gcp_retail_products.ndjson"],
          "dataSchema": "product"
        }
      }
    }'
  ```

- [ ] **Monitor Import Progress**
  - Check GCP Console: Retail > Catalogs > default_catalog
  - Wait for import to complete (5-15 minutes)

- [ ] **Verify Products Imported**
  ```bash
  curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    "https://retail.googleapis.com/v2/projects/teddy-demo-2025/locations/global/catalogs/default_catalog/branches/default_branch/products" \
    | jq '.products | length'
  ```

### Phase 5: Import Events (30 minutes)
- [ ] **Start Events Import**
  ```bash
  curl -X POST \
    "https://retail.googleapis.com/v2/projects/teddy-demo-2025/locations/global/catalogs/default_catalog/userEvents:import" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d '{
      "inputConfig": {
        "gcsSource": {
          "inputUris": ["gs://teddy-demo-2025-retail-data/gcp_retail_events.ndjson"],
          "dataSchema": "user_event"
        }
      }
    }'
  ```

- [ ] **Monitor Import Progress**
  - Check GCP Console: Retail > Events
  - Wait for import to complete (10-30 minutes)

- [ ] **Verify Events Imported**
  ```bash
  curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    "https://retail.googleapis.com/v2/projects/teddy-demo-2025/locations/global/catalogs/default_catalog/userEvents:list?pageSize=5"
  ```

### Phase 6: Create Model (10 minutes)
- [ ] **Create Recommendation Model**
  ```bash
  curl -X POST \
    "https://retail.googleapis.com/v2/projects/teddy-demo-2025/locations/global/catalogs/default_catalog/models" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d '{
      "displayName": "Recommended for You",
      "type": "recommended-for-you",
      "optimizationObjective": "CLICK_THROUGH_RATE",
      "periodicTuningState": "PERIODIC_TUNING_ENABLED"
    }'
  ```

- [ ] **Verify Model Created**
  ```bash
  curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    "https://retail.googleapis.com/v2/projects/teddy-demo-2025/locations/global/catalogs/default_catalog/models"
  ```

### Phase 7: Model Training (24-48 hours)
- [ ] **Monitor Training Status**
  - Check GCP Console: Retail > Models
  - Status should change from "TRAINING" to "ACTIVE"

- [ ] **Wait for Training Completion**
  - Initial training: 24-48 hours
  - Check periodically for status updates

### Phase 8: Test Recommendations (After Training)
- [ ] **Test Basic Recommendations**
  ```bash
  curl -X POST \
    "https://retail.googleapis.com/v2/projects/teddy-demo-2025/locations/global/catalogs/default_catalog/placements/recommended_for_you_default:predict" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d '{
      "userEvent": {
        "eventType": "detail-page-view",
        "visitorId": "test-user-123"
      },
      "pageSize": 5
    }'
  ```

- [ ] **Test with Real User IDs**
  ```bash
  # Use visitor IDs from your fake data: b060a1c35fa679e1, a01f7e09fda27cf7, etc.
  curl -X POST \
    "https://retail.googleapis.com/v2/projects/teddy-demo-2025/locations/global/catalogs/default_catalog/placements/recommended_for_you_default:predict" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d '{
      "userEvent": {
        "eventType": "detail-page-view",
        "visitorId": "b060a1c35fa679e1",
        "productDetails": {
          "product": {"id": "product_25"}
        }
      },
      "pageSize": 10
    }'
  ```

## 🎯 Success Criteria
- [ ] **Products Imported**: 300 products visible in GCP Console
- [ ] **Events Imported**: 32,000 events visible in GCP Console  
- [ ] **Model Created**: "Recommended for You" model exists
- [ ] **Model Training**: Status shows "ACTIVE" after 24-48 hours
- [ ] **API Response**: Recommendations API returns product suggestions

## 🚨 Troubleshooting
- **Import Fails**: Check service account permissions and file format
- **Model Won't Train**: Verify minimum data requirements are met
- **API Errors**: Check authentication and project ID
- **No Recommendations**: Wait for training completion (up to 48 hours)

## 📞 Support Resources
- **GCP Console**: https://console.cloud.google.com/retail
- **Retail API Docs**: https://cloud.google.com/retail/docs
- **Service Account**: teddy-recommendation-service@teddy-demo-2025.iam.gserviceaccount.com

---

## 🏃‍♂️ Quick Start Option
**Run the automated script:**
```bash
# PowerShell (Windows)
.\implement_teddy_setup.ps1

# Bash (Linux/Mac)
./implement_teddy_setup.sh
```

This will execute all steps automatically with prompts for verification.