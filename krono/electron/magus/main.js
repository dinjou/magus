// main.js
const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow () {
  const win = new BrowserWindow({
    width: 475,
    height: 550,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    },
    autoHideMenuBar: true // This option hides the menu bar
  });

  // Alternatively, you can use the following method after the window is created
  // win.setMenuBarVisibility(false);

  // Load your Django app URL
  win.loadURL('https://magus.nayru.cc/magus/clock_in'); // Adjust the URL as needed

  // Open the DevTools.
  // win.webContents.openDevTools();
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});
