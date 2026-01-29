
# veri_agents_aiware

This package is part of the Veritone Agents Toolkit and provides various aiWARE related functionality:

- aiware_client: A GraphQL client for interacting with the aiWARE platform used by the agents. Builds on top of the Veritone 'aiware' package.
- content_intelligence: Neuro-symbolic LangGraph agent components for aiWARE content intelligence tasks - natural language interaction with TDOs, Watchlists, Mentions and other aiWARE concepts.
- knowledgebase: Document knowledgebase built on top of aiWARE, usable with LangGraph agents and the rest of the agents toolkit.
- llm_gateway: Code for interacting with the Veritone LLM Gateway.
- tools: Agent tools for interacting with aiWARE.


## GraphQL codegen Client

Update graphql queries in src/veri_agents_aiware/aiware_client/graphql/operations and run:

```
uv run aiware-codegen-client
```

This will update src/veri_agents_aiware/aiware_client.