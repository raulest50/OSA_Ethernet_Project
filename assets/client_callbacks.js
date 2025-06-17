// Client-side callbacks for immediate UI feedback

// Disable the acquire button when any of the required fields are empty
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        /**
         * Update the disabled state of the acquire button based on form values
         * 
         * @param {string} ip_address - The IP address of the OSA
         * @param {number} wavelength_start - The start wavelength
         * @param {number} wavelength_end - The end wavelength
         * @returns {boolean} - Whether the button should be disabled
         */
        update_acquire_button_state: function(ip_address, wavelength_start, wavelength_end) {
            // Check if any required field is empty or null
            return !ip_address || !wavelength_start || !wavelength_end;
        }
    }
});
