// Business MCP Server Template
// Customize this for your business operations

const { MCPServer } = require('@anthropic-ai/mcp-server-sdk');

const server = new MCPServer({
  name: 'business-mcp',
  version: '1.0.0',
  description: 'Business operations MCP server'
});

// Tool 1: Get Client Information
server.tool({
  name: 'get_client',
  description: 'Retrieve client information from database',
  parameters: {
    client_id: {
      type: 'string',
      description: 'Unique client identifier',
      required: true
    }
  },
  handler: async ({ client_id }) => {
    // TODO: Connect to your database
    // Example implementation:
    return {
      client_id,
      name: 'Example Client',
      email: 'client@example.com',
      status: 'active',
      projects: [],
      total_revenue: 0
    };
  }
});

// Tool 2: Create Invoice
server.tool({
  name: 'create_invoice',
  description: 'Generate a new invoice for a client',
  parameters: {
    client_id: { type: 'string', required: true },
    amount: { type: 'number', required: true },
    description: { type: 'string', required: true },
    due_date: { type: 'string', required: false }
  },
  handler: async ({ client_id, amount, description, due_date }) => {
    // TODO: Implement invoice generation
    const invoice_id = `INV-${Date.now()}`;

    return {
      invoice_id,
      client_id,
      amount,
      description,
      due_date: due_date || new Date(Date.now() + 30*24*60*60*1000).toISOString(),
      status: 'pending',
      created_at: new Date().toISOString()
    };
  }
});

// Tool 3: Get Financial Summary
server.tool({
  name: 'get_financial_summary',
  description: 'Get financial summary for a time period',
  parameters: {
    start_date: { type: 'string', required: true },
    end_date: { type: 'string', required: true }
  },
  handler: async ({ start_date, end_date }) => {
    // TODO: Query financial data
    return {
      period: { start_date, end_date },
      revenue: 0,
      expenses: 0,
      profit: 0,
      outstanding_invoices: 0,
      paid_invoices: 0
    };
  }
});

// Start the server
server.start();

console.log('Business MCP Server running...');
