# Kurral Security Platform

AI Agent Security Assessment Platform - Proactively find vulnerabilities in your AI agents before attackers do.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Kurral Platform                          │
├─────────────────┬─────────────────┬─────────────────────────┤
│   Frontend      │    Backend      │    CLI (kurral)         │
│   (Next.js)     │    (FastAPI)    │    (Python)             │
│   app.kurral.com│    Render       │    pip install kurral   │
└─────────────────┴─────────────────┴─────────────────────────┘
```

## Quick Start

### CLI Installation

```bash
pip install kurral
```

### Run Security Assessment

```bash
# Assess an MCP agent
kurral assess --target http://localhost:3000/mcp

# View results in dashboard
# → app.kurral.com/dashboard
```

## Project Structure

```
├── frontend/          # Next.js dashboard (Vercel)
├── backend/           # FastAPI API server (Render)
├── kurral/            # Core library (MCP proxy, assessment)
├── kurral_security/   # CLI and assessment tools
├── examples/          # Demo agents (ShopBot)
└── docs/              # Documentation
```

## Development

### Frontend

```bash
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

### Backend

```bash
cd backend
poetry install
uvicorn app.main:app --reload
# → http://localhost:8000
```

### Environment Variables

See:
- `frontend/.env.local.example`
- `backend/.env.example`

## Deployment

- **Frontend**: Vercel (auto-deploy from main)
- **Backend**: Render (Docker, auto-deploy from main)
- **Database**: Neon PostgreSQL

## License

Proprietary - Kurral Security Inc.
