const { app, BrowserWindow, shell } = require('electron');
const path = require('path');
const url = require('url');
const { spawn } = require('child_process');

let mainWindow;

app.on('ready', () => {
  mainWindow = new BrowserWindow({ width: 800, height: 600 });

  // Open the Flask app in the Electron window
  const flaskProcess = spawn('python', ['app.py'], {
    cwd: __dirname, // Replace with the path to your Flask app
    shell: true,
  });

  mainWindow.loadURL('http://localhost:5000');

  // Open the DevTools (optional)
  mainWindow.webContents.openDevTools();

  mainWindow.on('closed', () => {
    // Terminate the Flask process when the Electron window is closed
    flaskProcess.kill();
    mainWindow = null;
  });
});
