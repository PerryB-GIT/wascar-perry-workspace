# MCP Server Setup for Claude Skills

**Model Context Protocol (MCP) Servers extend Claude Code with custom tools and integrations.**

---

## 📦 Included MCP Server Templates

### 1. **Custom Business MCP Template**
Create your own business-specific MCP servers.

**Location:** `mcp-templates/business-mcp/`

**Features:**
- Client data access
- Invoice generation
- Financial reporting
- Calendar integration

### 2. **Automation MCP Template**
Workflow automation server.

**Location:** `mcp-templates/automation-mcp/`

**Features:**
- Task scheduling
- Email automation
- File processing
- API integrations

### 3. **Database MCP Template**
Database access server.

**Location:** `mcp-templates/database-mcp/`

**Features:**
- SQL query execution
- Data exports
- Report generation
- Backup management

---

## 🚀 Quick Start

### Install MCP SDK
```bash
npm install -g @anthropic-ai/mcp-server-sdk
```

### Create Your First MCP Server
```bash
cd ~/workspace
mkdir my-business-mcp
cd my-business-mcp
npm init -y
npm install @anthropic-ai/mcp-server-sdk
```

### Basic MCP Server Structure
```javascript
// index.js
const { MCPServer } = require('@anthropic-ai/mcp-server-sdk');

const server = new MCPServer({
  name: 'my-business-mcp',
  version: '1.0.0'
});

// Define a tool
server.tool({
  name: 'get_client_info',
  description: 'Get client information',
  parameters: {
    client_id: {
      type: 'string',
      description: 'Client ID',
      required: true
    }
  },
  handler: async ({ client_id }) => {
    // Your business logic here
    return {
      client_id,
      name: 'Example Client',
      status: 'active'
    };
  }
});

server.start();
```

### Add to Claude Code Config
```bash
# Edit ~/.claude/config.json
{
  "mcpServers": {
    "my-business-mcp": {
      "command": "node",
      "args": ["/path/to/my-business-mcp/index.js"]
    }
  }
}
```

---

## 📚 Perry's Custom MCP Servers

These are already configured on Perry's system. You can replicate for your use:

### **Gmail MCP**
**Location:** `~/mcp-servers/gmail/`

**Tools:**
- send_email
- search_emails
- read_email
- draft_email
- list_labels
- modify_labels

**Setup:**
```bash
cd ~/mcp-servers/gmail
npm install
npm run auth  # OAuth authentication
```

### **Google Calendar MCP**
**Location:** `~/mcp-servers/google-calendar/`

**Tools:**
- create_event
- list_events
- update_event
- delete_event
- list_calendars

**Setup:**
```bash
cd ~/mcp-servers/google-calendar
npm install
npm run auth
```

### **Stripe MCP**
**Location:** `~/mcp-servers/stripe/`

**Tools:**
- list_customers
- create_invoice
- send_invoice
- list_payments
- create_payment_link

**Setup:**
```bash
cd ~/mcp-servers/stripe
npm install
# Set STRIPE_SECRET_KEY env var
```

### **GitHub MCP**
**Location:** `~/mcp-servers/github-mcp/`

**Tools:**
- repo_list
- issue_create
- pr_create
- pr_merge
- workflow_run

**Setup:**
```bash
cd ~/mcp-servers/github-mcp
npm install
# Uses gh CLI authentication (already done)
```

### **WhatsApp MCP**
**Location:** `~/mcp-servers/whatsapp/`

**Tools:**
- whatsapp_send
- whatsapp_get_chats
- whatsapp_get_messages
- whatsapp_search

**Setup:**
```bash
cd ~/mcp-servers/whatsapp
npm install
npm run auth  # Scan QR code with phone
```

### **Cost Analyzer MCP**
**Location:** `~/mcp-servers/cost-analyzer/`

