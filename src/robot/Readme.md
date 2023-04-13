The botcode will connect to the gameEngine Server in order to receive messages, but it will also run its own separate robomodules server for internal use.


 server.py is the internal server, 

pacbotCommsModule.py is a module that connects to both the gameEngine server and the local server, 
listens to the gameEngine's LightState messages and forwards them to the local server.
