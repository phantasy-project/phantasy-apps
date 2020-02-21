window.onload = function () {
    // Initialize the view
    Ui.initializeView();

    // Find and setup any elements that correspond to devices
    Ui.findDevices();

    // Register annotation anchors
    Ui.findAnnotes();
};