**Tools:**
- costs_get_summary (AWS + GCP)
- costs_check_aws
- costs_check_gcp
- costs_check_alerts
- costs_history

**Setup:**
```bash
cd ~/mcp-servers/cost-analyzer
npm install
# Requires AWS CLI and gcloud CLI configured
```

---

## 🔧 Creating Your Own MCP Server

### Step 1: Plan Your Tools
What business functions do you need?
- Data access?
- API integrations?
- File processing?
- External services?

### Step 2: Create Project
```bash
cd ~/workspace
mkdir wascar-business-mcp
cd wascar-business-mcp
npm init -y
npm install @anthropic-ai/mcp-server-sdk
```

### Step 3: Define Tools
```javascript
// index.js
const { MCPServer } = require('@anthropic-ai/mcp-server-sdk');
const server = new MCPServer({ name: 'wascar-business-mcp' });

// Example: Client Management Tool
server.tool({
  name: 'get_client',
  description: 'Retrieve client information',
  parameters: {
    client_id: { type: 'string', required: true }
  },
  handler: async ({ client_id }) => {
    // Connect to your database/API
    // Return client data
  }
});

// Example: Invoice Generation Tool
server.tool({
  name: 'generate_invoice',
  description: 'Generate a new invoice',
  parameters: {
    client_id: { type: 'string', required: true },
    amount: { type: 'number', required: true },
    items: { type: 'array', required: true }
  },
  handler: async ({ client_id, amount, items }) => {
    // Generate PDF invoice
    // Store in database
    // Return invoice ID
  }
});

server.start();
```

### Step 4: Add to Claude Config
Edit `~/.claude/config.json`:
```json
{
  "mcpServers": {
    "wascar-business-mcp": {
      "command": "node",
      "args": ["/Users/wascardeleon/workspace/wascar-business-mcp/index.js"],
      "env": {
        "DATABASE_URL": "your-database-url"
      }
    }
  }
}
```

### Step 5: Test
```bash
# Restart Claude Code
claude chat

# Try your tools
> Use the wascar-business-mcp to get client information for client_id ABC123
```

---

## 💡 MCP Use Cases for Your Business

### 1. **Client Management MCP**
- Get client details
- Update client info
- Track project status
- Generate reports

### 2. **Financial Operations MCP**
- Create invoices
- Track payments
- Generate financial reports
- Export to accounting software

### 3. **Task Automation MCP**
- Schedule tasks
- Send notifications
- Process files
- Sync calendars

### 4. **Data Analytics MCP**
- Query databases
- Generate charts
- Export reports
- Real-time metrics

---

## 📖 MCP Documentation

**Official Docs:** https://modelcontextprotocol.io/

**Examples:**
- `mcp-templates/` in this package
- Perry's MCPs in `~/mcp-servers/`

**Key Concepts:**
- **Tools:** Functions Claude can call
- **Resources:** Data Claude can access
- **Prompts:** Pre-defined conversation starters

---

## 🆘 Troubleshooting

### MCP Server Not Starting
```bash
# Check logs
~/.claude/logs/mcp-servers.log

# Test server directly
node /path/to/mcp/index.js
```

### Tool Not Available
```bash
# Restart Claude Code
# Check ~/.claude/config.json syntax
# Verify server is running: ps aux | grep node
```

### Authentication Issues
```bash
# Re-run auth for OAuth MCPs
cd ~/mcp-servers/[service]
npm run auth
```

---

## 🎯 Next Steps

1. **Review Templates:** Check `mcp-templates/` for examples
2. **Identify Needs:** What business functions need automation?
3. **Start Simple:** Create one MCP with 2-3 tools
4. **Test & Iterate:** Use in Claude Code, refine
5. **Expand:** Add more tools as needed

---

**Questions?** Ask Claude Code:
> "How do I create an MCP server that accesses my business database?"

**Created for:** Wascar Deleon
**Project:** AI Implementation & Automation
**Date:** February 8, 2026
