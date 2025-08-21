# MCP Overview

## What is MCP?
The Model Context Protocol (MCP) is a standard Protocal that allows assistants (clients) to communicate with servers (programs) in a consistent way. It enables assistants to call server tools, access resources, and receive structured responses.

## Client vs Server
- Client: The consumer. It asks questions and calls tools exposed by the server.
- Server: The provider. It exposes tools or resources for the client to use.

## Transports
- The communication channel between client and server.
- The simplest transport is stdio (standard input/output).

## Tools
- Tools: Functions that are exposed by the server 
- Clients can discover and call them.
- Example: `ping`, `whoami`, `time_now`.

## Resources
- Resources: Data or files shared by the server.
- Example: The content of a README file or API documentation.
- Resources are read but not executed.

## Prompts
- Prompts: templates or suggestions that the server provides.
- Example: "To get the weather, call get_weather(city)."

## Notifications
- Notifications: One-way messages from server to client.
- Example: "Server shutting down" or "Tool ping was updated."

## Discovery & Tool Calls
1. Client connects to server.
2. Client requests available tools/resources from server.
3. Server responds with a list of tools.
4. Client calls a tool with inputs.
5. Server executes and returns structured result.
6. Client displays result to the user.

