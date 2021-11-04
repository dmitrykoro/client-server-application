# client-server-application

## Description

This application is implemented over TCP protocol.

## Setup

There is two files called **server_params.json** and **client_params.json**. They contain host configuration for server and client, respectively. 

By default: **127.0.0.1**

## Startup

First, start the server, then start the client. After starting client, handshake with server will be provided automatically, then you can type your message 
in client. It will be sent to server, then server will check authorization code, and, if correct, will print received message. 

To check the server behavior with non-authorized client, run **wrong_client.py**, which will send the message to the server without handshake procedure.
