---
name: azure-sandbox
description: Manage Perry's Azure sandbox environment - storage, AI services, functions, containers, and cost monitoring. $1,000 credits available.
version: 1.0.0
author: Perry
---

# Azure Sandbox Skill

You are an Azure cloud specialist helping Perry manage his Azure sandbox environment with $1,000 in credits.

## Perry's Azure Account

| Property | Value |
|----------|-------|
| **Account** | perry.bailes@outlook.com |
| **Subscription** | Azure subscription 1 |
| **Subscription ID** | d06a2dde-1115-4513-81ca-d3848d63ec76 |
| **Tenant ID** | 12dd56f3-2181-43ca-8015-163162d36a55 |
| **Resource Group** | perry-sandbox |
| **Region** | eastus |
| **Credits** | $1,000 |

## Current Resources

| Resource | Type | Tier | Free Limits |
|----------|------|------|-------------|
| perrysandboxstorage | Blob Storage | Standard LRS | 5GB |
| perry-speech | AI Speech | F0 (Free) | 5 hrs STT, 500K chars TTS/month |

## Azure CLI Reference

**Path**: `C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd`

### Account & Subscription

```bash
# Login (opens browser)
az login

# Show current account
az account show

# List subscriptions
az account list -o table
```

### Resource Management

```bash
# List all resources in sandbox
az resource list --resource-group perry-sandbox -o table

# Create resource group (if needed)
az group create --name <name> --location eastus
```

### Cost Monitoring

```bash
# Check current month costs
az costmanagement query \
  --type ActualCost \
  --scope "subscriptions/d06a2dde-1115-4513-81ca-d3848d63ec76" \
  --timeframe MonthToDate \
  -o json

# Set budget alert
az consumption budget create \
  --budget-name "sandbox-budget" \
  --amount 100 \
  --category cost \
  --time-grain monthly \
  --start-date $(date +%Y-%m-01) \
  --resource-group perry-sandbox
```

## Blob Storage Operations

**Account**: perrysandboxstorage
**URL**: https://perrysandboxstorage.blob.core.windows.net/

```bash
# Create container
az storage container create \
  --account-name perrysandboxstorage \
  --name <container-name> \
  --auth-mode login

# List containers
az storage container list \
  --account-name perrysandboxstorage \
  --auth-mode login \
  -o table

# Upload file
az storage blob upload \
  --account-name perrysandboxstorage \
  --container-name <container> \
  --name <blob-name> \
  --file <local-path> \
  --auth-mode login

# Download file
az storage blob download \
  --account-name perrysandboxstorage \
  --container-name <container> \
  --name <blob-name> \
  --file <local-path> \
  --auth-mode login

# List blobs
az storage blob list \
  --account-name perrysandboxstorage \
  --container-name <container> \
  --auth-mode login \
  -o table
```

## Azure AI Speech Service

**Name**: perry-speech
**Region**: eastus
**Endpoint**: https://eastus.api.cognitive.microsoft.com/
**STT Endpoint**: https://eastus.stt.speech.microsoft.com
**TTS Endpoint**: https://eastus.tts.speech.microsoft.com

### Get Keys

```bash
az cognitiveservices account keys list \
  --name perry-speech \
  --resource-group perry-sandbox \
  -o json
```

### Free Tier Limits (F0)

| Feature | Monthly Free |
|---------|--------------|
| Speech-to-Text | 5 hours |
| Text-to-Speech | 500,000 characters |
| Neural Voices | Included |
| Custom Voice | Not available |

### Voice Options (TTS)

British voices (for Evie):
- `en-GB-SoniaNeural` - Professional British female
- `en-GB-LibbyNeural` - Casual British female
- `en-GB-RyanNeural` - British male

### Python SDK Example

```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription="<key>",
    region="eastus"
)

# Text-to-Speech
speech_config.speech_synthesis_voice_name = "en-GB-SoniaNeural"
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
result = synthesizer.speak_text_async("Hello Perry").get()

# Speech-to-Text
audio_config = speechsdk.audio.AudioConfig(filename="audio.wav")
recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
result = recognizer.recognize_once()
print(result.text)
```

## Azure Functions (Serverless)

Free tier: 1 million executions/month

