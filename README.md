<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  
</head>
<body>

  <h1>🏠 Smart Home OS - Terminal CTF Challenge</h1>
  <p>
    A fully interactive text-based escape room and Capture The Flag (CTF) challenge. 
    Players are trapped inside a hyper-modern smart home that has triggered a lockdown protocol. 
    To escape, they must explore rooms, gather clues, unlock the family safe, and decrypt the central AI’s override cipher.
  </p>

  <h2>✨ Features</h2>
  <ul>
    <li><strong>Custom Text Parser</strong> – Navigate rooms using classic MUD-style commands such as <em>go north</em> and <em>examine fridge</em>.</li>
    <li><strong>Dynamic Environment</strong> – Room descriptions and items change as puzzles are solved.</li>
    <li><strong>Auto-Generating Cryptography</strong> – The final hex cipher is generated using XOR encryption with a custom FLAG and KEY.</li>
    <li><strong>Multiplayer Ready</strong> – Can be hosted using netcat, allowing multiple players to connect and play simultaneously.</li>
  </ul>

  <h2>🚀 How to Play (Solo / Local)</h2>
  <p>If you want to run the game locally without hosting a server:</p>
  <ol>
    <li>Ensure Python 3 is installed.</li>
    <li>Clone or download this repository.</li>
    <li>Open a terminal and run:</li>
  </ol>
  <pre><code>python3 smarthome.py</code></pre>

  <h2>🌐 How to Host for Friends (Server Mode)</h2>
  <p>You can host the game so others can connect through their terminal using netcat, giving the experience of connecting to a remote system.</p>

  <h3>1. Start the Server</h3>
  <p>Install socat:</p>
  <pre><code>sudo apt install socat</code></pre>
  <p>Run the following command to bind the game to port 1337:</p>
  <pre><code>socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"python3 -u smarthome.py"</code></pre>
  <p>Your terminal will remain blank while the server listens for incoming connections.</p>

  <h3>2. Connect as a Player</h3>
  <p>Players can connect using netcat.</p>
  <p>If they are on the same local network:</p>
  <pre><code>nc &lt;your_local_ip_address&gt; 1337</code></pre>
  <p>You can test it yourself by opening another terminal and running:</p>
  <pre><code>nc localhost 1337</code></pre>

  <p><strong>Good luck escaping the smart home. The system is watching. 🔐</strong></p>

  <hr>
  <p><em>Developed by Magne Dina Neves</em></p>

</body>
</html>

