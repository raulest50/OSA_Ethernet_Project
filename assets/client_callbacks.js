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
         * @param {number} resolution - The resolution
         * @returns {boolean} - Whether the button should be disabled
         */
        update_acquire_button_state: function(ip_address, wavelength_start, wavelength_end, resolution) {
            // Check if any required field is empty or null
            return !ip_address || !wavelength_start || !wavelength_end || !resolution;
        },

        /**
         * Toggle the visibility of a form section
         * 
         * @param {number} n_clicks - Number of clicks on the toggle button
         * @param {string} current_style - Current style of the form section
         * @returns {object} - Updated style object
         */
        toggle_form_section: function(n_clicks, current_style) {
            if (n_clicks % 2 === 1) {
                return {'display': 'none'};
            } else {
                return {'display': 'block'};
            }
        }
    }
});