```bash
# Create function app (consumption plan = free)
az functionapp create \
  --resource-group perry-sandbox \
  --consumption-plan-location eastus \
  --runtime node \
  --functions-version 4 \
  --name <unique-name> \
  --storage-account perrysandboxstorage \
  --os-type Linux

# List function apps
az functionapp list --resource-group perry-sandbox -o table

# Deploy function
az functionapp deployment source config-zip \
  --resource-group perry-sandbox \
  --name <app-name> \
  --src <path-to-zip>
```

## Azure Container Apps (Serverless Containers)

Scales to zero = free when idle

```bash
# Create environment (one-time)
az containerapp env create \
  --name perry-sandbox-env \
  --resource-group perry-sandbox \
  --location eastus

# Deploy container (scale-to-zero)
az containerapp create \
  --name <app-name> \
  --resource-group perry-sandbox \
  --environment perry-sandbox-env \
  --image <image:tag> \
  --target-port 80 \
  --ingress external \
  --min-replicas 0 \
  --max-replicas 1

# List container apps
az containerapp list --resource-group perry-sandbox -o table
```

## Azure OpenAI (Requires Approval)

**Status**: Requires access request

1. Apply: https://aka.ms/oai/access (1-3 days approval)
2. Create resource:
   ```bash
   az cognitiveservices account create \
     --name perry-openai \
     --resource-group perry-sandbox \
     --kind OpenAI \
     --sku S0 \
     --location eastus
   ```
3. Deploy models in Azure Portal > Azure OpenAI Studio

**Available Models** (after approval):
- GPT-4, GPT-4o, GPT-4o-mini
- DALL-E 3
- Whisper
- Text Embedding models

**Pricing**: Pay-per-token (GPT-4o-mini ~$0.15/1M input tokens)

## MCP Server

**Location**: `C:\Users\Jakeb\mcp-servers\azure\`

Available tools via Claude Code:
- `azure_account_info` - Show subscription details
- `azure_list_resources` - List sandbox resources
- `azure_check_costs` - Monitor credit usage
- `azure_blob_list` / `azure_blob_upload` / `azure_blob_download`
- `azure_create_container` - Create storage containers
- `azure_function_create` - Create serverless functions
- `azure_speech_setup` - Set up Speech service
- `azure_speech_get_key` - Get Speech API credentials
- `azure_container_app_create` - Deploy containers
- `azure_raw_command` - Run any az CLI command

## Cost Optimization Tips

### Free Tier Maximization

| Service | Free Amount | Tips |
|---------|-------------|------|
| Functions | 1M exec/mo | Use for webhooks, automations |
| Blob Storage | 5GB | Store backups, assets |
| AI Speech | 5 hrs/mo | Batch transcriptions |
| Container Apps | Scale-to-zero | DR/failover for Support Forge |

### Avoid Accidental Spend

1. **Always use free SKUs** (F0, Consumption, scale-to-zero)
2. **Set budget alerts** at $50, $100, $250
3. **Delete unused resources** in portal
4. **Check costs weekly**: `az costmanagement query`

### Good Uses for $1,000

| Use Case | Est. Cost | Value |
|----------|-----------|-------|
| Evie voice upgrade (Speech) | Free tier | Better TTS quality |
| Support Forge DR (Container Apps) | ~$5-20/mo | Multi-cloud redundancy |
| AI document processing | ~$20-50/mo | Auto-process invoices |
| Azure OpenAI experiments | ~$10-50/mo | Compare with Anthropic |

## Comparison with AWS/GCP

| Feature | Azure | AWS | GCP |
|---------|-------|-----|-----|
| Serverless Containers | Container Apps | Fargate | Cloud Run |
| Functions | Azure Functions | Lambda | Cloud Functions |
| Object Storage | Blob Storage | S3 | Cloud Storage |
| AI Speech | AI Speech | Transcribe/Polly | Speech-to-Text |
| AI Models | Azure OpenAI | Bedrock | Vertex AI |

## Quick Commands

```bash
# Check what's deployed
az resource list --resource-group perry-sandbox -o table

# Check costs
az costmanagement query --type ActualCost --scope "subscriptions/d06a2dde-1115-4513-81ca-d3848d63ec76" --timeframe MonthToDate

# Speech service key
az cognitiveservices account keys list --name perry-speech --resource-group perry-sandbox -o json
```
